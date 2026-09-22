"""
TOOLS — everything the LLM Orchestrator can call.

Two families, matching the two strategies of the field spec:
  deterministic.py  extract_<field>     facts observable in repository artefacts (no LLM)
  retrieval.py      retrieve_evidence   text evidence from the closed repository corpus (BM25)

Tools return a one-line summary to the model (to keep its context small) and store the full
result in RESULTS, keyed by (repo_path, field_id). The Harvester drains RESULTS into the state.
"""

import json
from typing import Dict, Tuple

RESULTS: Dict[Tuple[str, str], dict] = {}


def preview(value, n: int = 140) -> str:
    s = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, default=str)
    return s[:n] + ("…" if len(s) > n else "")


from .deterministic import DETERMINISTIC_TOOLS, EXTRACTORS, run_extractor   # noqa: E402
from .retrieval import RETRIEVAL_TOOLS, run_retrieval, get_retriever      # noqa: E402

ALL_TOOLS = DETERMINISTIC_TOOLS + RETRIEVAL_TOOLS

__all__ = ["RESULTS", "ALL_TOOLS", "DETERMINISTIC_TOOLS", "RETRIEVAL_TOOLS",
           "EXTRACTORS", "run_extractor", "run_retrieval", "get_retriever", "preview"]
