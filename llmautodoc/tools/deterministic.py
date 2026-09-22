"""
Deterministic tools (strategy "tool").

Each extractor reads specific repository artefacts (git history, DVC files, LICENSE,
dvc.yaml, source code) and returns an Evidence: value + provenance. No LLM is involved.
If the artefact does not exist the value is None: an extractor never guesses.

The LangChain tools `extract_<field>` wrap these functions so the Orchestrator can call them.
"""

from __future__ import annotations
import os, re, json, subprocess, datetime, collections
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Callable, Annotated

from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState

from . import RESULTS, preview
from ..field_spec import fields_by_strategy

DATA_EXT = {
    "images": {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".dcm", ".nii", ".gz"},
    "tabular": {".csv", ".tsv", ".parquet", ".xlsx", ".xls", ".feather"},
    "text": {".txt", ".json", ".jsonl"},
    "audio": {".wav", ".mp3", ".flac"},
    "video": {".mp4", ".avi"},
    "arrays": {".npy", ".npz", ".h5", ".hdf5", ".pt", ".pkl"},
}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".dvc", ".venv", "venv", ".idea", ".vscode",
             ".llmautodoc"}   # the framework itself, when checked out inside the repository under CI

# A directory written by a previous run carries this marker. Such directories are excluded from
# the corpus and from the extractors: the evidence must come from the repository, never from what
# the system itself wrote the last time it ran.
OUTPUT_MARKER = ".llmautodoc-output"


def prune(root: str, dirs: List[str]) -> None:
    """In-place pruning of an os.walk directory list: service dirs and own previous outputs."""
    dirs[:] = [d for d in dirs
               if d not in SKIP_DIRS
               and not os.path.exists(os.path.join(root, d, OUTPUT_MARKER))]


@dataclass
class Evidence:
    """Result of an extractor: the value, where it was found, and a note if it was not found."""
    value: Any = None
    sources: List[Dict[str, str]] = field(default_factory=list)   # [{file, detail}]
    note: str = ""

    def to_dict(self):
        return asdict(self)


# ---------------------------------------------------------------- helpers
def _run(cmd: List[str], cwd: str) -> str:
    try:
        return subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True).stdout
    except Exception:
        return ""


def _read(path: str, limit: int = 200_000) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read(limit)
    except Exception:
        return ""


def _find_files(repo: str, names: List[str] = None, exts: set = None, max_depth: int = 6) -> List[str]:
    out, base = [], repo.rstrip(os.sep).count(os.sep)
    for root, dirs, files in os.walk(repo):
        prune(root, dirs)
        if root.count(os.sep) - base > max_depth:
            dirs[:] = []
            continue
        for fn in files:
            if names and fn.lower() in [n.lower() for n in names]:
                out.append(os.path.join(root, fn))
            elif exts and os.path.splitext(fn)[1].lower() in exts:
                out.append(os.path.join(root, fn))
    return out


def rel(repo: str, path: str) -> str:
    """Repository-relative path with forward slashes (used as provenance)."""
    return os.path.relpath(path, repo).replace(os.sep, "/")


def _readme(repo: str) -> Optional[str]:
    for fn in ("README.md", "README.rst", "README.txt", "README", "readme.md"):
        p = os.path.join(repo, fn)
        if os.path.exists(p):
            return p
    return None


def _git_authors(repo: str) -> List[Dict[str, Any]]:
    """Authors from git log, grouped by e-mail, most commits first."""
    counter: Dict[str, Dict[str, Any]] = {}
    for line in _run(["git", "log", "--format=%an|%ae"], repo).splitlines():
        if "|" not in line:
            continue
        name, email = line.split("|", 1)
        d = counter.setdefault(email.lower(), {"names": collections.Counter(), "email": email, "commits": 0})
        d["names"][name] += 1
        d["commits"] += 1
    out = []
    for d in counter.values():
        names = sorted(d["names"], key=lambda n: (" " not in n, -d["names"][n]))  # prefer "First Last"
        out.append({"name": names[0], "email": d["email"], "commits": d["commits"]})
    return sorted(out, key=lambda x: -x["commits"])


