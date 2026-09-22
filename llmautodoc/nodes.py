"""
Graph nodes (names match the architecture figure).

  setup      configuration, clone, field initialisation from the field spec
  extract / retrieve   declarative baseline: same tools, run in field-spec order without the LLM Orchestrator
  grader     evidence check per retrieval field (CRAG) -> generate or abstain
  generator  grounded, cited text for the fields with sufficient evidence
  verifier   faithfulness check of the generated text -> abstain if it fails
  compiler   Jinja2 rendering + audit.json

The Orchestrator, Tools and Harvester live in agent.py and tools/.
"""

from __future__ import annotations
import os, json, time, tempfile, subprocess, datetime
from typing import Any

from jinja2 import Environment, FileSystemLoader, Undefined
from langchain_core.messages import AIMessage

from .state import State
from .agent import summarise_choices
from .field_spec import FIELDS, fields_by_strategy
from .tools import run_extractor, run_retrieval, get_retriever
from .tools.deterministic import OUTPUT_MARKER
from .llm import get_models, grade_evidence, generate_field, verify_field


def _trace(state: State, node: str, **kw):
    state.setdefault("trace", []).append({"t": round(time.time(), 2), "node": node, **kw})


def _apply(fr: dict, payload: dict, covered_by: str):
    fr.update({k: payload[k] for k in ("status", "value", "sources", "note")}, covered_by=covered_by)


# ------------------------------------------------------------------ setup
def setup(state: State) -> State:
    cfg = state["config"]                       # already complete: config.yaml + CLI overrides
    state.update(trace=[], messages=[], orch_turns=0)
    _trace(state, "setup", config={k: v for k, v in cfg.items() if k != "llm_api_key"})

    src = cfg["repo_source"]
    if os.path.isdir(src):
        state["repo_path"] = os.path.abspath(src)
    else:
        tmp = tempfile.mkdtemp(prefix="repo_")
        r = subprocess.run(["git", "clone", "--depth", "500", src, tmp], capture_output=True, text=True)
        if r.returncode:
            raise RuntimeError(f"clone failed: {r.stderr}")
        state["repo_path"] = tmp
    if cfg.get("dry_run") and cfg.get("routing") == "agentic":
        _trace(state, "setup", note="dry-run: no LLM available, using the declarative path")
    _trace(state, "setup", cloned=state["repo_path"])

    state["fields"] = {}
    for s in FIELDS:
        human = s.strategy == "human"
        state["fields"][s.id] = {"field": s.id, "section": s.section, "label": s.label, "strategy": s.strategy,
                                 "status": "human_required" if human else "pending", "value": None, "sources": [],
                                 "covered_by": "spec" if human else "pending",
                                 "note": "Judgement/organisational information: must be provided by the manufacturer." if human else ""}
    return state


# ----------------------------------------------- declarative baseline
def extract(state: State) -> State:
    for spec in fields_by_strategy("tool"):
        _apply(state["fields"][spec.id], run_extractor(spec, state["repo_path"]), "declarative")
        _trace(state, "extract", field=spec.id, status=state["fields"][spec.id]["status"])
    return state


def retrieve(state: State) -> State:
    for spec in fields_by_strategy("retrieval"):
        _apply(state["fields"][spec.id], run_retrieval(spec, state["repo_path"], state["config"]["top_k"]), "declarative")
        _trace(state, "retrieve", field=spec.id, n_hits=len(state["fields"][spec.id]["sources"]))
    return state


# ----------------------------------------------------------------- grader
def grader(state: State) -> State:
    r = get_retriever(state["repo_path"])
    state["corpus_stats"] = {"n_chunks": len(r.chunks), "files": sorted({c.file for c in r.chunks})}
    _, judge, _checker = get_models(state["config"])
    grade_on = state["config"].get("grade", True)
    for spec in fields_by_strategy("retrieval"):
        fr = state["fields"][spec.id]
        if not grade_on:
            # Ablation: no evidence grading. Every chunk is passed on and no field is abstained,
            # which is the plain RAG behaviour the CRAG grader is meant to correct.
            fr["grade"] = {"verdict": "CORRECT", "relevant": list(range(len(fr["sources"]))),
                           "mode": "disabled", "rationale": ""}
            _trace(state, "grader", field=spec.id, verdict="DISABLED", relevant=fr["grade"]["relevant"], mode="disabled")
            continue
        g = grade_evidence(spec, fr["sources"], judge, state["config"]["dry_run"])
        fr["grade"] = g
        if g["verdict"] == "INCORRECT":
            fr.update(status="abstained", value=None, note="No sufficient evidence in the repository: " + g.get("rationale", ""))
        _trace(state, "grader", field=spec.id, verdict=g["verdict"], relevant=g["relevant"], mode=g["mode"])
    return state




