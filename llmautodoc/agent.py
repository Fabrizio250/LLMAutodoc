"""
LLM ORCHESTRATOR and HARVESTER (the agentic loop of the graph).

  llm_orchestrator  an LLM with the tools bound: reads the field spec and decides which tools
                    to call to collect evidence, observes the results, iterates (ReAct).
  harvester         moves the tool results (tools.RESULTS) into state["fields"].

The field spec constrains the Orchestrator (which strategy is allowed for each field) but does
not replace it: the model chooses which tools to call and when it is done. Fields it leaves
uncovered are completed by `coverage_fallback` and recorded in the trace.
"""

from __future__ import annotations
from typing import List

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from .field_spec import FIELDS, BY_ID
from .tools import RESULTS, ALL_TOOLS, run_extractor, run_retrieval
from .llm import get_models


def _spec_table(hints: bool = True) -> str:
    """With hints=True every field carries the action allowed by the specification.
    With hints=False the Orchestrator sees only what the template itself provides, section and
    label, and must infer which instrument fits (ablation of the strategy assignment).
    `guidance` is withheld on purpose: it is written only for retrieval fields, so showing it
    would reveal the answer."""
    rows = []
    for s in FIELDS:
        if not hints:
            rows.append(f"- {s.id} [{s.section}] {s.label}")
        elif s.strategy == "tool":
            rows.append(f"- {s.id} [{s.section}] -> tool: extract_{s.id}")
        elif s.strategy == "retrieval":
            rows.append(f"- {s.id} [{s.section}] -> retrieve_evidence(field_id='{s.id}')")
        else:
            rows.append(f"- {s.id} [{s.section}] -> human (do NOT call any tool: requires human input)")
    return "\n".join(rows)


ORCHESTRATOR_PROMPT = (
    "You are the orchestrator of a framework that produces the regulatory Data Documentation "
    "(EU AI Act, Art. 10) of a machine-learning repository. Your job is NOT to write the document: "
    "it is to collect evidence for each field by calling the tools allowed by the field specification.\n\n"
    "RULES\n"
    "1. For every field with strategy 'tool' call the tool extract_<field>.\n"
    "2. For every field with strategy 'retrieval' call retrieve_evidence with that field_id.\n"
    "3. Never call tools for 'human' fields.\n"
    "4. Call MANY tools in the same turn (in parallel), not one at a time.\n"
    "5. Never invent values: values come from the tools. Do not summarise results.\n"
    "6. When every tool/retrieval field has been called, answer only: DONE\n\n"
    "FIELD SPECIFICATION (id [section] -> allowed action)\n" + _spec_table(True)
)

# Ablation: the field-strategy mapping is NOT given. The Orchestrator sees only what each field
# asks for and must decide which instrument fits, or that no instrument does.
ORCHESTRATOR_PROMPT_NOHINTS = (
    "You are the orchestrator of a framework that produces the regulatory Data Documentation "
    "(EU AI Act, Art. 10) of a machine-learning repository. Your job is NOT to write the document: "
    "it is to collect the evidence for each field by calling the appropriate instrument.\n\n"
    "AVAILABLE INSTRUMENTS\n"
    "a. extract_<field_id>: a deterministic extractor. Use it when the value is an observable fact "
    "recorded by a tool (git history, DVC pointers, LICENSE, dvc.yaml, source code).\n"
    "b. retrieve_evidence(field_id): retrieves text fragments from the repository (README, reports, "
    "notebooks, docstrings). Use it when the answer was written in prose by a person.\n"
    "c. no instrument at all: when the field records a judgement or an organisational decision that "
    "cannot reside in the repository (conformity assessment, reviewers, retention policy).\n\n"
    "RULES\n"
    "1. Decide for EACH field which of a, b or c applies, and act accordingly.\n"
    "2. Call MANY tools in the same turn (in parallel), not one at a time.\n"
    "3. Never invent values: values come from the tools. Do not summarise results.\n"
    "4. When you have acted on every field, answer only: DONE\n\n"
    "FIELDS (id [section] label), as the template provides them\n" + _spec_table(False)
)


def pending_fields(state) -> List[str]:
    return [fid for fid, fr in state["fields"].items() if fr["status"] == "pending"]


