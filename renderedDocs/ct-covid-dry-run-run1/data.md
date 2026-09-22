# Data Documentation — CT-COVID

> EU AI Act [Article 10](https://artificialintelligenceact.eu/article/10/) · [Article 11](https://artificialintelligenceact.eu/article/11/) · [Annex IV](https://artificialintelligenceact.eu/annex/4/) §1, §2(d)
>
> Generated on 2026-09-10 from `https://github.com/se4ai2122-cs-uniba/CT-COVID.git` by LLMAutodoc (routing: `agentic`).
> Fields: 27 filled, 9 abstained, 4 human_required.
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

Moreover, within the dataset, the bounding box
coordinates for of lungs region are also available for each
example. The class distributions are available in Table I. The dataset
is freely available on Kaggle. TABLE I
COVID X-CT EXAMPLES DISTRIBUTION FOR EACH CLASS . COVIDx-CT Normal Pneumonia COVID-19 Total
Train 35,996 25,496 82,286 143,778
Validation 11,842 7400 6244 25,486
Test 12,245 7395 6018 25,658
Furthermore, another dataset called COVIDx-SeqCT is ob-
tained from the original dataset. The COVIDx-SeqCT dataset
is composed of 2390 training examples, 430 validation ex-
amples and 408 test examples. Each example consists of a
sequence of exactly 16 CT slices extracted uniformly from
CT scans. CT scans in the original dataset having less than
16 slices are discarded. [0] All the sequences of CT images are
annotated with one between three labels: normal (normal CT
image), pneumonia (pneumonia not caused by COVID-19)
and covid19 (pneumonia caused by COVID-19). The class
distributions of COVIDx-SeqCT are available in Table II. TABLE II
COVID X-S EQCT EXAMPLES DISTRIBUTION FOR EACH CLASS . COVIDx-SeqCT Normal Pneumonia COVID-19 Total
Train 486 403 1501 2390
Validation 172 112 146 43

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

C ONCLUSIONS AND FUTURE WORKS
We proposed two different approaches, one based on single
image classiﬁcation and one on sequence classiﬁcation. Both
of the approaches are performing quite well, but they are not
directly comparable, since they use different datasets. Further-
more, the COVIDx-SeqCT is very small, so the sequence-
based model should be tested on a bigger dataset to assess
better the performances. We think that the sequence-based
approach is more correct then evaluating single images sepa-
rately, that looks naive. Since a patient has more images for
a single CT-exam, a patient is being classiﬁed n times and
it is difﬁcult to understand how to get a single classiﬁcation
for the patient from the n classiﬁcations of his CT images. Instead, evaluating a patient from the whole sequence seems
more natural and may give a better overview of the patient’s
health state. [0]

<details><summary>Evidence (1)</summary>

- `docs/ct-report.pdf:528` (pdf, bm25=15.783)</details>


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

_No sufficient evidence in the repository: lexical heuristic (dry-run)_

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

# Usage
## API Endpoints
The API is accessible at the following endpoints:
- `/` which gives a welcome message
- `/docs` which provides a documentation of the API
- `/models` which provides a list of available models
- `/predict` used to receive prediction for a given image and his bounding box [0]

<details><summary>Evidence (1)</summary>

- `README.md:5` (markdown, bm25=11.517)</details>


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

[page 1]
Screening CT Images for COVID-19
Infections and Pneumonia
Lorenzo Loconte
University of Bari Aldo Moro
l.loconte5@studenti.uniba.it
744328
Giuseppe Colavito
University of Bari Aldo Moro
g.colavito2@studenti.uniba.it
736047
I. I NTRODUCTION
The goal of this work is to understand if a patient has a
COVID-19 infection or a non-COVID-19 pneumonia, given
some CT (computed tomography) images of the lungs. The
task is a multi-class classiﬁcation task with three classes:
normal, pneumonia and COVID-19. In this kind of task, it
is important to don’t have false-negatives, since an infected
patient can have several health problems and can help the
infection spreading. In this work two approaches are used to solve the problem,
both in the area of deep learning. The ﬁrst is to classify
each image separately, hence producing several predictions
for a single CT scan. [0] Empirical
results showed that the compatibility function in Equation (11)
generally outperforms the one in Equation (12). In general, multiple attention modules are used in CNNs at
different depth, hence obtaining a set of global features vector
G =
[ˆg1 ... ˆgm
]
where m is the number of attention
modules. Then the glob

<details><summary>Evidence (2)</summary>

- `docs/ct-report.pdf:1` (pdf, bm25=16.356)- `docs/ct-report.pdf:201` (pdf, bm25=13.629)</details>


## Data Origin and Source

### Source(s)
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

Moreover, within the dataset, the bounding box
coordinates for of lungs region are also available for each
example. The class distributions are available in Table I. The dataset
is freely available on Kaggle. TABLE I
COVID X-CT EXAMPLES DISTRIBUTION FOR EACH CLASS . COVIDx-CT Normal Pneumonia COVID-19 Total
Train 35,996 25,496 82,286 143,778
Validation 11,842 7400 6244 25,486
Test 12,245 7395 6018 25,658
Furthermore, another dataset called COVIDx-SeqCT is ob-
tained from the original dataset. The COVIDx-SeqCT dataset
is composed of 2390 training examples, 430 validation ex-
amples and 408 test examples. Each example consists of a
sequence of exactly 16 CT slices extracted uniformly from
CT scans. CT scans in the original dataset having less than
16 slices are discarded. [0] [page 8]
Fig. 6. Attention maps given from R ESNET50-LSTM-A TT2. The intensity of the attention maps have been weighted according to the sequence attention
map given by B I-LSTM. Normal CT scan images (on the left), non-COVID-19 pneumonia CT scan images (at the center) and COVID-19 pneumonia CT
scan images (on the right).
8

[page 9]
Fig. 7. Segmentation masks given from R ESNET50-A TT2, obtained by combining th

<details><summary>Evidence (2)</summary>

- `docs/ct-report.pdf:40` (pdf, bm25=28.459)- `docs/ct-report.pdf:586` (pdf, bm25=11.791)</details>


## Provenance

### Collection Method(s)
<sub>strategy: `retrieval` · status: **⛔ ABSTAINED — no evidence in repository**</sub>

_No sufficient evidence in the repository: lexical heuristic (dry-run)_

<details><summary>Evidence (5)</summary>

- `src/covidx/ct/dataset.py:78` (comment, bm25=7.102)- `src/covidx/utils/train.py:86` (comment, bm25=6.083)- `src/covidx/utils/train.py:122` (comment, bm25=6.083)- `dvc.yaml:1` (yaml, bm25=5.992)- `params.yaml:1` (yaml, bm25=5.983)</details>


### Dates of Collection
<sub>strategy: `retrieval` · status: **⛔ ABSTAINED — no evidence in repository**</sub>

_No sufficient evidence in the repository: lexical heuristic (dry-run)_

<details><summary>Evidence (5)</summary>

- `docs/ct-report.pdf:155` (pdf, bm25=9.03)- `docs/ct-report.pdf:288` (pdf, bm25=7.889)- `docs/ct-report.pdf:379` (pdf, bm25=7.386)- `docs/ct-report.pdf:233` (pdf, bm25=6.691)- `docs/ct-report.pdf:160` (pdf, bm25=6.629)</details>


### Collection Cadence
<sub>strategy: `retrieval` · status: **⛔ ABSTAINED — no evidence in repository**</sub>

_No sufficient evidence in the repository: lexical heuristic (dry-run)_

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
<sub>strategy: `retrieval` · status: **⛔ ABSTAINED — no evidence in repository**</sub>

_No sufficient evidence in the repository: lexical heuristic (dry-run)_

<details><summary>Evidence (5)</summary>

- `docs/ct-report.pdf:404` (pdf, bm25=3.796)- `docs/ct-report.pdf:303` (pdf, bm25=3.654)- `dvc.yaml:1` (yaml, bm25=2.996)- `params.yaml:1` (yaml, bm25=2.992)- `src/covidx/ct/dataset.py:78` (comment, bm25=2.855)</details>


### Data Transformation
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

Preprocess the image using Crop + Resize (with bicubic interpolation) [0] Convert the input image to a tensor, normalize it,
move it to device and unsqueeze the batch dimension [1] Experimental Setting
Data augmentation has been used because, in general, hav-
ing augmented data can help to achieve a lower generalization
error and higher classiﬁcation accuracy, as shown in [7], [8]. The dataset is augmented using random horizontal and vertical
ﬂip, gaussian blur with kernel size 7 and standard deviation
sampled uniformly from [0.05, 2.0]. Moreover, random afﬁne
transformations including random scaling (with scale sampled
uniformly from [0.9, 1.1]), random rotation (with degrees sam-
pled uniformly from [−30, 30]) and random translation (with
translation percentages sampled uniformly from [0.0, 0.1]) are
introduced as well. Moreover, random shear augmentation on
the x-axis with rotation sampled uniformly from [−20, 20] is
used. The default layers of R ESNET50-A TT2 are initialized with
pretraining on ImageNet. [2]

<details><summary>Evidence (3)</summary>

- `src/api.py:201` (comment, bm25=19.021)- `src/api.py:168` (comment, bm25=5.83)- `docs/ct-report.pdf:288` (pdf, bm25=4.531)</details>


### Feature Engineering
<sub>strategy: `retrieval` · status: **⛔ ABSTAINED — no evidence in repository**</sub>

_No sufficient evidence in the repository: lexical heuristic (dry-run)_

<details><summary>Evidence (5)</summary>

- `docs/ct-report.pdf:160` (pdf, bm25=12.755)- `src/covidx/ct/models.py:67` (comment, bm25=11.236)- `src/covidx/ct/models.py:60` (comment, bm25=11.023)- `docs/ct-report.pdf:115` (pdf, bm25=7.726)- `docs/ct-report.pdf:180` (pdf, bm25=7.3)</details>


### Data Augmentation
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

Experimental Setting
Data augmentation has been used because, in general, hav-
ing augmented data can help to achieve a lower generalization
error and higher classiﬁcation accuracy, as shown in [7], [8]. The dataset is augmented using random horizontal and vertical
ﬂip, gaussian blur with kernel size 7 and standard deviation
sampled uniformly from [0.05, 2.0]. Moreover, random afﬁne
transformations including random scaling (with scale sampled
uniformly from [0.9, 1.1]), random rotation (with degrees sam-
pled uniformly from [−30, 30]) and random translation (with
translation percentages sampled uniformly from [0.0, 0.1]) are
introduced as well. Moreover, random shear augmentation on
the x-axis with rotation sampled uniformly from [−20, 20] is
used. The default layers of R ESNET50-A TT2 are initialized with
pretraining on ImageNet. [0]

<details><summary>Evidence (1)</summary>

- `docs/ct-report.pdf:288` (pdf, bm25=13.594)</details>


## Data Annotation and Labeling

### Annotation process
<sub>strategy: `retrieval` · status: **✅ filled**</sub>

The second is to classify a CT scan,
consisting of several CT images, in an end-to-end fashion. Moreover, attention mechanisms are used to generate some
explanations regarding the predictions, a very important aspect
in the underlying medical domain. II. D ATASET
The COVIDx-CT dataset is composed of 143,778 training
examples, 25,486 validation examples and 25,658 testing
examples. Each example is a CT image (i.e. a slice of a CT
scan) and it is annotated with one between three labels: normal
(normal CT image), pneumonia (pneumonia not caused by
COVID-19) and covid19 (pneumonia caused by COVID-19). However, all CT slices belonging to a single CT scan have the
same label. In other words, we also have annotated CT scans,
consisting of several CT slices. It’s important to notice that
the three classes ( normal, pneumonia and covid19) are highly
unbalanced. [0] All the sequences of CT images are
annotated with one between three labels: normal (normal CT
image), pneumonia (pneumonia not caused by COVID-19)
and covid19 (pneumonia caused by COVID-19). The class
distributions of COVIDx-SeqCT are available in Table II. TABLE II
COVID X-S EQCT EXAMPLES DISTRIBUTION FOR EACH CLASS . COVIDx-Seq

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

## Great Expectations
```bash
cd tests
for checkpoint in ct-train ct-valid ct-test
do
  great_expectations --v3-api checkpoint run $checkpoint
done
``` [0] Get the average train and validation losses and accuracies and print it [1] Moreover, within the dataset, the bounding box
coordinates for of lungs region are also available for each
example. The class distributions are available in Table I. The dataset
is freely available on Kaggle. TABLE I
COVID X-CT EXAMPLES DISTRIBUTION FOR EACH CLASS . COVIDx-CT Normal Pneumonia COVID-19 Total
Train 35,996 25,496 82,286 143,778
Validation 11,842 7400 6244 25,486
Test 12,245 7395 6018 25,658
Furthermore, another dataset called COVIDx-SeqCT is ob-
tained from the original dataset. The COVIDx-SeqCT dataset
is composed of 2390 training examples, 430 validation ex-
amples and 408 test examples. Each example consists of a
sequence of exactly 16 CT slices extracted uniformly from
CT scans. CT scans in the original dataset having less than
16 slices are discarded. [2] All the sequences of CT images are
annotated with one between three labels: normal (normal CT
image), pneumonia (pneumonia not caused by COVID-19)
and covid19 (pneumonia caused by COV

<details><summary>Evidence (4)</summary>

- `README.md:96` (markdown, bm25=12.851)- `src/covidx/utils/train.py:148` (comment, bm25=12.806)- `docs/ct-report.pdf:40` (pdf, bm25=12.747)- `docs/ct-report.pdf:56` (pdf, bm25=9.662)</details>


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

_No sufficient evidence in the repository: lexical heuristic (dry-run)_

<details><summary>Evidence (5)</summary>

- `docs/ct-report.pdf:180` (pdf, bm25=5.134)- `docs/ct-report.pdf:404` (pdf, bm25=4.942)- `docs/ct-report.pdf:84` (pdf, bm25=4.812)- `docs/ct-report.pdf:288` (pdf, bm25=4.693)- `docs/ct-report.pdf:303` (pdf, bm25=4.667)</details>


### Retention & Deletion
<sub>strategy: `human` · status: **✍️ REQUIRES HUMAN INPUT**</sub>

_Judgement/organisational information: must be provided by the manufacturer._


## Data Risk Assessment

### Bias / risk examination
<sub>strategy: `retrieval` · status: **⛔ ABSTAINED — no evidence in repository**</sub>

_No sufficient evidence in the repository: lexical heuristic (dry-run)_

<details><summary>Evidence (5)</summary>

- `docs/ct-report.pdf:56` (pdf, bm25=5.111)- `docs/ct-report.pdf:40` (pdf, bm25=4.505)- `docs/ct-report.pdf:303` (pdf, bm25=3.754)- `dvc.yaml:1` (yaml, bm25=2.996)- `params.yaml:1` (yaml, bm25=2.992)</details>


## Cybersecurity Measures

### Security measures
<sub>strategy: `retrieval` · status: **⛔ ABSTAINED — no evidence in repository**</sub>

_No sufficient evidence in the repository: lexical heuristic (dry-run)_

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


