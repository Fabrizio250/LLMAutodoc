"""
The LangGraph state graph (node names match the architecture figure).

routing = "agentic" (default)
    setup -> llm_orchestrator <-> (tools -> harvester) -> grader -> generator -> verifier -> compiler -> END
                                                            '--- (all fields abstained) ---------------^
routing = "declarative" (baseline)
    setup -> extract -> retrieve -> grader -> generator -> verifier -> compiler -> END
"""

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from .state import State
from .nodes import setup, extract, retrieve, grader, generator, verifier, compiler
from .agent import llm_orchestrator, harvester, has_tool_calls
from .tools import ALL_TOOLS


def _after_setup(state: State) -> str:
    """Dry-run has no model to orchestrate, so it always takes the declarative path."""
    cfg = state["config"]
    if cfg.get("dry_run") or cfg.get("routing", "agentic") != "agentic":
        return "declarative"
    return "agentic"


def _after_orchestrator(state: State) -> str:
    return "tools" if has_tool_calls(state) else "grader"


def _after_grader(state: State) -> str:
    """Skip generation when no retrieval field has sufficient evidence."""
    any_ok = any(fr["strategy"] == "retrieval" and fr["status"] != "abstained" for fr in state["fields"].values())
    return "generator" if any_ok else "compiler"


def build_graph():
    g = StateGraph(State)
    g.add_node("setup", setup)
    g.add_node("llm_orchestrator", llm_orchestrator)
    g.add_node("tools", ToolNode(ALL_TOOLS))
    g.add_node("harvester", harvester)
    g.add_node("extract", extract)        # baseline
    g.add_node("retrieve", retrieve)      # baseline
    g.add_node("grader", grader)
    g.add_node("generator", generator)
    g.add_node("verifier", verifier)
    g.add_node("compiler", compiler)

    g.set_entry_point("setup")
    g.add_conditional_edges("setup", _after_setup, {"agentic": "llm_orchestrator", "declarative": "extract"})
    g.add_conditional_edges("llm_orchestrator", _after_orchestrator, {"tools": "tools", "grader": "grader"})
    g.add_edge("tools", "harvester")
    g.add_edge("harvester", "llm_orchestrator")
    g.add_edge("extract", "retrieve")
    g.add_edge("retrieve", "grader")
    g.add_conditional_edges("grader", _after_grader, {"generator": "generator", "compiler": "compiler"})
    g.add_edge("generator", "verifier")
    g.add_edge("verifier", "compiler")
    g.add_edge("compiler", END)
    return g.compile()
