"""
Run the experiments defined in the `experiments` section of config.yaml:
for each repository x variant x N runs, save renderedDocs/<repo>-<variant>-run<k>/
(data.md, audit.json, evaluation.json/.md/.csv) and write renderedDocs/summary.csv with per-run
metrics plus mean and standard deviation per configuration.

  python run_experiments.py                    # everything in the config
  python run_experiments.py --config exp.yaml  # another config file
  python run_experiments.py --only ct-covid    # one repository
  python run_experiments.py --runs 1           # override the number of runs
  python run_experiments.py --summarize-only   # rebuild summary.csv from existing runs
"""

import argparse, csv, json, os, statistics, sys, time
from llmautodoc.config import load_yaml, DEFAULT_CONFIG, HERE
from main import run, summarize

sys.path.insert(0, os.path.join(HERE, "evaluation"))
from evaluate import evaluate, write_report  # noqa: E402

METRICS = ["coverage", "fill_precision", "abstention_precision", "abstention_recall", "hallucination_rate"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=DEFAULT_CONFIG)
    ap.add_argument("--only", default=None, help="run only this repository")
    ap.add_argument("--runs", type=int, default=None)
    ap.add_argument("--summarize-only", action="store_true")
    a = ap.parse_args()

    y = load_yaml(a.config)
    exp = y.get("experiments", {})
    runs = a.runs or int(exp.get("runs_per_config", 1))
    variants = exp.get("variants") or {v: {"routing": v} for v in exp.get("routings", ["agentic"])}
    repos = [r for r in exp.get("repos", []) if not a.only or r["name"] == a.only]
    out_root = os.path.join(HERE, y.get("paths", {}).get("outputs_dir", "renderedDocs"))
    rows = []

    if a.summarize_only:
        import glob, re
        known_repos = [r["name"] for r in exp.get("repos", [])]
        for d in sorted(glob.glob(os.path.join(out_root, "*-run*"))):
            m = re.match(r"(.+)-run(\d+)$", os.path.basename(d))
            ev = os.path.join(d, "evaluation.json")
            if not m or not os.path.exists(ev):
                continue
            stem = m.group(1)                      # <repo>-<variant>, both may contain hyphens
            repo_name = next((r for r in known_repos if stem.startswith(r + "-")), stem.split("-")[0])
            variant = stem[len(repo_name) + 1:]
            rep = json.load(open(ev)); rep = rep.get("report", rep)
            au = json.load(open(os.path.join(d, "audit.json")))
            row = {"run": os.path.basename(d), "repo": repo_name, "variant": variant, "k": int(m.group(2)),
                   "orch_turns": au.get("orchestrator_turns", 0), **{f"n_{st}": n for st, n in au["summary"].items()}}
            for mt in METRICS:
                row[mt] = rep["overall"][mt]; row[f"retrieval_{mt}"] = rep["retrieval"][mt]
            rows.append(row)
        repos = [{"name": n} for n in sorted({r["repo"] for r in rows})]
        variants = {v: {} for v in sorted({r["variant"] for r in rows})}
        runs = 0

    for repo in repos:
        for vname, overrides in variants.items():
            n_runs = 1 if overrides.get("dry_run") else runs   # dry-run is deterministic
            for k in range(1, n_runs + 1):
                name = f"{repo['name']}-{vname}-run{k}"
                out = os.path.join(out_root, name)
                t0 = time.time()
                print(f"\n▶ {name}")
                final = run(repo["url"], out, a.config, **overrides)
                s = summarize(final)
                row = {"run": name, "repo": repo["name"], "variant": vname, "k": k,
                       "seconds": round(time.time() - t0), **{f"n_{st}": n for st, n in s["status"].items()},
                       "orch_turns": s["orchestrator_turns"]}
                gt = repo.get("groundtruth")
                if gt and os.path.exists(os.path.join(HERE, gt)):
                    ev_rows, report = evaluate(os.path.join(out, "audit.json"), os.path.join(HERE, gt))
                    json.dump({"rows": ev_rows, "report": report}, open(os.path.join(out, "evaluation.json"), "w",
                              encoding="utf-8"), indent=2, ensure_ascii=False)
                    write_report(ev_rows, report, out, name)   # evaluation.md + evaluation.csv
                    for m in METRICS:
                        row[m] = report["overall"][m]
                        row[f"retrieval_{m}"] = report["retrieval"][m]
                rows.append(row)
                print("  ", json.dumps({k: v for k, v in row.items() if k in ("seconds", "orch_turns", *METRICS)}))

    # mean / sd per configuration
    keys = sorted({k for r in rows for k in r})
    for repo in repos:
        for vname in variants:
            grp = [r for r in rows if r["repo"] == repo["name"] and r["variant"] == vname and "coverage" in r]
            if len(grp) > 1:
                mean = {"run": f"{repo['name']}-{vname}-MEAN", "repo": repo["name"], "variant": vname, "k": "mean"}
                for m in METRICS + [f"retrieval_{m}" for m in METRICS]:
                    vals = [r[m] for r in grp if r.get(m) is not None]
                    if vals:
                        mean[m] = round(statistics.mean(vals), 3)
                        mean[m + "_sd"] = round(statistics.pstdev(vals), 3)
                rows.append(mean)
    keys = sorted({k for r in rows for k in r})
    os.makedirs(out_root, exist_ok=True)
    with open(os.path.join(out_root, "summary.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(rows)
    print(f"\n✔ summary: {os.path.join(out_root, 'summary.csv')}")
    write_field_matrix(out_root, list(variants))


def write_field_matrix(out_root: str, known_variants=None):
    """field_matrix.csv: one row per field, one column per variant (outcome of run 1).

    Aggregate metrics can coincide while the underlying fields differ, so the per-field
    comparison is what actually shows what each component changes.
    """
    import glob
    matrix, variants = {}, []
    for d in sorted(glob.glob(os.path.join(out_root, "*-run1"))):
        base, ev = os.path.basename(d)[:-len("-run1")], os.path.join(d, "evaluation.json")
        if not os.path.exists(ev):
            continue
        variant = next((v for v in (known_variants or []) if base.endswith("-" + v)), base.split("-")[-1])
        variants.append(variant)
        for row in json.load(open(ev, encoding="utf-8")).get("rows", []):
            f = matrix.setdefault(row["field"], {"field": row["field"], "strategy": row["strategy"],
                                                 "expected": row["expected"]})
            f[variant] = row["outcome"]
    if not variants:
        return
    path = os.path.join(out_root, "field_matrix.csv")
    cols = ["field", "strategy", "expected"] + variants + ["differs"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
        for row in matrix.values():
            row["differs"] = "yes" if len({row.get(v) for v in variants}) > 1 else ""
            w.writerow({c: row.get(c, "") for c in cols})
    n_diff = sum(1 for row in matrix.values() if row["differs"] == "yes")
    print(f"✔ field matrix: {path}  ({n_diff} fields differ between variants)")


if __name__ == "__main__":
    main()
