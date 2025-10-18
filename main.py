from graph import build_graph
from states import State
from langchain_core.messages import AIMessage

if __name__ == "__main__":
    compiled_graph = build_graph()

    state: State = {
        "config": {
            "repo_source": "https://github.com/se4ai2122-cs-uniba/CT-COVID.git",
            "documents_to_generate": ["data"],
            "templates_dir": "./templates",                   
            "outputs_doc_dir": "./renderedDocs",  
            "llm_provider": "anthropic",
            "llm_model": "claude-3-haiku-20240307",
            "llm_api_key":"" # "llm_api_key": "<LA_TUA_CHIAVE>"
        }
    }

    final_state = compiled_graph.invoke(state)

    
    print("\n=== CONVERSAZIONE ===")
    for m in final_state.get("messages", []):
        role = m.__class__.__name__.replace("Message", "").upper()
        print(f"{role}: {getattr(m, 'content', '')}")

    print("Final state:")
    print(final_state["dataset"])

    print("\n=== DEBUG ===")
    print(final_state.get("debug"))


    #print("Graph structure:")
    #print(compiled_graph.get_graph().draw_mermaid())
