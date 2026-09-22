# Data Documentation — CT-COVID

> EU AI Act [Article 10](https://artificialintelligenceact.eu/article/10/) · [Article 11](https://artificialintelligenceact.eu/article/11/) · [Annex IV](https://artificialintelligenceact.eu/annex/4/) §1, §2(d)
>
> Generated on 2026-09-13 from `https://github.com/se4ai2122-cs-uniba/CT-COVID.git` by LLMAutodoc (routing: `agentic`).
> Fields: 36 filled, 4 human_required.
> Closed-scope corpus: 69 chunks from 13 files.
>
> **Reading guide.** Every field states *how* it was produced. `tool` = deterministic extraction from repository artefacts (no LLM involved in the value); `retrieval` = evidence retrieved from repository text, graded, and rewritten by an LLM using only that evidence; `human` = judgement that cannot be derived from artefacts. An **ABSTAINED** field means the repository contains no sufficient evidence — it must not be read as "not applicable".

**Dataset Owner**: - **organization**: se4ai2122-cs-uniba
- **main_contributor**: {"name": "Lorenzo Loconte", "email": "lorenzoloconte@outlook.it", "commits": 74}
**Document Version**: auto-2026-09-13-3f05400
**Reviewers**: _requires human input_

## Overview

### Dataset name
<sub>strategy: `tool` · status: **✅ filled**</sub>

CT-COVID

<details><summary>Evidence (1)</summary>

- `README.md` — first H1 title</details>


### Dataset Description
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

The dataset contains COVIDx-CT, which is freely available on Kaggle and consists of 143,778 training, 25,486 validation, and 25,658 test examples [0, 3]. Each example is a CT image (a slice of a CT scan) annotated with one of three highly unbalanced labels: normal, pneumonia (not caused by COVID-19), and covid19 (pneumonia caused by COVID-19) [0, 1, 3]. Bounding box coordinates for the lungs region are available for each example [0]. Additionally, the COVIDx-SeqCT dataset is obtained from the original dataset, composed of 2,390 training, 430 validation, and 408 test examples, where each example consists of a sequence of exactly 16 CT slices extracted uniformly from CT scans [0, 1]. The dataset serves the tasks of image classification and end-to-end classification of CT scans consisting of several CT images [2, 3]. The motivation and source details other than being on Kaggle are not documented in the repository [0].

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
- **days_since_last_commit**: 1705
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

To run the API locally, execute `pip install -r requirements.txt` [0]. To use tools such as `locust`, `pytest`, and `great_expectations`, execute `pip install -r requirements_dev.txt` [0]. Any other instructions and restrictions for deployers using the data are not documented in the repository.

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

Data metadata and schema are maintained and versioned using Great Expectations by running checkpoints for `ct-train`, `ct-valid`, and `ct-test` using the v3 API within the `tests` directory [2].

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

Not documented in the repository

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

The dataset was built for screening CT images of the lungs to determine if a patient has a COVID-19 infection or a non-COVID-19 pneumonia [0]. The task is a multi-class classification task with three classes: normal, pneumonia, and COVID-19 [0].

<details><summary>Evidence (5)</summary>

- `docs/ct-report.pdf:1` (pdf, bm25=16.356)- `docs/ct-report.pdf:70` (pdf, bm25=14.903)- `docs/ct-report.pdf:201` (pdf, bm25=13.629)- `docs/ct-report.pdf:394` (pdf, bm25=13.532)- `README.md:5` (markdown, bm25=13.519)</details>


## Data Origin and Source

### Source(s)
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

The dataset is freely available on Kaggle [0]. Links: not documented in the repository.

<details><summary>Evidence (5)</summary>

- `docs/ct-report.pdf:40` (pdf, bm25=28.459)- `docs/ct-report.pdf:288` (pdf, bm25=18.791)- `docs/ct-report.pdf:70` (pdf, bm25=11.96)- `docs/ct-report.pdf:586` (pdf, bm25=11.791)- `docs/ct-report.pdf:528` (pdf, bm25=11.569)</details>


## Provenance

### Collection Method(s)
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

Not documented in the repository.

<details><summary>Evidence (5)</summary>

- `src/covidx/ct/dataset.py:78` (comment, bm25=7.102)- `src/covidx/utils/train.py:86` (comment, bm25=6.083)- `src/covidx/utils/train.py:122` (comment, bm25=6.083)- `dvc.yaml:1` (yaml, bm25=5.992)- `params.yaml:1` (yaml, bm25=5.983)</details>


### Dates of Collection
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

not documented in the repository

<details><summary>Evidence (5)</summary>

- `docs/ct-report.pdf:155` (pdf, bm25=9.03)- `docs/ct-report.pdf:288` (pdf, bm25=7.889)- `docs/ct-report.pdf:379` (pdf, bm25=7.386)- `docs/ct-report.pdf:233` (pdf, bm25=6.691)- `docs/ct-report.pdf:160` (pdf, bm25=6.629)</details>


### Collection Cadence
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

not documented in the repository

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

Data cleaning operations are not documented in the repository.

<details><summary>Evidence (5)</summary>

- `docs/ct-report.pdf:404` (pdf, bm25=3.796)- `docs/ct-report.pdf:303` (pdf, bm25=3.654)- `dvc.yaml:1` (yaml, bm25=2.996)- `params.yaml:1` (yaml, bm25=2.992)- `src/covidx/ct/dataset.py:78` (comment, bm25=2.855)</details>


### Data Transformation
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

Data transformations applied to the input image include preprocessing via Crop and Resize using bicubic interpolation [0], converting to a tensor, normalization, moving to the device, and unsqueezing the batch dimension [1]. Data augmentation techniques include random horizontal and vertical flips, and Gaussian blur with a kernel size of 7 and a standard deviation sampled uniformly from [0.05, 2.0] [3]. Random affine transformations are also applied, consisting of random scaling with a scale sampled uniformly from [0.9, 1.1], random rotation with degrees sampled uniformly from [-30, 30], and random translation with percentages sampled uniformly from [0.0, 0.1] [3]. Additionally, random shear augmentation on the x-axis with rotation sampled uniformly from [-20, 20] is used [3].

<details><summary>Evidence (5)</summary>

- `src/api.py:201` (comment, bm25=19.021)- `src/api.py:168` (comment, bm25=5.83)- `src/covidx/ct/layers.py:5` (docstring, bm25=4.792)- `docs/ct-report.pdf:288` (pdf, bm25=4.531)- `docs/ct-report.pdf:561` (pdf, bm25=3.871)</details>


### Feature Engineering
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

Feature vectors $X = [x_1 ... x_n]$ are extracted at a certain convolutional layer, where each $x_i$ is the vector of output activations at spatial location $i$ [0]. Local feature tensors are obtained by forwarding through the innermost two ResNet50 layers [2]. A global feature vector $g$ is the output of the network's sequence of convolutional and non-linear layers [0], or is obtained by forwarding through average pooling [1], or by applying a linear transformation with a tanh activation function to the last hidden state $h_n$ given by a bidirectional RNN ($g = \tanh(W_g h_n + b_g$) [3]. The set of feature vectors $X$ is projected into the vector space of $g$ using a linear mapping ($\hat{X} = W_p X$) [0]. Compatibility scores $s_i$ between projected feature vectors $\hat{x}_i$ and $g$, or between $g$ and hidden states $h_i$, are computed using compatibility functions such as $C(\hat{x}_i, g) = \langle u, \hat{x}_i + g \rangle$ or the dot product $C(\hat{x}_i, g) = \langle \hat{x}_i, g \rangle$, as well as $s_i = g^T W_s h_i$ [0, 3, 4]. These scores are normalized via softmax to obtain attentions $a_i$ [0, 3, 4]. A context vector or new global feature $\hat{g}$ is then obtained as a linear combination of feature vectors $x_i$ (or hidden states $h_i$) with attentions $a_i$ ($\hat{g} = \sum_{i=1}^{n} a_i x_i$ or $\hat{g} = \sum_{i=1}^{n} a_i h_i$) [3, 4].

<details><summary>Evidence (5)</summary>

- `docs/ct-report.pdf:160` (pdf, bm25=12.755)- `src/covidx/ct/models.py:67` (comment, bm25=11.236)- `src/covidx/ct/models.py:60` (comment, bm25=11.023)- `docs/ct-report.pdf:115` (pdf, bm25=7.726)- `docs/ct-report.pdf:180` (pdf, bm25=7.3)</details>


### Data Augmentation
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

The dataset is augmented using random horizontal and vertical flips, and gaussian blur with a kernel size of 7 and standard deviation sampled uniformly from [0.05, 2.0] [0]. Random affine transformations are introduced, including random scaling with scale sampled uniformly from [0.9, 1.1], random rotation with degrees sampled uniformly from [-30, 30], and random translation with translation percentages sampled uniformly from [0.0, 0.1] [0]. Additionally, random shear augmentation on the x-axis with rotation sampled uniformly from [-20, 20] is used [0]. Data augmentation is applied to train data [1].

<details><summary>Evidence (5)</summary>

- `docs/ct-report.pdf:288` (pdf, bm25=13.594)- `src/covidx/ct/dataset.py:78` (comment, bm25=7.299)- `docs/ct-report.pdf:561` (pdf, bm25=4.754)- `dvc.yaml:1` (yaml, bm25=2.996)- `params.yaml:1` (yaml, bm25=2.992)</details>


## Data Annotation and Labeling

### Annotation process
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

Each CT image (a slice of a CT scan) and each sequence of CT images is annotated with one of three labels: normal (normal CT image), pneumonia (pneumonia not caused by COVID-19), and covid19 (pneumonia caused by COVID-19) [0, 1]. All CT slices belonging to a single CT scan and every image of a sequence share the same label, which is evaluated by an expert considering all of the images [0, 2]. Who performed the annotations and the specific annotation guidelines are not documented in the repository.

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

Sampling criteria: not documented in the repository [0, 1, 2, 3, 4]. For the COVIDx-CT dataset, the train, validation, and test splits contain 143,778, 25,486, and 25,658 examples respectively across Normal, Pneumonia, and COVID-19 classes [2]. For the COVIDx-SeqCT dataset—obtained from the original dataset by extracting sequences of exactly 16 CT slices uniformly from CT scans, while discarding scans with fewer than 16 slices—the train, validation, and test splits consist of 2,390, 430, and 408 examples respectively [2, 3]. Data augmentation is applied to train data [4]. Great Expectations checkpoints are run for `ct-train`, `ct-valid`, and `ct-test` [0].

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
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

To mitigate the problem of unbalanced training data, a weighted binary cross-entropy is used as the loss function, where the weights are inversely proportional with respect to the class frequencies in the training data [2]. Bias, PII, and sensitive data are not documented in the repository.

<details><summary>Evidence (5)</summary>

- `docs/ct-report.pdf:56` (pdf, bm25=5.111)- `docs/ct-report.pdf:40` (pdf, bm25=4.505)- `docs/ct-report.pdf:303` (pdf, bm25=3.754)- `dvc.yaml:1` (yaml, bm25=2.996)- `params.yaml:1` (yaml, bm25=2.992)</details>


## Cybersecurity Measures

### Security measures
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

not documented in the repository

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

- **document_version**: auto-2026-09-13-3f05400
- **generated_on**: 2026-09-13
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