# ------------------------------------------------------------- extractors
def dataset_name(repo: str) -> Evidence:
    p = _readme(repo)
    if p:
        m = re.search(r"^#\s+([^\n\[]+)", _read(p), re.M)
        if m:
            return Evidence(m.group(1).strip(), [{"file": rel(repo, p), "detail": "first H1 title"}])
    origin = _run(["git", "config", "--get", "remote.origin.url"], repo).strip()
    if origin:
        return Evidence(origin.rstrip("/").split("/")[-1].replace(".git", ""), [{"file": ".git/config", "detail": "remote.origin.url"}])
    return Evidence(None, note="no README title and no git remote")


def relevant_links(repo: str) -> Evidence:
    links, sources = [], []
    origin = _run(["git", "config", "--get", "remote.origin.url"], repo).strip()
    if origin:
        links.append({"label": "GitHub Repository", "url": origin})
        sources.append({"file": ".git/config", "detail": "remote.origin.url"})
    p = _readme(repo)
    if p:
        txt = _read(p)
        for m in re.finditer(r"\[([^\]]{2,60})\]\((https?://[^\s)]+)\)", txt):
            if not any(k in m.group(2) for k in ("badge", "shields.io", ".svg")):
                links.append({"label": m.group(1), "url": m.group(2)})
        for m in re.finditer(r"(?<!\()\bhttps?://[^\s)\]>\"']+", txt):
            url = m.group(0).rstrip(".,")
            if any(k in url for k in ("badge", "shields.io", ".svg", "localhost", "127.0.0.1")) or any(l["url"] == url for l in links):
                continue
            links.append({"label": url.split("/")[2], "url": url})
        if len(links) > (1 if origin else 0):
            sources.append({"file": rel(repo, p), "detail": "URLs in README"})
    for d in _find_files(repo, exts={".pdf"}):
        links.append({"label": "Report / documentation (repo file)", "url": rel(repo, d)})
        sources.append({"file": rel(repo, d), "detail": "PDF document in repository"})
    return Evidence(links or None, sources, "" if links else "no observable links")


def developers(repo: str) -> Evidence:
    authors = _git_authors(repo)
    srcs = [{"file": ".git (git log)", "detail": f"{len(authors)} distinct authors by e-mail"}]
    for fn in ("AUTHORS", "AUTHORS.md", "CONTRIBUTORS.md", "CITATION.cff"):
        if os.path.exists(os.path.join(repo, fn)):
            srcs.append({"file": fn, "detail": "authors file present"})
    return Evidence(authors or None, srcs if authors else [], "" if authors else "no git history")


def owners(repo: str) -> Evidence:
    """Owner proxy: organisation of the git remote, CODEOWNERS, top contributor."""
    origin = _run(["git", "config", "--get", "remote.origin.url"], repo).strip()
    val, srcs = {}, []
    m = re.search(r"[:/]([^/:]+)/([^/]+?)(\.git)?$", origin) if origin else None
    if m:
        val["organization"] = m.group(1)
        srcs.append({"file": ".git/config", "detail": "remote organisation"})
    for fn in ("CODEOWNERS", ".github/CODEOWNERS", "docs/CODEOWNERS"):
        p = os.path.join(repo, fn)
        if os.path.exists(p):
            val["codeowners"] = _read(p).strip()
            srcs.append({"file": fn, "detail": "CODEOWNERS"})
    authors = _git_authors(repo)
    if authors:
        val["main_contributor"] = authors[0]
        srcs.append({"file": ".git (git log)", "detail": "author with most commits"})
    return Evidence(val or None, srcs, "" if val else "no observable owner")


def status_date(repo: str) -> Evidence:
    d = _run(["git", "log", "-1", "--format=%cs"], repo).strip()
    return Evidence(d or None, [{"file": ".git (git log)", "detail": "last commit date"}] if d else [])


