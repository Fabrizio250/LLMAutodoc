"""
Model access and the three LLM components: GRADER, GENERATOR, VERIFIER.

Two model instances are used in the whole framework (see get_models):
  gen    (llm.model)         LLM Orchestrator (with tools bound, in agent.py) and Generator
  judge  (llm.grader_model)  Grader and Verifier

  grade_evidence  Corrective-RAG grader: does the retrieved evidence answer the field?
                  CORRECT / AMBIGUOUS / INCORRECT (-> abstain)
  generate_field  writes the field using ONLY the relevant chunks, with citations [n]
  verify_field    checks sentence by sentence that the text is supported by the chunks

Every function has a `dry_run` mode (no model call) for offline tests and the no-LLM baseline.
"""

from __future__ import annotations
import json, os, re, time
from typing import Dict, List, Optional

from langchain_core.messages import SystemMessage, HumanMessage


def make_llm(model: str, config: dict, max_tokens: int = 900, temperature: float = 0.0):
    """Build a chat model.

    A model is named either "<claude id>", served by Anthropic, or "<endpoint>:<model id>",
    served by an OpenAI-compatible endpoint declared in config.yaml under llm.endpoints.
    The key of each endpoint is read from the environment variable that the endpoint declares:
    no credential ever appears in the configuration file.
    """
    if ":" in model:
        endpoint, name = model.split(":", 1)
        ep = (config.get("llm_endpoints") or {}).get(endpoint)
        if not ep:
            raise ValueError(f"unknown endpoint '{endpoint}': declare it under llm.endpoints in config.yaml")
        key = os.environ.get(ep["api_key_env"])
        if not key:
            raise ValueError(f"environment variable {ep['api_key_env']} is not set (endpoint '{endpoint}')")
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=name, temperature=temperature, max_tokens=max_tokens,
                          base_url=ep["base_url"], api_key=key)

    from langchain_anthropic import ChatAnthropic
    kw = dict(model=model, temperature=temperature, max_tokens=max_tokens)
    key = config.get("llm_api_key") or os.environ.get("ANTHROPIC_API_KEY")
    if key:
        kw["anthropic_api_key"] = key
    return ChatAnthropic(**kw)


def get_models(config: dict):
    """(gen, judge, checker) from the run config; (None, None, None) in dry-run.

    The three roles are configured independently so that the model which writes a field and the
    model which verifies it may belong to different families.
    """
    if config.get("dry_run"):
        return None, None, None
    grader_model = config.get("grader_model") or config["llm_model"]
    gen = make_llm(config["llm_model"], config, max_tokens=1500)
    judge = make_llm(grader_model, config, max_tokens=1200)
    verifier_model = config.get("verifier_model") or grader_model
    checker = judge if verifier_model == grader_model else make_llm(verifier_model, config, max_tokens=1200)
    return gen, judge, checker


RATE_LIMIT_MARKS = ("429", "rate limit", "rate_limit", "RESOURCE_EXHAUSTED", "quota")


def _invoke(llm, messages, attempts: int = 6):
    """Call the model, waiting out rate limits instead of failing.

    Free tiers allow a handful of requests per minute, while a run issues dozens in sequence.
    The wait is taken from the provider's own retry hint when present, and grows otherwise.
    """
    delay = 8.0
    for i in range(attempts):
        try:
            return llm.invoke(messages)
        except Exception as e:
            msg = str(e)
            if not any(m in msg for m in RATE_LIMIT_MARKS) or i == attempts - 1:
                raise
            m = re.search(r"retry in ([\d.]+)s", msg) or re.search(r"retryDelay['\"]?:\s*['\"]?(\d+)", msg)
            wait = float(m.group(1)) + 1.0 if m else delay
            print(f"    rate limit: waiting {wait:.0f}s ({i + 1}/{attempts - 1})")
            time.sleep(wait)
            delay = min(delay * 2, 60.0)


def _json(text: str) -> Dict:
    """Extract the first balanced JSON object from a model reply.

    Models wrap the object in markdown fences and add prose after it, so a greedy match from the
    first brace to the last one swallows the commentary and fails. The scan below stops at the
    brace that closes the object, ignoring braces inside strings.

    Returns {"_parse_ok": False} when no object can be read. The flag is kept in the audit trail:
    a model whose reply cannot be parsed would otherwise be indistinguishable from a model that
    approves every field, because the caller falls back to a permissive default.
    """
    text = text or ""
    start = text.find("{")
    while start != -1:
        depth, in_str, esc = 0, False, False
        for i in range(start, len(text)):
            ch = text[i]
            if in_str:
                if esc:
                    esc = False
                elif ch == "\\":
                    esc = True
                elif ch == '"':
                    in_str = False
                continue
            if ch == '"':
                in_str = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    try:
                        out = json.loads(text[start:i + 1])
                    except Exception:
                        out = None
                    if isinstance(out, dict):
                        out["_parse_ok"] = True
                        return out
                    break
        start = text.find("{", start + 1)
    return {"_parse_ok": False, "_raw": text[:400]}


