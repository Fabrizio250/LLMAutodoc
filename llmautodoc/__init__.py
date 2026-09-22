"""
LLMAutodoc — agentic framework for regulatory data documentation (EU AI Act, Art. 10).

    from llmautodoc import build_graph, build_config
    final = build_graph().invoke({"config": build_config("https://github.com/org/repo.git")})
"""
from .graph import build_graph
from .config import build_config, load_yaml, DEFAULT_CONFIG
from .field_spec import FIELDS, BY_ID, fields_by_strategy

__all__ = ["build_graph", "build_config", "load_yaml", "DEFAULT_CONFIG", "FIELDS", "BY_ID", "fields_by_strategy"]
__version__ = "1.0.0"
