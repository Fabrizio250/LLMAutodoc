"""
Retrieval tool (strategy "retrieval").

Builds a closed corpus from the text found in the repository (markdown, PDF reports, notebook
markdown cells, Python docstrings and comments, YAML configs) and retrieves the most relevant
chunks for a field with BM25. No external source is ever used: if the repository does not
contain the information, retrieval must fail visibly (the Grader will then abstain).

Every chunk keeps its provenance (file, line).
"""

from __future__ import annotations
import os, re, json
from dataclasses import dataclass, asdict
from typing import Annotated, Dict, List

from rank_bm25 import BM25Okapi
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState

from . import RESULTS
from .deterministic import SKIP_DIRS, prune, rel
from ..field_spec import BY_ID

MAX_CHUNK = 900   # characters
MIN_CHUNK = 60


@dataclass
class Chunk:
    id: int
    file: str
    line: int
    kind: str      # markdown | pdf | notebook | docstring | comment | yaml
    text: str

    def to_dict(self):
        return asdict(self)


# ------------------------------------------------------------ corpus build
def _split(text: str, file: str, kind: str, start_line: int = 1) -> List[Dict]:
    """Split by paragraphs/headings up to MAX_CHUNK; long paragraphs (PDF pages) are split by sentence."""
    paras = []
    for para in re.split(r"\n\s*\n", text):
        if len(para) <= MAX_CHUNK:
            paras.append(para)
            continue
        cur = ""
        for s in re.split(r"(?<=[.!?])\s+", para):
            if cur and len(cur) + len(s) > MAX_CHUNK:
                paras.append(cur); cur = s
            else:
                cur = (cur + " " + s).strip()
        if cur:
            paras.append(cur)
    out, buf, buf_line, line = [], [], start_line, start_line
    for para in paras:
        n_lines = para.count("\n") + 2
        p = para.strip()
        if not p:
            line += n_lines
            continue
        if buf and (p.startswith("#") or sum(len(b) for b in buf) + len(p) > MAX_CHUNK):
            out.append({"file": file, "line": buf_line, "kind": kind, "text": "\n\n".join(buf)})
            buf = []
        if not buf:
            buf_line = line
        buf.append(p)
        line += n_lines
    if buf:
        out.append({"file": file, "line": buf_line, "kind": kind, "text": "\n\n".join(buf)})
    return [c for c in out if len(c["text"]) >= MIN_CHUNK]


def _pdf_text(path: str) -> str:
    try:
        from pypdf import PdfReader
        return "\n\n".join(f"[page {i+1}]\n" + (p.extract_text() or "") for i, p in enumerate(PdfReader(path).pages[:60]))
    except Exception:
        return ""


def _notebook_md(path: str) -> str:
    try:
        nb = json.load(open(path, encoding="utf-8"))
        return "\n\n".join("".join(c.get("source", [])) for c in nb.get("cells", []) if c.get("cell_type") == "markdown")
    except Exception:
        return ""


def _py_docs(path: str) -> List[Dict]:
    """Docstrings and consecutive comment blocks of a Python file, with line numbers."""
    out = []
    try:
        src = open(path, encoding="utf-8", errors="ignore").read()
    except Exception:
        return out
    for m in re.finditer(r'"""(.*?)"""|\'\'\'(.*?)\'\'\'', src, re.S):
        txt = (m.group(1) or m.group(2) or "").strip()
        if len(txt) >= MIN_CHUNK:
            out.append({"line": src[:m.start()].count("\n") + 1, "kind": "docstring", "text": txt})
    buf, start = [], None
    for i, l in enumerate(src.splitlines(), 1):
        s = l.strip()
        if s.startswith("#") and not s.startswith("#!"):
            start = start or i
            buf.append(s.lstrip("# ").rstrip())
        else:
            if buf and len(" ".join(buf)) >= MIN_CHUNK:
                out.append({"line": start, "kind": "comment", "text": "\n".join(buf)})
            buf, start = [], None
    return out


