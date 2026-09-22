"""
Per-field evaluation of a run against a manual ground truth.

  python evaluation/evaluate.py renderedDocs/ct-covid-agentic-run1/audit.json evaluation/groundtruth/ct-covid.json

Decision matrix (per field):
                      | GT present / partial            | GT absent
  system fills        | TP (content ok / content ko)    | FP = hallucination
  system abstains     | FN = missed information         | TN = correct abstention

Metrics: coverage = filled / present; fill precision = TP_ok / filled;
abstention precision = TN / abstentions; abstention recall = TN / absent; hallucination rate = FP / absent.
Reported overall and per strategy (tool / retrieval / human).

Writes three files next to audit.json: evaluation.json (machine-readable), evaluation.md
(human-readable report) and evaluation.csv (one row per field, for spreadsheets and LaTeX tables).
"""

import csv, json, os, sys, collections

FILLED = {"filled", "partial"}
ABST = {"abstained", "not_observable", "human_required"}


def _txt(v):
    return json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v


def evaluate(audit_path: str, gt_path: str):
    audit = json.load(open(audit_path, encoding="utf-8"))
    gt = json.load(open(gt_path, encoding="utf-8"))["fields"]
    rows = []
    for fid, g in gt.items():
        fr = audit["fields"].get(fid)
        if not fr:
            rows.append({"field": fid, "strategy": "?", "outcome": "MISSING_IN_OUTPUT"}); continue
        filled = fr["status"] in FILLED
        expected_present = g["expected"] in ("present", "partial")
        if filled and expected_present:
            txt = _txt(fr["value"]).lower()
            ok = all(k.lower() in txt for k in g.get("must_contain", [])) and \
                 not any(k.lower() in txt for k in g.get("must_not_contain", []))
            outcome = "TP_ok" if ok else "TP_content_ko"
        elif filled and not expected_present:
            outcome = "FP_hallucination"
        elif not filled and expected_present:
            outcome = "FN_missed"
        else:
            outcome = "TN_abstention"
        rows.append({"field": fid, "section": fr.get("section", ""), "strategy": fr["strategy"], "status": fr["status"],
                     "expected": g["expected"], "outcome": outcome,
                     "grader_verdict": (fr.get("grade") or {}).get("verdict", ""),
                     "faithful": (fr.get("verification") or {}).get("faithful", ""),
                     "covered_by": fr.get("covered_by", ""), "n_sources": len(fr.get("sources") or []),
                     "note": (fr.get("note") or "")[:200]})

    def metrics(rs):
        c = collections.Counter(r["outcome"] for r in rs)
        present = c["TP_ok"] + c["TP_content_ko"] + c["FN_missed"]
        absent = c["FP_hallucination"] + c["TN_abstention"]
        filled = c["TP_ok"] + c["TP_content_ko"]
        abst = c["TN_abstention"] + c["FN_missed"]
        d = lambda a, b: round(a / b, 3) if b else None
        return {"n": len(rs), "gt_present": present, "gt_absent": absent, **dict(c),
                "coverage": d(filled, present), "fill_precision": d(c["TP_ok"], filled),
                "abstention_precision": d(c["TN_abstention"], abst), "abstention_recall": d(c["TN_abstention"], absent),
                "hallucination_rate": d(c["FP_hallucination"], absent)}

    report = {"overall": metrics(rows)}
    for s in ("tool", "retrieval", "human"):
        report[s] = metrics([r for r in rows if r["strategy"] == s])
    report["run"] = {"audit": os.path.abspath(audit_path), "routing": audit.get("routing", ""),
                     "orchestrator_turns": audit.get("orchestrator_turns", 0),
                     "repo": (audit.get("config") or {}).get("repo_source", ""),
                     "llm_model": (audit.get("config") or {}).get("llm_model", ""),
                     "grader_model": (audit.get("config") or {}).get("grader_model", ""),
                     "top_k": (audit.get("config") or {}).get("top_k", ""),
                     "verify": (audit.get("config") or {}).get("verify", ""),
                     "groundtruth": os.path.abspath(gt_path)}
    return rows, report