def dataset_status(repo: str) -> Evidence:
    """Status inferred from repository activity with an explicit, verifiable rule."""
    last = _run(["git", "log", "-1", "--format=%cs"], repo).strip()
    if not last:
        return Evidence(None, note="no git history")
    days = (datetime.date.today() - datetime.date.fromisoformat(last)).days
    n = len(_run(["git", "log", "--format=%h"], repo).splitlines())
    if "archived" in _read(_readme(repo) or "").lower():
        status = "Deprecated"
    elif days > 730:
        status = "Limited Maintenance / Deprecated (no commits in >2 years)"
    elif days > 180:
        status = "Limited Maintenance"
    else:
        status = "Actively Maintained"
    return Evidence({"status": status, "last_commit": last, "days_since_last_commit": days, "commits": n},
                    [{"file": ".git (git log)", "detail": "rule: >180 days -> Limited, >730 days -> Deprecated"}])


def version_details(repo: str) -> Evidence:
    tags = _run(["git", "tag", "--sort=-creatordate"], repo).split()
    head = _run(["git", "rev-parse", "--short", "HEAD"], repo).strip()
    val, srcs = {}, []
    if tags:
        val["latest_tag"], val["tags"] = tags[0], tags[:10]
        srcs.append({"file": ".git (tags)", "detail": "git tag"})
    if head:
        val["head_commit"] = head
        srcs.append({"file": ".git", "detail": "HEAD"})
    for fn in ("VERSION", "version.txt", "pyproject.toml", "setup.py", "package.json"):
        p = os.path.join(repo, fn)
        if os.path.exists(p):
            m = re.search(r"version\s*[=:]\s*[\"']?([\d][\w.\-]*)", _read(p), re.I)
            if m:
                val["declared_version"] = m.group(1)
                srcs.append({"file": fn, "detail": "version field"})
                break
    for d in _find_files(repo, exts={".dvc"}):
        m = re.search(r"md5:\s*([0-9a-f]+)", _read(d))
        if m:
            val.setdefault("data_versions", {})[rel(repo, d)] = m.group(1)
            srcs.append({"file": rel(repo, d), "detail": "DVC data hash"})
    return Evidence(val or None, srcs, "" if val else "no observable version")


def data_versioning(repo: str) -> Evidence:
    tools, srcs = [], []
    dvc_files = _find_files(repo, exts={".dvc"})
    if os.path.exists(os.path.join(repo, "dvc.yaml")) or os.path.isdir(os.path.join(repo, ".dvc")) or dvc_files:
        tools.append("DVC (Data Version Control)")
        for p in ("dvc.yaml", "dvc.lock"):
            if os.path.exists(os.path.join(repo, p)):
                srcs.append({"file": p, "detail": "DVC pipeline"})
        srcs += [{"file": rel(repo, f), "detail": "DVC pointer"} for f in dvc_files]
        m = re.search(r"url\s*=\s*(\S+)", _read(os.path.join(repo, ".dvc", "config")))
        if m:
            tools.append(f"DVC remote: {m.group(1)}")
            srcs.append({"file": ".dvc/config", "detail": "remote"})
    if "lfs" in _read(os.path.join(repo, ".gitattributes")):
        tools.append("Git LFS")
        srcs.append({"file": ".gitattributes", "detail": "filter=lfs"})
    if _find_files(repo, names=["MLproject", "mlflow.yml"]):
        tools.append("MLflow")
    return Evidence(tools or None, srcs, "" if tools else "no observable data versioning")


def known_models(repo: str) -> Evidence:
    val, srcs = {}, []
    outs = re.findall(r"-\s*(models?/[^\s]+)", _read(os.path.join(repo, "dvc.yaml")))
    if outs:
        val["model_artifacts"] = sorted(set(outs))
        srcs.append({"file": "dvc.yaml", "detail": "stage outputs"})
    files = _find_files(repo, exts={".pt", ".pth", ".h5", ".onnx", ".pkl", ".joblib", ".ckpt"})
    if files:
        val["model_files"] = [rel(repo, m) for m in files][:20]
        srcs.append({"file": "models/", "detail": "model files in repository"})
    for fn in _find_files(repo, exts={".py"}):
        for cls in re.findall(r"class\s+(\w*(?:Net|Model|Classifier|CNN|ResNet)\w*)\s*\(", _read(fn, 50_000)):
            val.setdefault("model_classes", []).append(f"{cls} ({rel(repo, fn)})")
    if "model_classes" in val:
        srcs.append({"file": "src/", "detail": "model classes in code"})
    return Evidence(val or None, srcs, "" if val else "no observable model")


