# LLMAutodoc

Generates the **EU AI Act Data Documentation** (Art. 10–11, Annex IV) of an AI/ML project directly from its Git repository.

Every field of the document is filled only from evidence found in the repository and carries its sources. When the evidence is missing, the field is left empty and says why. **A field without evidence is declared as such, never invented.**

![Architecture](images/architecture.png)

The document has 40 fields, each with a fixed strategy: *tool* (18 fields — deterministic extractors, no model), *retrieval* (18 — retrieve → grade → generate → verify), *human* (4 — never filled by the system). The language model chooses which tools to call; a separate model judges the evidence before any text is written; a third re-reads the text against the same evidence and rejects what is not supported.

## Quick start

```bash
git clone https://github.com/Fabrizio250/LLMAutodoc.git
cd LLMAutodoc
pip install -r requirements.txt

export ANTHROPIC_API_KEY=sk-ant-...      # Windows: set ANTHROPIC_API_KEY=sk-ant-...

python main.py https://github.com/se4ai2122-cs-uniba/CT-COVID.git --out renderedDocs/ct-covid
```

The repository argument is a Git URL or a local path. Python 3.11+ and `git` are required.

### What you get

```
renderedDocs/ct-covid/
├── data.md       the Data Documentation, one section per template section
└── audit.json    for every field: strategy, status, value, sources, verdicts, and the configuration used
```

Each field ends in one of five states: `filled`, `partial`, `abstained` (evidence insufficient — reason recorded), `not_observable` (artefact missing from the repository), `human_required`.

## Configuration

Everything lives in `config.yaml`; the command line only overrides single values.

| what | key in `config.yaml` | flag |
|---|---|---|
| model that orchestrates and writes | `llm.model` | `--model` |
| model that judges the evidence | `llm.grader_model` | `--grader` |
| model that verifies the text | `llm.verifier_model` (empty = grader) | `--verifier` |
| chunks retrieved per field | `pipeline.top_k` | `--top-k` |
| output directory | `paths.outputs_dir` | `--out` |

Models outside Anthropic are written `<endpoint>:<model id>`, e.g. `gemini:gemini-3.5-flash-lite`; the endpoint is declared under `llm.endpoints` with its `base_url` and the **name** of the environment variable holding the key. Keys never go in the file.

```bash
# Claude writes, Gemini verifies
python main.py <repo> --verifier gemini:gemini-3.5-flash-lite
```

### Ablations

| flag | effect |
|---|---|
| `--no-grade` | no Grader: plain retrieve-and-generate, no abstention |
| `--no-verify` | no Verifier |
| `--infer-strategy` | the Orchestrator is not told which tool fits each field |
| `--routing declarative` | tools run in specification order, no LLM Orchestrator |
| `--dry-run` | no model at all: extractors and lexical heuristics only |

## Evaluating a run

A manual ground truth (`evaluation/groundtruth/<repo>.json`) labels each field as present, partial or absent in the repository and lists the expected terms. The evaluation is deterministic — no model judges the output.

```bash
python evaluation/evaluate.py renderedDocs/ct-covid/audit.json evaluation/groundtruth/ct-covid.json
```

Writes `evaluation.md` (report), `evaluation.csv` (one row per field) and `evaluation.json` next to `audit.json`. Metrics: coverage, fill precision, abstention precision, hallucination rate — overall and per strategy.

### Reproducing the thesis experiments

```bash
python run_experiments.py --only ct-covid --runs 2      # full, no-verify, infer-strategy, no-grade ×2, dry-run ×1
python run_experiments.py --summarize-only              # rebuild summary.csv from existing runs
```

Produces `renderedDocs/summary.csv` (metrics per run, mean and sd per variant) and `field_matrix.csv` (outcome of every field under every variant). The definitive runs of the thesis are committed under `renderedDocs/`; the cross-family runs (Claude/Gemini roles swapped) are launched by hand with `--model`, `--grader`, `--verifier` and evaluated with `evaluate.py`.

## Running elsewhere

**Container**

```bash
docker build -t llmautodoc .
docker run --rm -e ANTHROPIC_API_KEY -v "$PWD/renderedDocs:/app/renderedDocs" \
    llmautodoc https://github.com/se4ai2122-cs-uniba/CT-COVID.git --out renderedDocs/ct-covid
```

**GitHub Actions** — `examples/regulatory-docs.yml` goes into `.github/workflows/` of the repository to be documented. On every pull request it regenerates the document and commits it, with its audit trail, back to the branch. Needs an `ANTHROPIC_API_KEY` secret and this repository's name in `LLMAUTODOC_REPO`.

**As a library**

```python
from llmautodoc import build_graph, build_config
final = build_graph().invoke({"config": build_config("https://github.com/org/repo.git")})
```

## Repository layout

```
LLMAutodoc/
├── llmautodoc/                 the framework
│   ├── field_spec.py           the 40 fields with their strategy (tool | retrieval | human)
│   ├── agent.py                Orchestrator and Harvester
│   ├── tools/
│   │   ├── deterministic.py    18 extractors (git, DVC, LICENSE, dvc.yaml, code) — no model
│   │   └── retrieval.py        retrieve_evidence: closed repository corpus, BM25
│   ├── llm.py                  Grader, Generator, Verifier; model factory
│   ├── nodes.py                Setup, Compiler and the nodes wrapping llm.py
│   ├── graph.py                the edges (LangGraph)
│   ├── config.py               config.yaml → run configuration
│   └── templates/data.j2       Jinja2 template of the document
├── main.py                     one run
├── run_experiments.py          the experiment campaign → summary.csv, field_matrix.csv
├── config.yaml                 all parameters
├── evaluation/
│   ├── evaluate.py             per-field evaluation against the ground truth
│   └── groundtruth/            ct-covid.json
├── renderedDocs/               run outputs (the thesis runs are committed here)
├── examples/regulatory-docs.yml   GitHub Actions workflow for the documented repository
├── images/                     architecture figure and the script that draws it
├── docs/                       user guide, code reference, test report, thesis PDF
└── Dockerfile                  container image
```

## Thesis

*An Agentic AI Framework for Regulatory Documentation of AI-Based Medical Software* — Fabrizio Rosmarino, MSc in Computer Science, University of Bari, 2026. Supervisors: Giulio Mallardi, Filippo Lanubile. Full text: [`docs/Tesi_Rosmarino.pdf`](docs/Tesi_Rosmarino.pdf).