# ------------------------------------------------------------ orchestrator
def llm_orchestrator(state):
    """One turn of the model with the tools bound. First turn: seed messages. Next turns: history + reminder."""
    gen, _judge, _checker = get_models(state["config"])        # same model as the Generator, here with tools bound
    llm = gen.bind_tools(ALL_TOOLS)
    prompt = ORCHESTRATOR_PROMPT if state["config"].get("spec_hints", True) else ORCHESTRATOR_PROMPT_NOHINTS
    msgs = state.get("messages") or []
    state["orch_turns"] = state.get("orch_turns", 0) + 1

    if not msgs:
        human = HumanMessage(content=(f"Repository to document: {state['config']['repo_source']} (already cloned). "
                                      f"Documents requested: {', '.join(state['config']['documents_to_generate'])}. "
                                      "Collect the evidence for every tool and retrieval field, then answer DONE."))
        ai = llm.invoke([SystemMessage(content=prompt), human])
        out = [SystemMessage(content=prompt), human, ai]
    else:
        pend = [f for f in pending_fields(state) if state["fields"][f]["strategy"] != "human"]
        if pend and state["orch_turns"] <= state["config"].get("max_orch_turns", 8):
            reminder = HumanMessage(content=f"Fields still without evidence: {pend}. Call the corresponding tools or answer DONE.")
            ai = llm.invoke(msgs + [reminder])
            out = [reminder, ai]
        else:
            ai, out = AIMessage(content="DONE"), [AIMessage(content="DONE")]

    raw = getattr(ai, "tool_calls", []) or []
    calls = [tc["name"] for tc in raw]
    _record_choices(state, raw)
    state.setdefault("trace", []).append({"node": "llm_orchestrator", "turn": state["orch_turns"],
                                          "tool_calls": len(calls), "tools": calls})
    if not calls:
        coverage_fallback(state)   # last act of the orchestrator: guarantee coverage
    # orch_choice must be returned: only the keys a node returns are merged into the shared state.
    return {"messages": out, "orch_turns": state["orch_turns"], "trace": state["trace"],
            "fields": state["fields"], "orch_choice": state.get("orch_choice", {})}


def _record_choices(state, raw_calls) -> None:
    """Record which instrument the Orchestrator chose for each field, to compare it with the
    strategy the specification prescribes (see summarise_choices)."""
    ch = state.setdefault("orch_choice", {})
    for tc in raw_calls:
        name, args = tc.get("name", ""), (tc.get("args") or {})
        if name.startswith("extract_"):
            ch.setdefault(name[len("extract_"):], "tool")
        elif name == "retrieve_evidence" and args.get("field_id"):
            ch.setdefault(args["field_id"], "retrieval")


def summarise_choices(state) -> dict:
    """Agreement between the instrument chosen by the Orchestrator and the prescribed strategy."""
    if state["config"].get("routing") != "agentic" or state["config"].get("dry_run"):
        return {"applicable": False, "reason": "the Orchestrator does not run in this configuration"}
    ch = state.get("orch_choice") or {}
    per, agree = {}, 0
    for spec in FIELDS:
        chosen = ch.get(spec.id, "none")          # 'none' = no instrument called
        ok = (chosen == spec.strategy) or (spec.strategy == "human" and chosen == "none")
        agree += int(ok)
        per[spec.id] = {"expected": spec.strategy, "chosen": chosen, "agree": ok}
    return {"applicable": True, "n_fields": len(FIELDS), "agreement": agree,
            "rate": round(agree / len(FIELDS), 3) if FIELDS else 0.0, "per_field": per}


def has_tool_calls(state) -> bool:
    msgs = state.get("messages") or []
    return bool(msgs) and isinstance(msgs[-1], AIMessage) and bool(getattr(msgs[-1], "tool_calls", None))


# --------------------------------------------------------------- harvester
def harvester(state):
    """Drain tools.RESULTS for this repository into state['fields']."""
    repo, n = state["repo_path"], 0
    for (rp, fid), payload in list(RESULTS.items()):
        if rp != repo:
            continue
        state["fields"][fid].update({k: payload[k] for k in ("status", "value", "sources", "note")}, covered_by="orchestrator")
        del RESULTS[(rp, fid)]
        n += 1
    left = [f for f in pending_fields(state) if state["fields"][f]["strategy"] != "human"]
    state["trace"].append({"node": "harvester", "harvested": n, "pending": len(left)})
    return state


def coverage_fallback(state):
    """Complete tool/retrieval fields the orchestrator left pending, and record which ones."""
    repo, missed = state["repo_path"], []
    for fid in pending_fields(state):
        spec = BY_ID[fid]
        if spec.strategy == "tool":
            payload = run_extractor(spec, repo)
        elif spec.strategy == "retrieval":
            payload = run_retrieval(spec, repo, state["config"]["top_k"])
        else:
            continue
        state["fields"][fid].update({k: payload[k] for k in ("status", "value", "sources", "note")}, covered_by="fallback")
        missed.append(fid)
    state["trace"].append({"node": "coverage_fallback", "missed_by_orchestrator": missed})
    return state