def data_types(repo: str) -> Evidence:
    counts = collections.Counter()
    data_dirs = [d for d in ("data", "dataset", "datasets", "raw") if os.path.isdir(os.path.join(repo, d))]
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        if data_dirs and not any(root.startswith(os.path.join(repo, d)) for d in data_dirs):
            continue
        for fn in files:
            ext = os.path.splitext(fn)[1].lower()
            for kind, exts in DATA_EXT.items():
                if ext in exts:
                    counts[kind] += 1
    val, srcs = {}, []
    if counts:
        val["by_extension"] = dict(counts)
        srcs.append({"file": ", ".join(data_dirs) or ".", "detail": "file extensions in data directories"})
    for fn in _find_files(repo, exts={".py"}):           # data kept outside the repo (DVC): infer from code
        t = _read(fn, 50_000)
        if re.search(r"\b(PIL|Image\.open|cv2|imread|nibabel|pydicom|torchvision)\b", t):
            val["inferred_from_code"] = "images"; srcs.append({"file": rel(repo, fn), "detail": "image I/O libraries in code"}); break
        if re.search(r"\b(read_csv|read_parquet|pandas)\b", t):
            val["inferred_from_code"] = "tabular"; srcs.append({"file": rel(repo, fn), "detail": "pandas in code"}); break
    dvc = [rel(repo, d) for d in _find_files(repo, exts={".dvc"})]
    if dvc:
        val["dvc_tracked_data"] = dvc
    return Evidence(val or None, srcs, "" if val else "no observable data files")


def dataset_size(repo: str) -> Evidence:
    val, srcs = {}, []
    for d in _find_files(repo, exts={".dvc"}):
        txt = _read(d)
        n, s = re.search(r"nfiles:\s*(\d+)", txt), re.search(r"size:\s*(\d+)", txt)
        if n or s:
            val[rel(repo, d)] = {"nfiles": int(n.group(1)) if n else None, "bytes": int(s.group(1)) if s else None}
            srcs.append({"file": rel(repo, d), "detail": "nfiles/size in DVC pointer"})
    for m in re.finditer(r"path:\s*(data\S*)\s*\n(?:.*\n){0,3}?\s*size:\s*(\d+)\s*\n\s*nfiles:\s*(\d+)", _read(os.path.join(repo, "dvc.lock"))):
        val[m.group(1)] = {"nfiles": int(m.group(3)), "bytes": int(m.group(2))}
        srcs.append({"file": "dvc.lock", "detail": f"size/nfiles of {m.group(1)}"})
    n = total = 0
    for d in ("data", "dataset", "datasets"):
        for root, _, files in os.walk(os.path.join(repo, d)):
            for fn in files:
                if not fn.endswith(".dvc"):
                    n += 1; total += os.path.getsize(os.path.join(root, fn))
    if n:
        val["files_in_repo"] = {"nfiles": n, "bytes": total}
        srcs.append({"file": "data/", "detail": "file count"})
    return Evidence(val or None, srcs, "" if val else "size not observable (data not in repository)")


def preprocessing_pipeline(repo: str) -> Evidence:
    val, srcs = {}, []
    stages = re.findall(r"^\s{2}(\w[\w\-]*):\s*\n\s+cmd:\s*(.+)", _read(os.path.join(repo, "dvc.yaml")), re.M)
    if stages:
        val["dvc_stages"] = [{"stage": s, "cmd": c.strip()} for s, c in stages]
        srcs.append({"file": "dvc.yaml", "detail": "pipeline stages"})
    scripts = [f for f in _find_files(repo, exts={".py"}) if re.search(r"preprocess|prepare|clean|transform|feature", os.path.basename(f), re.I)]
    if scripts:
        val["preprocessing_scripts"] = [rel(repo, s) for s in scripts]
        srcs += [{"file": rel(repo, s), "detail": "pre-processing script"} for s in scripts]
        ops = set()
        patterns = {"resize": r"resize", "normalize": r"normali[sz]|/\s*255", "crop": r"crop", "grayscale": r"gray|grey|convert\(['\"]L",
                    "augmentation": r"flip|rotat|augment", "split": r"train_test_split|split", "filter/clean": r"drop|filter|remove|isnan|dropna"}
        for s in scripts:
            t = _read(s, 100_000)
            ops |= {op for op, pat in patterns.items() if re.search(pat, t, re.I)}
        if ops:
            val["operations_detected_in_code"] = sorted(ops)
    return Evidence(val or None, srcs, "" if val else "no observable pre-processing pipeline")


