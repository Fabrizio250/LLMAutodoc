"""
Entry point for a single run.

  python main.py https://github.com/se4ai2122-cs-uniba/CT-COVID.git
  python main.py <repo> --out renderedDocs/ct-covid
  python main.py <repo> --routing declarative     # override a config value
  python main.py <repo> --config other.yaml       # alternative configuration file
  python main.py <repo> --dry-run / --no-grade / --no-verify   # quick overrides
  python main.py <repo> --mermaid                 # print the graph and exit

All parameters live in config.yaml; the command line only overrides them.
API key: environment variable ANTHROPIC_API_KEY. For repeated experiments use run_experiments.py.
"""

import argparse, json, re
from llmautodoc.graph import build_graph
from llmautodoc.config import build_config, DEFAULT_CONFIG


def clean_mermaid(txt: str) -> str:
    """LangGraph's mermaid, made pasteable into mermaid.live: drop the YAML front matter,
    the HTML tags in labels and the non-breaking spaces."""
    if txt.startswith("---"):
        txt = txt.split("---", 2)[-1].lstrip("\n")
    return re.sub(r"</?p>", "", txt).replace("&nbsp;", " ")


def run(repo: str, out: str | None = None, yaml_path: str = DEFAULT_CONFIG, **overrides) -> dict:
    """Run the graph on a repository and return the final state."""
    cfg = build_config(repo, yaml_path, out, **overrides)
    return build_graph().invoke({"config": cfg})


def summarize(final: dict) -> dict:
    counts, cov = {}, {}
    for fr in final["fields"].values():
        counts[fr["status"]] = counts.get(fr["status"], 0) + 1
        cov[fr.get("covered_by", "n/a")] = cov.get(fr.get("covered_by", "n/a"), 0) + 1
    return {"status": counts, "covered_by": cov, "orchestrator_turns": final.get("orch_turns", 0)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", help="git URL or local path of the repository to document")
    ap.add_argument("--config", default=DEFAULT_CONFIG, help="YAML configuration file")
    ap.add_argument("--out", default=None, help="output directory (default: paths.outputs_dir in config)")
    ap.add_argument("--routing", choices=["agentic", "declarative"], default=None)
    ap.add_argument("--model", default=None)
    ap.add_argument("--grader", default=None)
    ap.add_argument("--top-k", type=int, default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--infer-strategy", action="store_true", help="ablation: hide the field->instrument mapping from the Orchestrator")
    ap.add_argument("--no-grade", action="store_true", help="ablation: disable the CRAG Grader (plain RAG)")
    ap.add_argument("--no-verify", action="store_true")
    ap.add_argument("--mermaid", action="store_true")
    a = ap.parse_args()

    if a.mermaid:
        print(clean_mermaid(build_graph().get_graph().draw_mermaid()))
        return

    final = run(a.repo, a.out, a.config, routing=a.routing, llm_model=a.model, grader_model=a.grader, top_k=a.top_k,
                dry_run=True if a.dry_run else None, verify=False if a.no_verify else None,
                grade=False if a.no_grade else None,
                spec_hints=False if a.infer_strategy else None)

    print("\n=== FIELDS ===")
    for fid, fr in final["fields"].items():
        print(f"{fr['status']:15s} {fr['strategy']:9s} {fid}")
    print("\n=== SUMMARY ===", json.dumps(summarize(final)))
    print("=== OUTPUTS ===", final["outputs"])


if __name__ == "__main__":
    main()
