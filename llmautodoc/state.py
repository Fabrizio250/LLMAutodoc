"""
Shared state of the graph (the contract between nodes). No logic here.
"""

from typing import TypedDict, List, Dict, Any, Optional, Literal, Annotated
from langgraph.graph.message import add_messages

FieldStatus = Literal["pending", "filled", "partial", "abstained", "not_observable", "human_required", "unverified"]


class FieldResult(TypedDict, total=False):
    """One field of the document: its value and HOW it was obtained."""
    field: str
    section: str
    label: str
    strategy: str                  # tool | retrieval | human
    status: FieldStatus
    value: Any                     # str / list / dict, or None
    sources: List[Dict[str, Any]]  # provenance: file, line, detail
    grade: Dict[str, Any]          # grader verdict (retrieval fields)
    verification: Dict[str, Any]   # verifier result (retrieval fields)
    covered_by: str                # orchestrator | fallback | declarative | spec
    note: str


class Config(TypedDict, total=False):
    repo_source: str
    documents_to_generate: List[Literal["data", "model", "application"]]
    templates_dir: str
    outputs_doc_dir: str
    llm_provider: Literal["anthropic"]
    llm_model: str                 # Orchestrator + Generator
    grader_model: str              # Grader
    verifier_model: str            # Verifier (may belong to another family)
    llm_endpoints: Dict[str, Any]  # OpenAI-compatible endpoints declared in config.yaml
    spec_hints: bool               # give the Orchestrator the field -> instrument mapping
    grade: bool                    # CRAG grader on/off
    llm_api_key: Optional[str]
    routing: Literal["agentic", "declarative"]
    top_k: int
    verify: bool
    max_orch_turns: int
    dry_run: bool
    config_file: str


class State(TypedDict, total=False):
    config: Config
    repo_path: str
    corpus_stats: Dict[str, Any]
    fields: Dict[str, FieldResult]
    trace: List[Dict[str, Any]]    # execution trace (audit trail)
    outputs: List[str]
    orch_turns: int
    orch_choice: Dict[str, str]    # field -> instrument the Orchestrator actually called
    messages: Annotated[list, add_messages]   # orchestrator conversation (accumulated)