def build_corpus(repo: str) -> List[Chunk]:
    chunks: List[Dict] = []
    for root, dirs, files in os.walk(repo):
        prune(root, dirs)
        dirs[:] = [d for d in dirs if d != "frontend"]
        for fn in files:
            p, r, ext = os.path.join(root, fn), rel(repo, os.path.join(root, fn)), os.path.splitext(fn)[1].lower()
            try:
                if ext in (".md", ".rst", ".txt") and "requirements" not in fn.lower() and "license" not in fn.lower():
                    chunks += _split(open(p, encoding="utf-8", errors="ignore").read(), r, "markdown")
                elif ext == ".pdf":
                    chunks += _split(_pdf_text(p), r, "pdf")
                elif ext == ".ipynb":
                    chunks += _split(_notebook_md(p), r, "notebook")
                elif ext == ".py":
                    chunks += [dict(d, file=r) for d in _py_docs(p)]
                elif fn in ("params.yaml", "dvc.yaml", "config.yaml", "config.yml"):
                    chunks.append({"file": r, "line": 1, "kind": "yaml", "text": open(p, encoding="utf-8", errors="ignore").read()[:MAX_CHUNK]})
            except Exception:
                continue
    return [Chunk(i, c["file"], c["line"], c["kind"], c["text"]) for i, c in enumerate(chunks)]


# ------------------------------------------------------------- retriever
def _tok(s: str) -> List[str]:
    return re.findall(r"[a-z0-9]+", s.lower())


class Retriever:
    """BM25 index over the corpus chunks."""

    def __init__(self, chunks: List[Chunk]):
        self.chunks = chunks
        self.bm25 = BM25Okapi([_tok(c.text) for c in chunks]) if chunks else None

    def search(self, query: str, k: int = 5) -> List[Dict]:
        if not self.bm25:
            return []
        scores = self.bm25.get_scores(_tok(query))
        idx = sorted(range(len(scores)), key=lambda i: -scores[i])[:k]
        return [dict(self.chunks[i].to_dict(), score=round(float(scores[i]), 3)) for i in idx if scores[i] > 0]


_RETRIEVERS: Dict[str, Retriever] = {}   # one corpus per repository


def get_retriever(repo_path: str) -> Retriever:
    if repo_path not in _RETRIEVERS:
        _RETRIEVERS[repo_path] = Retriever(build_corpus(repo_path))
    return _RETRIEVERS[repo_path]


def run_retrieval(spec, repo_path: str, top_k: int = 5) -> dict:
    """Retrieve the chunks of a "retrieval" field and return the field payload (used by the tool and by the baseline)."""
    hits = get_retriever(repo_path).search(spec.query + " " + " ".join(spec.keywords), top_k)
    return {"field": spec.id, "strategy": "retrieval", "status": "unverified", "value": None, "sources": hits, "note": ""}


# --------------------------------------------------------- LangChain tool
@tool("retrieve_evidence")
def retrieve_evidence(field_id: str, state: Annotated[dict, InjectedState]) -> str:
    """Retrieve the most relevant text chunks of the repository (README, docs, PDF, notebooks,
    docstrings) for a field with strategy 'retrieval'. Argument: field_id."""
    spec = BY_ID.get(field_id)
    if not spec or spec.strategy != "retrieval":
        return f"error: '{field_id}' is not a retrieval field"
    payload = run_retrieval(spec, state["repo_path"], state["config"].get("top_k", 5))
    RESULTS[(state["repo_path"], spec.id)] = payload            # full result for the Harvester
    hits = payload["sources"]
    return f"{spec.id}: {len(hits)} chunks retrieved (top bm25={hits[0]['score'] if hits else 0}) from {sorted({h['file'] for h in hits})}"


RETRIEVAL_TOOLS = [retrieve_evidence]