def _fmt_chunks(chunks: List[Dict]) -> str:
    return "\n\n".join(f"[{i}] ({c['file']}:{c['line']}, {c['kind']})\n{c['text']}" for i, c in enumerate(chunks))


# ------------------------------------------------------------------ grader
GRADER_PROMPT = (
    "You are an evidence grader for regulatory documentation (EU AI Act, Art. 10). "
    "You are given a FIELD to fill and some CHUNKS extracted from the project repository. "
    "Judge whether the chunks contain information that DIRECTLY answers the field. "
    "Do not use external knowledge. A chunk about a related topic that does not answer the field is NOT relevant.\n"
    "Answer ONLY with JSON: {\"verdict\": \"CORRECT\"|\"AMBIGUOUS\"|\"INCORRECT\", "
    "\"relevant\": [indices of relevant chunks], \"rationale\": \"one sentence\"}\n"
    "CORRECT = at least one chunk answers explicitly; AMBIGUOUS = partial or indirect information; "
    "INCORRECT = no chunk answers."
)


def grade_evidence(spec, chunks: List[Dict], llm=None, dry_run: bool = False) -> Dict:
    if not chunks:
        return {"verdict": "INCORRECT", "relevant": [], "rationale": "no chunks retrieved", "mode": "none"}
    if dry_run or llm is None:   # lexical heuristic: a chunk is relevant if it contains >= 2 keywords
        rel = [i for i, c in enumerate(chunks) if sum(k.lower() in c["text"].lower() for k in spec.keywords) >= 2]
        verdict = "CORRECT" if rel and chunks[rel[0]]["score"] > 4 else ("AMBIGUOUS" if rel else "INCORRECT")
        return {"verdict": verdict, "relevant": rel, "rationale": "lexical heuristic (dry-run)", "mode": "heuristic"}
    human = HumanMessage(content=f"FIELD: {spec.label} ({spec.section})\nEXPECTED CONTENT: {spec.guidance}\n\nCHUNKS:\n{_fmt_chunks(chunks)}")
    out = _json(_invoke(llm, [SystemMessage(content=GRADER_PROMPT), human]).content)
    verdict = out.get("verdict", "INCORRECT")
    rel = [i for i in out.get("relevant", []) if isinstance(i, int) and 0 <= i < len(chunks)]
    if verdict not in ("CORRECT", "AMBIGUOUS") or not rel:
        verdict = "INCORRECT"
    return {"verdict": verdict, "relevant": rel, "rationale": out.get("rationale", ""), "mode": "llm",
            "parse_ok": out.get("_parse_ok", False), "raw": out.get("_raw", "")}


# --------------------------------------------------------------- generator
GENERATOR_PROMPT = (
    "Write the content of a regulatory documentation field in concise technical English (max 150 words). "
    "Use ONLY the information in the provided chunks: do not add, infer, or complete with general knowledge. "
    "If a detail required by the field is not in the chunks, write explicitly 'not documented in the repository'. "
    "Cite the source of every statement with [n], where n is the chunk index. No headings, no preamble."
)


def generate_field(spec, chunks: List[Dict], llm=None, dry_run: bool = False) -> str:
    if dry_run or llm is None:
        return " ".join(f"{c['text'].strip()} [{i}]" for i, c in enumerate(chunks))[:1200]
    human = HumanMessage(content=f"FIELD: {spec.label}\nEXPECTED CONTENT: {spec.guidance}\n\nCHUNKS:\n{_fmt_chunks(chunks)}")
    return _invoke(llm, [SystemMessage(content=GENERATOR_PROMPT), human]).content.strip()


# ---------------------------------------------------------------- verifier
VERIFIER_PROMPT = (
    "You are a reviewer. You are given a generated TEXT and the CHUNKS it must be derived from. "
    "Check sentence by sentence that every FACTUAL statement is supported by the chunks (paraphrases are fine; "
    "a sentence is unsupported only if it introduces a fact, number or entity absent from the chunks). "
    "Sentences stating that something is NOT documented ('not documented in the repository') are abstentions: ignore them. "
    "Answer ONLY with JSON: {\"faithful\": true|false, \"unsupported\": [\"unsupported sentence\", ...]}"
)


def verify_field(text: str, chunks: List[Dict], llm=None, dry_run: bool = False) -> Dict:
    if dry_run or llm is None:
        return {"faithful": True, "unsupported": [], "mode": "skipped"}
    human = HumanMessage(content=f"TEXT:\n{text}\n\nCHUNKS:\n{_fmt_chunks(chunks)}")
    out = _json(_invoke(llm, [SystemMessage(content=VERIFIER_PROMPT), human]).content)
    return {"faithful": bool(out.get("faithful", True)), "unsupported": out.get("unsupported", []), "mode": "llm",
            "parse_ok": out.get("_parse_ok", False), "raw": out.get("_raw", "")}