def data_validation(repo: str) -> Evidence:
    val, srcs = [], []
    ge = _find_files(repo, names=["great_expectations.yml"]) or [d for d in _find_files(repo, exts={".json"}) if "expectations" in d]
    if ge:
        val.append("Great Expectations (expectation suites / checkpoints)")
        srcs += [{"file": rel(repo, g), "detail": "Great Expectations configuration"} for g in ge[:5]]
    req = " ".join(_read(f) for f in _find_files(repo, names=["requirements.txt", "requirements_dev.txt", "pyproject.toml"]))
    for lib in ("great_expectations", "great-expectations", "pandera", "deepchecks", "evidently"):
        if lib in req and not any(lib.split("_")[0].split("-")[0] in v.lower() for v in val):
            val.append(f"{lib} (declared in requirements)")
            srcs.append({"file": "requirements*.txt", "detail": lib})
    tests = [t for t in _find_files(repo, exts={".py"}) if "test" in rel(repo, t).lower() and re.search(r"data|dataset", os.path.basename(t), re.I)]
    if tests:
        val.append("Automated data tests: " + ", ".join(rel(repo, t) for t in tests[:5]))
        srcs += [{"file": rel(repo, t), "detail": "data tests"} for t in tests[:5]]
    return Evidence(val or None, srcs, "" if val else "no observable data validation")


def distribution(repo: str) -> Evidence:
    val, srcs = {}, []
    m = re.search(r"url\s*=\s*(\S+)", _read(os.path.join(repo, ".dvc", "config")))
    if m:
        val["dvc_remote"] = m.group(1)
        srcs.append({"file": ".dvc/config", "detail": "DVC remote"})
    if _find_files(repo, exts={".dvc"}):
        val["mechanism"] = "data distributed through DVC pointers (not included in the git repository)"
        srcs.append({"file": "*.dvc", "detail": "pointer"})
    elif os.path.isdir(os.path.join(repo, "data")):
        val["mechanism"] = "data included in the git repository"
        srcs.append({"file": "data/", "detail": "directory"})
    p = _readme(repo)
    if p:
        for m in re.finditer(r"https?://(?:www\.)?(kaggle\.com|huggingface\.co|zenodo\.org|drive\.google\.com|physionet\.org)[^\s)]*", _read(p)):
            val.setdefault("download_links", []).append(m.group(0))
            srcs.append({"file": rel(repo, p), "detail": "download link"})
    return Evidence(val or None, srcs, "" if val else "no observable distribution mechanism")


def license(repo: str) -> Evidence:
    names = [(r"MIT License", "MIT"), (r"Apache License,?\s*Version 2", "Apache-2.0"), (r"GNU GENERAL PUBLIC LICENSE\s*Version 3", "GPL-3.0"),
             (r"GNU GENERAL PUBLIC LICENSE\s*Version 2", "GPL-2.0"), (r"BSD 3-Clause|Redistribution and use in source and binary forms", "BSD-3-Clause"),
             (r"Creative Commons", "Creative Commons"), (r"GNU LESSER", "LGPL"), (r"Mozilla Public License", "MPL-2.0")]
    for fn in ("LICENSE", "LICENSE.md", "LICENSE.txt", "LICENCE", "COPYING"):
        p = os.path.join(repo, fn)
        if os.path.exists(p):
            txt = _read(p, 4000)
            name = next((nm for pat, nm in names if re.search(pat, txt, re.I)), "unknown")
            m = re.search(r"Copyright\s*(?:\(c\)|©)?\s*([^\n]+)", txt, re.I)
            return Evidence({"license": name, "copyright": m.group(1).strip() if m else None,
                             "scope_note": "licence of the repository (code); the DATA licence may differ and is not observable unless declared"},
                            [{"file": fn, "detail": "licence file"}])
    return Evidence(None, note="no LICENSE file")


