# Data Documentation — CT-COVID

> EU AI Act [Article 10](https://artificialintelligenceact.eu/article/10/) · [Article 11](https://artificialintelligenceact.eu/article/11/) · [Annex IV](https://artificialintelligenceact.eu/annex/4/) §1, §2(d)
>
> Generated on 2026-09-10 from `https://github.com/se4ai2122-cs-uniba/CT-COVID.git` by LLMAutodoc (routing: `agentic`).
> Fields: 34 filled, 2 abstained, 4 human_required.
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

The COVIDx-CT dataset contains 194,922 CT images (slices) split into training (143,778), validation (25,486), and test (25,658) sets [3]. Each image is annotated with one of three labels: normal, pneumonia (non-COVID-19), or COVID-19 [3]. Bounding box coordinates for lung regions are also provided per example [0]. The dataset is freely available on Kaggle [0]. The three classes are highly unbalanced [3].

From COVIDx-CT, a derived dataset called COVIDx-SeqCT is constructed, comprising 2,390 training, 430 validation, and 408 test examples [0]. Each example consists of a sequence of exactly 16 CT slices extracted uniformly from a CT scan; scans with fewer than 16 slices are discarded [0]. Class labels (normal, pneumonia, COVID-19) are assigned at the sequence level [1].

The datasets serve two classification tasks: single CT image classification and end-to-end CT scan sequence classification [3]. Attention mechanisms are additionally applied to generate prediction explanations, motivated by the interpretability requirements of the medical domain [3]. Preprocessing involves cropping to the lung bounding box and resizing to 224×224 using bicubic interpolation [2].

<details><summary>Evidence (5)</summary>

- `docs/ct-report.pdf:40` (pdf, bm25=19.345)- `docs/ct-report.pdf:56` (pdf, bm25=16.55)- `docs/ct-report.pdf:70` (pdf, bm25=13.573)- `docs/ct-report.pdf:25` (pdf, bm25=12.569)- `docs/ct-report.pdf:379` (pdf, bm25=12.172)</details>


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
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

No deployer instructions or restrictions for deployers using the data are documented in the repository.

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
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

Not documented in the repository.

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
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

A REST API accepting POST requests on port 5000 exposes a `/predict` endpoint that receives an image and its bounding box and returns predictions [2][3]. The API also provides `/models` for listing available models and `/docs` for API documentation [2]. A frontend application consumes the API, run via npm [0]. The API is consumed via HTTP requests, with curl demonstrated as an example client [3].

<details><summary>Evidence (5)</summary>

- `README.md:59` (markdown, bm25=15.244)- `README.md:53` (markdown, bm25=12.209)- `README.md:5` (markdown, bm25=11.517)- `README.md:13` (markdown, bm25=10.135)- `README.md:40` (markdown, bm25=8.141)</details>


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

The dataset was built for multi-class classification of lung CT images into three classes: normal, pneumonia, and COVID-19 [0]. The primary use case is screening CT images to determine whether a patient has a COVID-19 infection or non-COVID-19 pneumonia [0]. Minimizing false-negatives is a critical requirement of the use case, as infected patients may spread infection and face health complications [0].

<details><summary>Evidence (5)</summary>

- `docs/ct-report.pdf:1` (pdf, bm25=16.356)- `docs/ct-report.pdf:70` (pdf, bm25=14.903)- `docs/ct-report.pdf:201` (pdf, bm25=13.629)- `docs/ct-report.pdf:394` (pdf, bm25=13.532)- `README.md:5` (markdown, bm25=13.519)</details>


## Data Origin and Source

### Source(s)
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

The dataset used is COVIDx-CT, described as freely available on Kaggle [0]. It contains CT scan images with bounding box coordinates for lung regions, distributed across Normal, Pneumonia, and COVID-19 classes [0]. A derived dataset, COVIDx-SeqCT, was constructed from COVIDx-CT by extracting sequences of 16 CT slices uniformly from each scan; scans with fewer than 16 slices were discarded [0]. No URL, DOI, or further details on the original collection method, institutional origin, or data provider are documented in the repository.

<details><summary>Evidence (5)</summary>

- `docs/ct-report.pdf:40` (pdf, bm25=28.459)- `docs/ct-report.pdf:288` (pdf, bm25=18.791)- `docs/ct-report.pdf:70` (pdf, bm25=11.96)- `docs/ct-report.pdf:586` (pdf, bm25=11.791)- `docs/ct-report.pdf:528` (pdf, bm25=11.569)</details>


## Provenance

### Collection Method(s)
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

Data are collected from raw input files located in `data/raw` [3], preprocessed via `src/preprocessing.py` with images resized to 224×224 pixels and output to `data/ct` [3]. Datasets are instantiated with data augmentation applied to training data [0]. Training data are loaded in batches of 32 [4] using a data loader, optionally wrapped with tqdm progress tracking [1]. Validation data are similarly loaded via a separate data loader [2]. No information on the original data acquisition method (e.g., scanner type, clinical source, or collection protocol) is documented in the repository.

<details><summary>Evidence (5)</summary>

- `src/covidx/ct/dataset.py:78` (comment, bm25=7.102)- `src/covidx/utils/train.py:86` (comment, bm25=6.083)- `src/covidx/utils/train.py:122` (comment, bm25=6.083)- `dvc.yaml:1` (yaml, bm25=5.992)- `params.yaml:1` (yaml, bm25=5.983)</details>


### Dates of Collection
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

Not documented in the repository.

<details><summary>Evidence (5)</summary>

- `docs/ct-report.pdf:155` (pdf, bm25=9.03)- `docs/ct-report.pdf:288` (pdf, bm25=7.889)- `docs/ct-report.pdf:379` (pdf, bm25=7.386)- `docs/ct-report.pdf:233` (pdf, bm25=6.691)- `docs/ct-report.pdf:160` (pdf, bm25=6.629)</details>


### Collection Cadence
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

Not documented in the repository.

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
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

Resizing of raw images to 224×224 pixels is performed via `src/preprocessing.py`, taking inputs from `data/raw` and outputting to `data/ct` [2]. No further data cleaning operations (e.g., denoising, artifact removal, normalization, duplicate removal, or missing value handling) are documented in the repository.

<details><summary>Evidence (5)</summary>

- `docs/ct-report.pdf:404` (pdf, bm25=3.796)- `docs/ct-report.pdf:303` (pdf, bm25=3.654)- `dvc.yaml:1` (yaml, bm25=2.996)- `params.yaml:1` (yaml, bm25=2.992)- `src/covidx/ct/dataset.py:78` (comment, bm25=2.855)</details>


### Data Transformation
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

Input images are preprocessed via crop and resize with bicubic interpolation [0], then converted to tensors, normalized, moved to the target device, and unsqueezed along the batch dimension [1]. Data augmentation is applied during training, including random horizontal and vertical flip, Gaussian blur with kernel size 7 and standard deviation sampled uniformly from [0.05, 2.0], random affine transformations comprising scaling (scale ∈ [0.9, 1.1]), rotation (degrees ∈ [−30, 30]), translation (percentages ∈ [0.0, 0.1]), and random shear on the x-axis with rotation sampled uniformly from [−20, 20] [3].

<details><summary>Evidence (5)</summary>

- `src/api.py:201` (comment, bm25=19.021)- `src/api.py:168` (comment, bm25=5.83)- `src/covidx/ct/layers.py:5` (docstring, bm25=4.792)- `docs/ct-report.pdf:288` (pdf, bm25=4.531)- `docs/ct-report.pdf:561` (pdf, bm25=3.871)</details>


### Feature Engineering
<sub>strategy: `retrieval` · status: **⛔ ABSTAINED — no evidence in repository**</sub>

_Generated text failed the faithfulness check; unsupported: Local feature tensors are extracted from the innermost two ResNet50 layers [2], and global feature vectors are obtained via average pooling [1].; compatibility scores si = C(x̂i, g) are computed and normalized via softmax to produce attention weights ai [0][4]._

<details><summary>Evidence (5)</summary>

- `docs/ct-report.pdf:160` (pdf, bm25=12.755)- `src/covidx/ct/models.py:67` (comment, bm25=11.236)- `src/covidx/ct/models.py:60` (comment, bm25=11.023)- `docs/ct-report.pdf:115` (pdf, bm25=7.726)- `docs/ct-report.pdf:180` (pdf, bm25=7.3)</details>


### Data Augmentation
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

Data augmentation is applied to training data only [1]. Techniques include: random horizontal and vertical flip; Gaussian blur with kernel size 7 and standard deviation sampled uniformly from [0.05, 2.0]; random affine transformations comprising random scaling (scale ∈ [0.9, 1.1]), random rotation (degrees ∈ [−30, 30]), and random translation (translation percentage ∈ [0.0, 0.1]); and random shear on the x-axis with rotation sampled uniformly from [−20, 20] [0]. Augmentation was applied to reduce generalization error and improve classification accuracy [0].

<details><summary>Evidence (5)</summary>

- `docs/ct-report.pdf:288` (pdf, bm25=13.594)- `src/covidx/ct/dataset.py:78` (comment, bm25=7.299)- `docs/ct-report.pdf:561` (pdf, bm25=4.754)- `dvc.yaml:1` (yaml, bm25=2.996)- `params.yaml:1` (yaml, bm25=2.992)</details>


## Data Annotation and Labeling

### Annotation process
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

Each CT image (slice) is annotated with one of three labels: normal, pneumonia (non-COVID-19), or covid19 [0]. All CT slices belonging to a single CT scan share the same label, assigned by an expert evaluating all images of the sequence collectively [2]. The annotator role is described only as "an expert" [2]; no further details on annotator identity, number, qualifications, or inter-annotator agreement are provided. No annotation guidelines or protocols are documented in the repository. The labelling scheme is applied consistently across the COVIDx-CT dataset (143,778 training, 25,486 validation, 25,658 test images) [0] and the derived COVIDx-SeqCT dataset (2,390 training, 430 validation, 408 test sequences) [1]. The three classes are noted to be highly unbalanced [0]. No further details on the annotation process, tooling, or quality control are documented in the repository.

<details><summary>Evidence (5)</summary>

- `docs/ct-report.pdf:25` (pdf, bm25=8.994)- `docs/ct-report.pdf:56` (pdf, bm25=6.12)- `docs/ct-report.pdf:218` (pdf, bm25=5.505)- `docs/ct-report.pdf:379` (pdf, bm25=4.626)- `docs/ct-report.pdf:271` (pdf, bm25=1.694)</details>


## Validation Types

### Validation method(s)
<sub>strategy: `tool` · status: **✅ filled**</sub>

- Great Expectations (expectation suites / checkpoints)

<details><summary>Evidence (1)</summary>

- `tests/great_expectations/great_expectations.yml` — Great Expectations configuration</details>


## Sampling Methods

### Sampling / split
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

The COVIDx-CT dataset is split into train, validation, and test sets. Train contains 35,996 Normal, 25,496 Pneumonia, and 82,286 COVID-19 examples (143,778 total); validation contains 11,842, 7,400, and 6,244 (25,486 total); test contains 12,245, 7,395, and 6,018 (25,658 total) [2]. The derived COVIDx-SeqCT dataset uses sequences of exactly 16 CT slices extracted uniformly from scans; scans with fewer than 16 slices are discarded [2]. COVIDx-SeqCT train contains 486 Normal, 403 Pneumonia, and 1,501 COVID-19 examples (2,390 total); validation contains 172, 112, and 146 (430 total); test contains 174, 100, and 134 (408 total) [3]. Data augmentation is applied to training data only [4]. Sampling criteria beyond the 16-slice minimum threshold for COVIDx-SeqCT are not documented in the repository.

<details><summary>Evidence (5)</summary>

- `README.md:96` (markdown, bm25=12.851)- `src/covidx/utils/train.py:148` (comment, bm25=12.806)- `docs/ct-report.pdf:40` (pdf, bm25=12.747)- `docs/ct-report.pdf:56` (pdf, bm25=9.662)- `src/covidx/ct/dataset.py:78` (comment, bm25=7.036)</details>


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
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

Not documented in the repository.

<details><summary>Evidence (5)</summary>

- `docs/ct-report.pdf:180` (pdf, bm25=5.134)- `docs/ct-report.pdf:404` (pdf, bm25=4.942)- `docs/ct-report.pdf:84` (pdf, bm25=4.812)- `docs/ct-report.pdf:288` (pdf, bm25=4.693)- `docs/ct-report.pdf:303` (pdf, bm25=4.667)</details>


### Retention & Deletion
<sub>strategy: `human` · status: **✍️ REQUIRES HUMAN INPUT**</sub>

_Judgement/organisational information: must be provided by the manufacturer._


## Data Risk Assessment

### Bias / risk examination
<sub>strategy: `retrieval` · status: **⛔ ABSTAINED — no evidence in repository**</sub>

_Generated text failed the faithfulness check; unsupported: To mitigate this, a weighted binary cross-entropy loss is applied, with weights inversely proportional to class frequencies in the training data [2].; No other bias mitigation measures are documented.; Patient demographic information (age, sex, ethnicity) and geographic provenance of the CT scans are not documented in the repository, preventing assessment of demographic or population-level bias._

<details><summary>Evidence (5)</summary>

- `docs/ct-report.pdf:56` (pdf, bm25=5.111)- `docs/ct-report.pdf:40` (pdf, bm25=4.505)- `docs/ct-report.pdf:303` (pdf, bm25=3.754)- `dvc.yaml:1` (yaml, bm25=2.996)- `params.yaml:1` (yaml, bm25=2.992)</details>


## Cybersecurity Measures

### Security measures
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

No security measures applied to the data are documented in the repository [0].

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