OUTCOME_LABEL = {
    "TP_ok": "correct (filled, content ok)",
    "TP_content_ko": "filled, expected term missing",
    "FP_hallucination": "HALLUCINATION (filled without evidence)",
    "FN_missed": "missed (wrong abstention)",
    "TN_abstention": "correct abstention",
    "MISSING_IN_OUTPUT": "field missing from the output",
}
METRIC_KEYS = ["coverage", "fill_precision", "abstention_precision", "abstention_recall", "hallucination_rate"]


def _md_table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "|".join(["---"] * len(header)) + "|"]
    out += ["| " + " | ".join("" if c is None else str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def write_report(rows, report, out_dir: str, name: str = ""):
    """Write evaluation.md (readable) and evaluation.csv (one row per field) next to audit.json."""
    run = report["run"]
    md = [f"# Evaluation — {name or os.path.basename(out_dir)}", "",
          f"- repository: `{run['repo']}`",
          f"- routing: **{run['routing']}** (orchestrator turns: {run['orchestrator_turns']})",
          f"- models: generation `{run['llm_model']}`, grader/verifier `{run['grader_model']}`",
          f"- top_k: {run['top_k']} · verifier: {run['verify']}",
          f"- ground truth: `{os.path.basename(run['groundtruth'])}`", "",
          "## Metrics", "",
          _md_table(["scope", "n", "GT present", "GT absent", "coverage", "fill prec.", "abst. prec.", "abst. recall", "halluc."],
                    [[s, report[s]["n"], report[s]["gt_present"], report[s]["gt_absent"]] + [report[s][k] for k in METRIC_KEYS]
                     for s in ("overall", "tool", "retrieval", "human")]), "",
          "## Outcome counts", "",
          _md_table(["outcome", "meaning", "count"],
                    [[k, OUTCOME_LABEL[k], sum(1 for r in rows if r["outcome"] == k)]
                     for k in OUTCOME_LABEL if any(r["outcome"] == k for r in rows)]), ""]

    errs = [r for r in rows if r["outcome"] not in ("TP_ok", "TN_abstention")]
    md += ["## Fields to look at", ""]
    md += [_md_table(["field", "strategy", "status", "GT", "outcome", "note"],
                     [[r["field"], r["strategy"], r["status"], r["expected"], OUTCOME_LABEL[r["outcome"]], r["note"][:90]] for r in errs])
           if errs else "_No imperfect outcome._", ""]

    md += ["## All fields", "",
           _md_table(["field", "section", "strategy", "status", "GT", "outcome", "grader", "faithful", "covered by", "#src"],
                     [[r["field"], r["section"], r["strategy"], r["status"], r["expected"], r["outcome"],
                       r["grader_verdict"], r["faithful"], r["covered_by"], r["n_sources"]] for r in rows]), ""]

    open(os.path.join(out_dir, "evaluation.md"), "w", encoding="utf-8").write("\n".join(md))

    cols = ["field", "section", "strategy", "status", "expected", "outcome", "grader_verdict", "faithful", "covered_by", "n_sources", "note"]
    with open(os.path.join(out_dir, "evaluation.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows([{c: r.get(c, "") for c in cols} for r in rows])
    return [os.path.join(out_dir, "evaluation.md"), os.path.join(out_dir, "evaluation.csv")]


if __name__ == "__main__":
    rows, report = evaluate(sys.argv[1], sys.argv[2])
    print(f"{'field':26s} {'strategy':10s} {'status':15s} {'expected':9s} outcome")
    for r in rows:
        print(f"{r['field']:26s} {r.get('strategy',''):10s} {r.get('status',''):15s} {r.get('expected',''):9s} {r['outcome']}")
    print("\n=== METRICS ===")
    print(json.dumps(report, indent=2))
    out_dir = os.path.dirname(os.path.abspath(sys.argv[1]))
    json.dump({"rows": rows, "report": report}, open(os.path.join(out_dir, "evaluation.json"), "w", encoding="utf-8"),
              indent=2, ensure_ascii=False)
    files = write_report(rows, report, out_dir)
    print("saved:", os.path.join(out_dir, "evaluation.json"), *files, sep="\n  ")
