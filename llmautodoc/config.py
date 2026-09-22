"""
Configuration: config.yaml -> CLI overrides -> the `config` dict of the graph.
The API key comes ONLY from the environment variable ANTHROPIC_API_KEY.
"""

from __future__ import annotations
import os
import yaml

PKG = os.path.dirname(os.path.abspath(__file__))   # package dir (templates live here)
HERE = os.path.dirname(PKG)                          # project root (config.yaml, renderedDocs)
DEFAULT_CONFIG = os.path.join(HERE, "config.yaml")


def load_yaml(path: str = DEFAULT_CONFIG) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def build_config(repo_source: str, yaml_path: str = DEFAULT_CONFIG, out_dir: str | None = None, **overrides) -> dict:
    """Flatten the YAML into the graph config; overrides (non-None) win over the file."""
    y = load_yaml(yaml_path)
    llm, pipe, paths = y.get("llm", {}), y.get("pipeline", {}), y.get("paths", {})
    cfg = {
        "repo_source": repo_source,
        "documents_to_generate": pipe.get("documents_to_generate", ["data"]),
        "templates_dir": os.path.join(PKG, paths.get("templates_dir", "templates")),
        "outputs_doc_dir": out_dir or os.path.join(HERE, paths.get("outputs_dir", "renderedDocs")),
        "llm_provider": llm.get("provider", "anthropic"),
        "llm_model": llm.get("model", "claude-sonnet-4-6"),
        "grader_model": llm.get("grader_model", "claude-haiku-4-5-20251001"),
        # The model that verifies may differ from the model that grades and from the model that
        # writes: an empty value means "the same as the grader".
        "verifier_model": llm.get("verifier_model") or llm.get("grader_model", "claude-haiku-4-5-20251001"),
        "llm_endpoints": llm.get("endpoints", {}),
        "llm_api_key": os.environ.get("ANTHROPIC_API_KEY"),
        "routing": pipe.get("routing", "agentic"),
        "top_k": int(pipe.get("top_k", 5)),
        "spec_hints": bool(pipe.get("spec_hints", True)),
        "grade": bool(pipe.get("grade", True)),
        "verify": bool(pipe.get("verify", True)),
        "max_orch_turns": int(pipe.get("max_orch_turns", 8)),
        "dry_run": bool(pipe.get("dry_run", False)),
        "config_file": os.path.abspath(yaml_path),
    }
    cfg.update({k: v for k, v in overrides.items() if v is not None})
    return cfg