def doc_authors(repo: str) -> Evidence:
    return Evidence({"generated_by": "LLMAutodoc (agentic documentation framework)",
                     "repository_contributors": [a["name"] for a in _git_authors(repo)[:5]]},
                    [{"file": ".git (git log)", "detail": "contributors"}])


def doc_version(repo: str) -> Evidence:
    head = _run(["git", "rev-parse", "--short", "HEAD"], repo).strip()
    today = datetime.date.today().isoformat()
    return Evidence({"document_version": f"auto-{today}-{head or 'nohead'}", "generated_on": today, "repo_commit": head},
                    [{"file": ".git", "detail": "HEAD"}])


def data_monitoring(repo: str) -> Evidence:
    val, srcs = [], []
    for fn, label in (("prometheus.yml", "Prometheus"), ("alert_rules.yml", "Prometheus alert rules"), ("grafana.json", "Grafana dashboard"), ("alertmanager.yml", "Alertmanager")):
        if _find_files(repo, names=[fn]):
            val.append(label)
            srcs.append({"file": fn, "detail": "monitoring configuration"})
    for f in _find_files(repo, exts={".py"}):
        t = _read(f, 50_000)
        if re.search(r"evidently|whylogs|drift", t, re.I):
            val.append(f"data drift monitoring in code ({rel(repo, f)})"); srcs.append({"file": rel(repo, f), "detail": "data monitoring"}); break
        if re.search(r"prometheus_client|Instrumentator", t):
            val.append(f"Prometheus metrics exposed by the service ({rel(repo, f)})"); srcs.append({"file": rel(repo, f), "detail": "prometheus_client"}); break
    if val and not any("drift" in v for v in val):
        val.append("NOTE: SERVICE monitoring is observable, not DATA quality/drift monitoring")
    return Evidence(val or None, srcs, "" if val else "no observable monitoring")


EXTRACTORS: Dict[str, Callable[[str], Evidence]] = {
    "dataset_name": dataset_name, "relevant_links": relevant_links, "developers": developers, "owners": owners,
    "status_date": status_date, "dataset_status": dataset_status, "version_details": version_details,
    "data_versioning": data_versioning, "known_models": known_models, "data_types": data_types,
    "dataset_size": dataset_size, "preprocessing_pipeline": preprocessing_pipeline, "data_validation": data_validation,
    "distribution": distribution, "license": license, "doc_authors": doc_authors, "doc_version": doc_version,
    "data_monitoring": data_monitoring,
}


# ------------------------------------------------------- LangChain tools
def run_extractor(spec, repo_path: str) -> dict:
    """Run the extractor of a "tool" field and return the field payload (used by tools and by the baseline)."""
    ev = EXTRACTORS[spec.tool](repo_path)
    return {"field": spec.id, "strategy": "tool", "status": "filled" if ev.value is not None else "not_observable",
            "value": ev.value, "sources": ev.sources, "note": ev.note}


def _make_tool(spec):
    desc = f"Field '{spec.id}' ({spec.label}, section {spec.section}): deterministic extractor '{spec.tool}'. No arguments."

    @tool(f"extract_{spec.id}", description=desc)
    def _t(state: Annotated[dict, InjectedState]) -> str:
        payload = run_extractor(spec, state["repo_path"])
        RESULTS[(state["repo_path"], spec.id)] = payload           # full result for the Harvester
        return f"{spec.id}: {payload['status']}. " + (preview(payload["value"]) if payload["value"] is not None else payload["note"])

    return _t


DETERMINISTIC_TOOLS = [_make_tool(s) for s in fields_by_strategy("tool")]
