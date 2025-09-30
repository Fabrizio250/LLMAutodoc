from typing import TypedDict, List, Dict, Any, Optional, Tuple,Literal, Annotated
from langgraph.graph.message import add_messages

# ----DATASET ----
class DatasetMeta(TypedDict):
    datasetDescription: Optional[str]
    version_and_status: Tuple[Optional[str], Optional[str]]  # (version, status)
    relevantLinks: List[str]
    developers: List[str]
    owners: List[str]
    Instructions: List[str]
    


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
  
    

