from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from states import State
from nodes import init_config, llm_orchestrator,compile_artifacts_node,harvest_tool_results, generate_contents
from tools import clone_repo, description, detectDatasetOwners,detectDatasetStatus
from langchain_core.messages import AIMessage

def _has_tool_calls(state: State) -> bool:
    msgs = state.get("messages") or []
    if not msgs:
        return False
    last = msgs[-1]   # ultimo messaggio
    return isinstance(last, AIMessage) and bool(getattr(last, "tool_calls", None)) # vai a toolNode solo se l' ultimo AI message contiene una tool call

    


def _router(state: State):
    return "tools" if _has_tool_calls(state) else "generate"


def build_graph():
    graph = StateGraph(State)
    graph.add_node("setup", init_config)
    graph.add_node("llm_orchestrator", llm_orchestrator)
    graph.add_node("toolsNode", ToolNode([clone_repo, description, detectDatasetOwners,detectDatasetStatus]))
    graph.add_node("compilerNode", compile_artifacts_node)
    graph.add_node("harvesterNode",harvest_tool_results)
    graph.add_node("generatorNode",generate_contents)


    graph.set_entry_point("setup")
    graph.add_edge("setup", "llm_orchestrator")
    graph.add_edge("toolsNode","harvesterNode")
    graph.add_edge("harvesterNode", "llm_orchestrator")
    graph.add_edge("compilerNode", END)
    graph.add_edge("generatorNode", "compilerNode")



    graph.add_conditional_edges("llm_orchestrator", _router, {
        "tools": "toolsNode",
        "generate": "generatorNode"
    })

    return graph.compile()




