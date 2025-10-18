from typing import TypedDict, List, Dict, Any, Optional, Tuple,Literal, Annotated
from langgraph.graph.message import add_messages

# ----DATASET ----
class DatasetMeta(TypedDict, total=False):
    datasetDescription: str | List[str]   # a
    version: str                          # b (parte 1)
    status: str                           # b (parte 2)
    relevantLinks: List[str]              # c
    developers: List[str]                 # d
    owners: List[str]                     # e
    instructions: str | List[str]         # f
    


# ---- CONFIG ----
class Config(TypedDict, total=False):
    repo_source: str                        # link repo GitHub o path locale
    documents_to_generate: List[Literal["data", "model", "application"]]
    llm_provider: Literal["anthropic"]
    llm_model : str  # es. "claude-3-sonnet-20240229"
    llm_api_key: str    # es. "sk-xxxx"
   


# ---- STATO GLOBALE ----
class State(TypedDict, total=False):
    config: Config
    dataset: DatasetMeta
    messages: Annotated[list, add_messages] #traccia il dialogo con l'LLM
    
    
  
    

