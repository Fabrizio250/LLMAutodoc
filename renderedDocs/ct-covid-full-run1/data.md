# Data Documentation — CT-COVID

> EU AI Act [Article 10](https://artificialintelligenceact.eu/article/10/) · [Article 11](https://artificialintelligenceact.eu/article/11/) · [Annex IV](https://artificialintelligenceact.eu/annex/4/) §1, §2(d)
>
> Generated on 2026-09-10 from `https://github.com/se4ai2122-cs-uniba/CT-COVID.git` by LLMAutodoc (routing: `agentic`).
> Fields: 24 filled, 9 abstained, 3 partial, 4 human_required.
> Closed-scope corpus: 69 chunks from 13 files.
>
> **Reading guide.** Every field states *how* it was produced. `tool` = deterministic extraction from repository artefacts (no LLM involved in the value); `retrieval` = evidence retrieved from repository text, graded, and rewritten by an LLM using only that evidence; `human` = judgement that cannot be derived from artefacts. An **ABSTAINED** field means the repository contains no sufficient evidence — it must not be read as "not applicable".

**Dataset Owner**: - **organization**: se4ai2122-cs-uniba
- **main_contributor**: {"name": "Lorenzo Loconte", "email": "lorenzoloconte@outlook.it", "commits": 74}
**Document Version**: auto-2026-09-10-3f05400
**Reviewers**: _requires human input_

## Overview

### Dataset name
<sub>strategy: `tool` · status: **✅ filled**</sub>

CT-COVID

<details><summary>Evidence (1)</summary>

- `README.md` — first H1 title</details>


### Dataset Description
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

The COVIDx-CT dataset consists of CT images (individual slices) annotated with one of three labels: normal, non-COVID-19 pneumonia, and COVID-19 pneumonia [2]. It contains 143,778 training, 25,486 validation, and 25,658 test examples [2]. Bounding box coordinates for lung regions are also provided for each example [0]. The three classes are highly unbalanced [2]. The dataset is freely available on Kaggle [0].

A derived dataset, COVIDx-SeqCT, is composed of sequences of exactly 16 CT slices extracted uniformly from CT scans; scans with fewer than 16 slices are discarded [0]. It contains 2,390 training, 430 validation, and 408 test examples, each annotated with the same three labels [0][1].

The datasets serve two tasks: single CT image classification and end-to-end CT scan classification using sequences of images [2]. Attention mechanisms are incorporated to provide prediction explanations, addressing interpretability requirements in the medical domain [2].

<details><summary>Evidence (3)</summary>

- `docs/ct-report.pdf:40` (pdf, bm25=19.345)- `docs/ct-report.pdf:56` (pdf, bm25=16.55)- `docs/ct-report.pdf:25` (pdf, bm25=12.569)</details>


### Status Date
<sub>strategy: `tool` · status: **✅ filled**</sub>

2022-01-12

<details><summary>Evidence (1)</summary>

- `.git (git log)` — last commit date</details>


### Status
<sub>strategy: `tool` · status: **✅ filled**</sub>

- **status**: Limited Maintenance / Deprecated (no commits in >2 years)
- **last_commit**: 2022-01-12
- **days_since_last_commit**: 1702
- **commits**: 156

<details><summary>Evidence (1)</summary>

- `.git (git log)` — rule: >180 days -> Limited, >730 days -> Deprecated</details>


### Relevant Links
<sub>strategy: `tool` · status: **✅ filled**</sub>

- label: GitHub Repository, url: https://github.com/se4ai2122-cs-uniba/CT-COVID.git
- label: dockerhub, url: https://hub.docker.com/r/peppocola/ct-covid
- label: Report / documentation (repo file), url: docs/ct-report.pdf

<details><summary>Evidence (3)</summary>

- `.git/config` — remote.origin.url- `README.md` — URLs in README- `docs/ct-report.pdf` — PDF document in repository</details>


### Developers
<sub>strategy: `tool` · status: **✅ filled**</sub>

- name: Lorenzo Loconte, email: lorenzoloconte@outlook.it, commits: 74
- name: Giuseppe Colavito, email: giuseppecolavito999@gmail.com, commits: 46
- name: itsfrank98, email: frybene@libero.it, commits: 20
- name: Francesco Benedetti, email: 45521145+itsfrank98@users.noreply.github.com, commits: 10
- name: Daniela Grassi, email: daniela.grassi.98@gmail.com, commits: 5
- name: Daniela Grassi, email: 48294368+DanielaGrassi@users.noreply.github.com, commits: 1

<details><summary>Evidence (1)</summary>

- `.git (git log)` — 6 distinct authors by e-mail</details>


### Owner
<sub>strategy: `tool` · status: **✅ filled**</sub>

- **organization**: se4ai2122-cs-uniba
- **main_contributor**: {"name": "Lorenzo Loconte", "email": "lorenzoloconte@outlook.it", "commits": 74}

<details><summary>Evidence (2)</summary>

- `.git/config` — remote organisation- `.git (git log)` — author with most commits</details>


### Deployer instructions of use
<sub>strategy: `retrieval` · status: **⛔ ABSTAINED — no evidence in repository**</sub>

_No sufficient evidence in the repository: The chunks contain technical implementation details (installation requirements, model architecture, attention mechanisms) but do not provide instructions or restrictions for deployers using the data._

<details><summary>Evidence (5)</summary>

- `README.md:40` (markdown, bm25=17.525)- `docs/ct-report.pdf:528` (pdf, bm25=15.783)- `docs/ct-report.pdf:70` (pdf, bm25=12.061)- `docs/ct-report.pdf:137` (pdf, bm25=12.02)- `docs/ct-report.pdf:180` (pdf, bm25=11.19)</details>


### Version Details
<sub>strategy: `tool` · status: **✅ filled**</sub>

- **head_commit**: 3f05400
- **data_versions**: {"data/raw.dvc": "79cb3cab45b888c9b29e52f7a1bb1415"}

<details><summary>Evidence (2)</summary>

- `.git` — HEAD- `data/raw.dvc` — DVC data hash</details>


## Data Versioning

### Data Version Control Tools
<sub>strategy: `tool` · status: **✅ filled**</sub>

- DVC (Data Version Control)
- DVC remote: gdrive://1n6fB1AHEiQ0x7m3Y0mlSmihLIYo583uf

<details><summary>Evidence (4)</summary>

- `dvc.yaml` — DVC pipeline- `dvc.lock` — DVC pipeline- `data/raw.dvc` — DVC pointer- `.dvc/config` — remote</details>


### Maintenance of Metadata and Schema Versioning
<sub>strategy: `retrieval` · status: **⛔ ABSTAINED — no evidence in repository**</sub>

_No sufficient evidence in the repository: None of the chunks contain information about how data metadata and schema are maintained and versioned; they only reference validation procedures, loss calculations, and Great Expectations checkpoints without addressing metadata or schema versioning practices._

<details><summary>Evidence (5)</summary>

- `src/covidx/utils/train.py:122` (comment, bm25=8.437)- `src/covidx/utils/torch.py:43` (docstring, bm25=6.143)- `README.md:96` (markdown, bm25=6.077)- `src/covidx/utils/train.py:148` (comment, bm25=5.969)- `src/covidx/utils/torch.py:6` (docstring, bm25=5.7)</details>


## Known Usages

### Model(s)
<sub>strategy: `tool` · status: **✅ filled**</sub>

- **model_artifacts**: ["models/ct_net.pt"]
- **model_classes**: ["CTNet (src/covidx/ct/models.py)"]

<details><summary>Evidence (2)</summary>

- `dvc.yaml` — stage outputs- `src/` — model classes in code</details>


### Application(s)
<sub>strategy: `retrieval` · status: **🟡 partial evidence**</sub>

A REST API accessible on port 5000 exposes a `/predict` endpoint that accepts an image and its bounding box coordinates to return predictions [1][2][3]. A frontend application consumes this API [0]. The `/predict` endpoint is called via HTTP POST, passing the image file and bounding box parameters (`xmin`, `ymin`, `xmax`, `ymax`) [3]. Additional endpoints include `/models` for listing available models and `/docs` for API documentation [2].

<details><summary>Evidence (4)</summary>

- `README.md:59` (markdown, bm25=15.244)- `README.md:53` (markdown, bm25=12.209)- `README.md:5` (markdown, bm25=11.517)- `README.md:13` (markdown, bm25=10.135)</details>


## Dataset Characteristics

### Data Types
<sub>strategy: `tool` · status: **✅ filled**</sub>

- **inferred_from_code**: images
- **dvc_tracked_data**: ["data/raw.dvc"]

<details><summary>Evidence (1)</summary>

- `src/api.py` — image I/O libraries in code</details>


### Size
<sub>strategy: `tool` · status: **✅ filled**</sub>

- **data/raw.dvc**: {"nfiles": 39079, "bytes": 6259568533}
- **data/raw**: {"nfiles": 39079, "bytes": 6259568533}
- **data/ct**: {"nfiles": 39079, "bytes": 1209139393}
- **files_in_repo**: {"nfiles": 1, "bytes": 11}

<details><summary>Evidence (6)</summary>

- `data/raw.dvc` — nfiles/size in DVC pointer- `dvc.lock` — size/nfiles of data/raw- `dvc.lock` — size/nfiles of data/ct- `dvc.lock` — size/nfiles of data/ct- `dvc.lock` — size/nfiles of data/ct- `data/` — file count</details>


### Primary Use Case(s)
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

The dataset was built for multi-class classification of lung CT images into three categories: normal, pneumonia, and COVID-19 [0]. The primary use case is screening CT images to determine whether a patient has a COVID-19 infection or non-COVID-19 pneumonia [0]. The task is framed as a deep learning classification problem, with emphasis on minimizing false-negatives, as undetected infected patients pose health risks and may contribute to infection spreading [0].

<details><summary>Evidence (1)</summary>

- `docs/ct-report.pdf:1` (pdf, bm25=16.356)</details>


## Data Origin and Source

### Source(s)
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

The dataset (COVIDx-CT) is a publicly available dataset hosted on Kaggle [0]. A derived dataset, COVIDx-SeqCT, is obtained from the original COVIDx-CT dataset [0]. No URL or direct link is documented in the repository. The specific data collection method, institutional origin, or partner information is not documented in the repository.

<details><summary>Evidence (1)</summary>

- `docs/ct-report.pdf:40` (pdf, bm25=28.459)</details>


## Provenance

### Collection Method(s)
<sub>strategy: `retrieval` · status: **⛔ ABSTAINED — no evidence in repository**</sub>

_No sufficient evidence in the repository: The chunks describe data processing pipelines, training procedures, and file paths, but contain no information about how the original data was collected (e.g., source, acquisition method, sampling strategy)._

<details><summary>Evidence (5)</summary>

- `src/covidx/ct/dataset.py:78` (comment, bm25=7.102)- `src/covidx/utils/train.py:86` (comment, bm25=6.083)- `src/covidx/utils/train.py:122` (comment, bm25=6.083)- `dvc.yaml:1` (yaml, bm25=5.992)- `params.yaml:1` (yaml, bm25=5.983)</details>


### Dates of Collection
<sub>strategy: `retrieval` · status: **⛔ ABSTAINED — no evidence in repository**</sub>

_No sufficient evidence in the repository: None of the chunks contain information about collection dates or time periods (YYYY-MM – YYYY-MM format) for the dataset; they only describe technical methods, data augmentation, and model architectures._

<details><summary>Evidence (5)</summary>

- `docs/ct-report.pdf:155` (pdf, bm25=9.03)- `docs/ct-report.pdf:288` (pdf, bm25=7.889)- `docs/ct-report.pdf:379` (pdf, bm25=7.386)- `docs/ct-report.pdf:233` (pdf, bm25=6.691)- `docs/ct-report.pdf:160` (pdf, bm25=6.629)</details>


### Collection Cadence
<sub>strategy: `retrieval` · status: **⛔ ABSTAINED — no evidence in repository**</sub>

_No sufficient evidence in the repository: None of the chunks contain information about collection cadence (Static/Streamed/Dynamic) for training data provenance as required by EU AI Act Article 10._

<details><summary>Evidence (5)</summary>

- `docs/ct-report.pdf:443` (pdf, bm25=4.612)- `dvc.yaml:1` (yaml, bm25=2.996)- `params.yaml:1` (yaml, bm25=2.992)- `src/covidx/ct/dataset.py:78` (comment, bm25=2.855)- `src/preprocessing.py:7` (comment, bm25=2.774)</details>


## Data Pre-Processing

### Pre-processing pipeline (observed)
<sub>strategy: `tool` · status: **✅ filled**</sub>

- **dvc_stages**: [{"stage": "data-ct", "cmd": "python src/preprocessing.py --size 224 224 data/raw data/ct"}, {"stage": "train", "cmd": "python src/experiments.py"}, {"stage": "evaluate", "cmd": "python src/evaluate.py"}]
- **preprocessing_scripts**: ["src/preprocessing.py"]
- **operations_detected_in_code**: ["crop", "resize", "split"]

<details><summary>Evidence (2)</summary>

- `dvc.yaml` — pipeline stages- `src/preprocessing.py` — pre-processing script</details>


### Data Cleaning
<sub>strategy: `retrieval` · status: **🟡 partial evidence**</sub>

Raw CT images are resized to 224×224 pixels via `src/preprocessing.py`, taking input from `data/raw` and outputting cleaned data to `data/ct` [0]. Data augmentation is applied to training data during dataset instantiation [1]. No further data cleaning operations (e.g., denoising, normalization, artifact removal, duplicate handling) are documented in the repository.

<details><summary>Evidence (2)</summary>

- `dvc.yaml:1` (yaml, bm25=2.996)- `src/covidx/ct/dataset.py:78` (comment, bm25=2.855)</details>


### Data Transformation
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

Input images are preprocessed using Crop followed by Resize with bicubic interpolation [0]. Images are then converted to tensors, normalized, moved to the target device, and unsqueezed along the batch dimension [1]. Data augmentation is applied using random horizontal and vertical flip, Gaussian blur with kernel size 7 and standard deviation sampled uniformly from [0.05, 2.0], random affine transformations including scaling (scale ∈ [0.9, 1.1]), rotation (degrees ∈ [−30, 30]), translation (translation percentages ∈ [0.0, 0.1]), and random shear augmentation on the x-axis with rotation sampled uniformly from [−20, 20] [2].

<details><summary>Evidence (3)</summary>

- `src/api.py:201` (comment, bm25=19.021)- `src/api.py:168` (comment, bm25=5.83)- `docs/ct-report.pdf:288` (pdf, bm25=4.531)</details>


### Feature Engineering
<sub>strategy: `retrieval` · status: **⛔ ABSTAINED — no evidence in repository**</sub>

_No sufficient evidence in the repository: All chunks describe model-internal feature extraction and attention mechanisms (CNN layers, RNN hidden states, attention computations) rather than derived variables or extracted features OF THE INPUT DATA during pre-processing._

<details><summary>Evidence (5)</summary>

- `docs/ct-report.pdf:160` (pdf, bm25=12.755)- `src/covidx/ct/models.py:67` (comment, bm25=11.236)- `src/covidx/ct/models.py:60` (comment, bm25=11.023)- `docs/ct-report.pdf:115` (pdf, bm25=7.726)- `docs/ct-report.pdf:180` (pdf, bm25=7.3)</details>


### Data Augmentation
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

Random horizontal and vertical flip [0]; Gaussian blur with kernel size 7 and standard deviation sampled uniformly from [0.05, 2.0] [0]; random affine transformations including random scaling with scale sampled uniformly from [0.9, 1.1], random rotation with degrees sampled uniformly from [−30, 30], and random translation with translation percentages sampled uniformly from [0.0, 0.1] [0]; random shear augmentation on the x-axis with rotation sampled uniformly from [−20, 20] [0].

<details><summary>Evidence (1)</summary>

- `docs/ct-report.pdf:288` (pdf, bm25=13.594)</details>


## Data Annotation and Labeling

### Annotation process
<sub>strategy: `retrieval` · status: **🟡 partial evidence**</sub>

Each CT image (slice) is annotated with one of three labels: normal, pneumonia (non-COVID-19), or covid19 [0]. All CT slices belonging to a single CT scan share the same label, assigned by an expert evaluating the patient's health state considering all images in the sequence [2]. Annotations apply at both the image level and the scan/sequence level [0][1]. The annotators, the annotation procedure, and the specific guidelines followed are not documented in the repository.

<details><summary>Evidence (3)</summary>

- `docs/ct-report.pdf:25` (pdf, bm25=8.994)- `docs/ct-report.pdf:56` (pdf, bm25=6.12)- `docs/ct-report.pdf:218` (pdf, bm25=5.505)</details>


## Validation Types

### Validation method(s)
<sub>strategy: `tool` · status: **✅ filled**</sub>

- Great Expectations (expectation suites / checkpoints)

<details><summary>Evidence (1)</summary>

- `tests/great_expectations/great_expectations.yml` — Great Expectations configuration</details>


## Sampling Methods

### Sampling / split
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

COVIDx-CT dataset is split into train (143,778 examples: 35,996 Normal, 25,496 Pneumonia, 82,286 COVID-19), validation (25,486 examples: 11,842 Normal, 7,400 Pneumonia, 6,244 COVID-19), and test (25,658 examples: 12,245 Normal, 7,395 Pneumonia, 6,018 COVID-19) [0]. Bounding box coordinates for lung regions are available per example [0].

COVIDx-SeqCT, derived from COVIDx-CT, is split into train (2,390 examples: 486 Normal, 403 Pneumonia, 1,501 COVID-19), validation (430 examples: 172 Normal, 112 Pneumonia, 146 COVID-19), and test (408 examples: 174 Normal, 100 Pneumonia, 134 COVID-19) [0][1]. CT scans with fewer than 16 slices are discarded; each retained example consists of exactly 16 CT slices extracted uniformly [0]. Sampling criteria beyond this slice-count threshold are not documented in the repository.

<details><summary>Evidence (2)</summary>

- `docs/ct-report.pdf:40` (pdf, bm25=12.747)- `docs/ct-report.pdf:56` (pdf, bm25=9.662)</details>


## Dataset Distribution and Licensing

### Distribution
<sub>strategy: `tool` · status: **✅ filled**</sub>

- **dvc_remote**: gdrive://1n6fB1AHEiQ0x7m3Y0mlSmihLIYo583uf
- **mechanism**: data distributed through DVC pointers (not included in the git repository)

<details><summary>Evidence (2)</summary>

- `.dvc/config` — DVC remote- `*.dvc` — pointer</details>


### License
<sub>strategy: `tool` · status: **✅ filled**</sub>

- **license**: MIT
- **copyright**: 2021 Software engineering for AI-enabled systems @UniBa
- **scope_note**: licence of the repository (code); the DATA licence may differ and is not observable unless declared

<details><summary>Evidence (1)</summary>

- `LICENSE` — licence file</details>


## Access, Retention, and Deletion

### Access
<sub>strategy: `retrieval` · status: **⛔ ABSTAINED — no evidence in repository**</sub>

_No sufficient evidence in the repository: All chunks contain technical information about machine learning models (LSTM, attention mechanisms, data augmentation, and training procedures) but none address data access, retention, or deletion policies required by EU AI Act Article 10._

<details><summary>Evidence (5)</summary>

- `docs/ct-report.pdf:180` (pdf, bm25=5.134)- `docs/ct-report.pdf:404` (pdf, bm25=4.942)- `docs/ct-report.pdf:84` (pdf, bm25=4.812)- `docs/ct-report.pdf:288` (pdf, bm25=4.693)- `docs/ct-report.pdf:303` (pdf, bm25=4.667)</details>


### Retention & Deletion
<sub>strategy: `human` · status: **✍️ REQUIRES HUMAN INPUT**</sub>

_Judgement/organisational information: must be provided by the manufacturer._


## Data Risk Assessment

### Bias / risk examination
<sub>strategy: `retrieval` · status: **⛔ ABSTAINED — no evidence in repository**</sub>

_No sufficient evidence in the repository: The chunks describe dataset composition, class distributions, training procedures, and model evaluation metrics, but contain no examination of possible biases, risks related to PII, sensitive data, or any data risk assessment._

<details><summary>Evidence (5)</summary>

- `docs/ct-report.pdf:56` (pdf, bm25=5.111)- `docs/ct-report.pdf:40` (pdf, bm25=4.505)- `docs/ct-report.pdf:303` (pdf, bm25=3.754)- `dvc.yaml:1` (yaml, bm25=2.996)- `params.yaml:1` (yaml, bm25=2.992)</details>


## Cybersecurity Measures

### Security measures
<sub>strategy: `retrieval` · status: **⛔ ABSTAINED — no evidence in repository**</sub>

_No sufficient evidence in the repository: The chunk contains only project metadata and description (project name, badges, and purpose) with no information about security measures or cybersecurity measures applied to data._

<details><summary>Evidence (1)</summary>

- `README.md:1` (markdown, bm25=4.472)</details>


## Documentation Metadata

### Documentation authors
<sub>strategy: `tool` · status: **✅ filled**</sub>

- **generated_by**: LLMAutodoc (agentic documentation framework)
- **repository_contributors**: ["Lorenzo Loconte", "Giuseppe Colavito", "itsfrank98", "Francesco Benedetti", "Daniela Grassi"]

<details><summary>Evidence (1)</summary>

- `.git (git log)` — contributors</details>


### Document version
<sub>strategy: `tool` · status: **✅ filled**</sub>

- **document_version**: auto-2026-09-10-3f05400
- **generated_on**: 2026-09-10
- **repo_commit**: 3f05400

<details><summary>Evidence (1)</summary>

- `.git` — HEAD</details>


### Reviewers
<sub>strategy: `human` · status: **✍️ REQUIRES HUMAN INPUT**</sub>

_Judgement/organisational information: must be provided by the manufacturer._


## Standards Applied

### Standards
<sub>strategy: `human` · status: **✍️ REQUIRES HUMAN INPUT**</sub>

_Judgement/organisational information: must be provided by the manufacturer._


## Data Monitoring

### Monitoring
<sub>strategy: `tool` · status: **✅ filled**</sub>

- Prometheus
- Prometheus alert rules
- Grafana dashboard
- Alertmanager
- Prometheus metrics exposed by the service (src/monitoring.py)
- NOTE: SERVICE monitoring is observable, not DATA quality/drift monitoring

<details><summary>Evidence (5)</summary>

- `prometheus.yml` — monitoring configuration- `alert_rules.yml` — monitoring configuration- `grafana.json` — monitoring configuration- `alertmanager.yml` — monitoring configuration- `src/monitoring.py` — prometheus_client</details>


## EU Declaration of Conformity

### Declaration
<sub>strategy: `human` · status: **✍️ REQUIRES HUMAN INPUT**</sub>

_Judgement/organisational information: must be provided by the manufacturer._