# -------------------------------------------------------------- generator
def generator(state: State) -> State:
    gen, _, _checker = get_models(state["config"])
    for spec in fields_by_strategy("retrieval"):
        fr = state["fields"][spec.id]
        if fr["status"] == "abstained":
            continue
        rel = [fr["sources"][i] for i in fr["grade"]["relevant"]]      # only the chunks the grader accepted
        fr.update(value=generate_field(spec, rel, gen, state["config"]["dry_run"]), sources=rel,
                  status="filled" if fr["grade"]["verdict"] == "CORRECT" else "partial")
        _trace(state, "generator", field=spec.id, status=fr["status"], n_chunks=len(rel))
    return state


# --------------------------------------------------------------- verifier
def verifier(state: State) -> State:
    _, _judge, checker = get_models(state["config"])
    cfg = state["config"]
    for spec in fields_by_strategy("retrieval"):
        fr = state["fields"][spec.id]
        if fr["status"] not in ("filled", "partial"):
            continue
        if not cfg.get("verify"):
            fr["verification"] = {"faithful": None, "unsupported": [], "mode": "disabled"}
            continue
        v = verify_field(fr["value"], fr["sources"], checker, cfg["dry_run"])
        fr["verification"] = v
        if not v["faithful"]:
            fr.update(status="abstained", value=None,
                      note="Generated text failed the faithfulness check; unsupported: " + "; ".join(v["unsupported"][:3]))
        _trace(state, "verifier", field=spec.id, faithful=v["faithful"], status=fr["status"])
    return state


# ---------------------------------------------------------------- compiler
def _fmt_value(v: Any) -> str:
    """Render a structured extractor value as markdown."""
    if v is None:
        return ""
    if isinstance(v, str):
        return v
    if isinstance(v, list):
        if all(isinstance(x, dict) for x in v):
            return "\n".join("- " + ", ".join(f"{k}: {x[k]}" for k in x if x[k] not in (None, "", [])) for x in v)
        return "\n".join(f"- {x}" for x in v)
    if isinstance(v, dict):
        return "\n".join(f"- **{k}**: {json.dumps(x, ensure_ascii=False) if isinstance(x, (dict, list)) else x}" for k, x in v.items())
    return str(v)


def compiler(state: State) -> State:
    cfg = state["config"]
    env = Environment(loader=FileSystemLoader(cfg["templates_dir"]), autoescape=False, undefined=Undefined, trim_blocks=True, lstrip_blocks=True)
    env.filters["fmt"] = _fmt_value
    os.makedirs(cfg["outputs_doc_dir"], exist_ok=True)
    # Mark the output directory so that a later run never reads its own documents as evidence.
    open(os.path.join(cfg["outputs_doc_dir"], OUTPUT_MARKER), "w").write(
        "Written by LLMAutodoc. Directories carrying this file are excluded from the corpus.\n")

    sections = list(dict.fromkeys(s.section for s in FIELDS))
    counts, covered = {}, {}
    for fr in state["fields"].values():
        counts[fr["status"]] = counts.get(fr["status"], 0) + 1
        covered[fr.get("covered_by", "n/a")] = covered.get(fr.get("covered_by", "n/a"), 0) + 1
    ctx = {"fields": state["fields"], "sections": sections, "specs": FIELDS, "counts": counts, "routing": cfg["routing"],
           "generated_on": datetime.date.today().isoformat(), "repo": cfg["repo_source"], "corpus": state.get("corpus_stats", {})}

    outputs = []
    for d in cfg["documents_to_generate"]:
        try:
            path = os.path.join(cfg["outputs_doc_dir"], f"{d}.md")
            open(path, "w", encoding="utf-8").write(env.get_template(f"{d}.j2").render(**ctx))
            outputs.append(path)
        except Exception as e:
            _trace(state, "compiler", doc=d, error=str(e))

    audit = os.path.join(cfg["outputs_doc_dir"], "audit.json")   # audit trail: how every field was produced
    json.dump({"routing": cfg["routing"], "config": {k: v for k, v in cfg.items() if k != "llm_api_key"},
               "summary": counts, "covered_by": covered, "orchestrator_turns": state.get("orch_turns", 0),
               "strategy_assignment": summarise_choices(state),
               "fields": state["fields"], "trace": state["trace"], "corpus": state.get("corpus_stats", {})},
              open(audit, "w", encoding="utf-8"), ensure_ascii=False, indent=2, default=str)
    outputs.append(audit)
    _trace(state, "compiler", outputs=outputs, summary=counts, covered_by=covered)
    return {"outputs": outputs, "trace": state["trace"], "fields": state["fields"],
            "messages": [AIMessage(content=f"Rendered: {outputs}\nSummary: {counts}\nCovered by: {covered}")]}
