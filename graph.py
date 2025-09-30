from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from states import State
from nodes import init_config, simple_llm_node,compile_artifacts_node
from tools import clone_repo, ask_user_input, read_text_file, list_repo_files
from langchain_core.messages import AIMessage

def _has_tool_calls(state: State) -> bool:
    msgs = state.get("messages") or []
    if not msgs:
        return False
    last = msgs[-1]   # ultimo messaggio
    return isinstance(last, AIMessage) and bool(getattr(last, "tool_calls", None)) # vai ai tool SOLO se l'ultimo è AIMessage *è* contiene almeno una tool_call

    


def _router(state: State):
    return "tools" if _has_tool_calls(state) else "compile"


def build_graph():
    graph = StateGraph(State)
    graph.add_node("setup", init_config)
    graph.add_node("llm_orchestrator", simple_llm_node)
    graph.add_node("toolsNode", ToolNode([clone_repo, ask_user_input, read_text_file, list_repo_files]))
    graph.add_node("compilerNode", compile_artifacts_node)


    graph.set_entry_point("setup")
    graph.add_edge("setup", "llm_orchestrator")
    graph.add_edge("compilerNode", END)


    graph.add_conditional_edges("llm_orchestrator", _router, {
        "tools": "toolsNode",
        "compile": "compilerNode"
    })
    graph.add_edge("toolsNode", "llm_orchestrator")

    return graph.compile()


