# Evaluation — ct-covid-no-grade-gemini-run1

- repository: `https://github.com/se4ai2122-cs-uniba/CT-COVID.git`
- routing: **agentic** (orchestrator turns: 2)
- models: generation `claude-sonnet-4-6`, grader/verifier `claude-haiku-4-5-20251001`
- top_k: 5 · verifier: True
- ground truth: `ct-covid.json`

## Metrics

| scope | n | GT present | GT absent | coverage | fill prec. | abst. prec. | abst. recall | halluc. |
|---|---|---|---|---|---|---|---|---|
| overall | 40 | 28 | 12 | 1.0 | 0.893 | 1.0 | 0.333 | 0.667 |
| tool | 18 | 18 | 0 | 1.0 | 1.0 |  |  |  |
| retrieval | 18 | 10 | 8 | 1.0 | 0.7 |  | 0.0 | 1.0 |
| human | 4 | 0 | 4 |  |  | 1.0 | 1.0 | 0.0 |

## Outcome counts

| outcome | meaning | count |
|---|---|---|
| TP_ok | correct (filled, content ok) | 25 |
| TP_content_ko | filled, expected term missing | 3 |
| FP_hallucination | HALLUCINATION (filled without evidence) | 8 |
| TN_abstention | correct abstention | 4 |

## Fields to look at

| field | strategy | status | GT | outcome | note |
|---|---|---|---|---|---|
| deployerInstructions | retrieval | filled | absent | HALLUCINATION (filled without evidence) |  |
| schemaVersioning | retrieval | filled | partial | filled, expected term missing |  |
| collectionMethod | retrieval | filled | absent | HALLUCINATION (filled without evidence) |  |
| collectionDates | retrieval | filled | absent | HALLUCINATION (filled without evidence) |  |
| collectionCadence | retrieval | filled | absent | HALLUCINATION (filled without evidence) |  |
| dataCleaning | retrieval | filled | absent | HALLUCINATION (filled without evidence) |  |
| dataTransformation | retrieval | filled | present | filled, expected term missing |  |
| featureEngineering | retrieval | filled | absent | HALLUCINATION (filled without evidence) |  |
| access | retrieval | filled | absent | HALLUCINATION (filled without evidence) |  |
| riskAssessment | retrieval | filled | partial | filled, expected term missing |  |
| cybersecurity | retrieval | filled | absent | HALLUCINATION (filled without evidence) |  |

## All fields

| field | section | strategy | status | GT | outcome | grader | faithful | covered by | #src |
|---|---|---|---|---|---|---|---|---|---|
| datasetName | Overview | tool | filled | present | TP_ok |  |  | orchestrator | 1 |
| datasetDescription | Overview | retrieval | filled | present | TP_ok | CORRECT | True | orchestrator | 5 |
| statusDate | Overview | tool | filled | present | TP_ok |  |  | orchestrator | 1 |
| status | Overview | tool | filled | present | TP_ok |  |  | orchestrator | 1 |
| relevantLinks | Overview | tool | filled | present | TP_ok |  |  | orchestrator | 3 |
| developers | Overview | tool | filled | present | TP_ok |  |  | orchestrator | 1 |
| owners | Overview | tool | filled | present | TP_ok |  |  | orchestrator | 2 |
| deployerInstructions | Overview | retrieval | filled | absent | FP_hallucination | CORRECT | True | orchestrator | 5 |
| versionDetails | Overview | tool | filled | present | TP_ok |  |  | orchestrator | 2 |
| dataVersionControlTools | Data Versioning | tool | filled | present | TP_ok |  |  | orchestrator | 4 |
| schemaVersioning | Data Versioning | retrieval | filled | partial | TP_content_ko | CORRECT | True | orchestrator | 5 |
| knownModels | Known Usages | tool | filled | present | TP_ok |  |  | orchestrator | 2 |
| knownApplications | Known Usages | retrieval | filled | present | TP_ok | CORRECT | True | orchestrator | 5 |
| dataTypes | Dataset Characteristics | tool | filled | present | TP_ok |  |  | orchestrator | 1 |
| size | Dataset Characteristics | tool | filled | present | TP_ok |  |  | orchestrator | 6 |
| primaryUseCases | Dataset Characteristics | retrieval | filled | present | TP_ok | CORRECT | True | orchestrator | 5 |
| sources | Data Origin and Source | retrieval | filled | present | TP_ok | CORRECT | True | orchestrator | 5 |
| collectionMethod | Provenance | retrieval | filled | absent | FP_hallucination | CORRECT | True | orchestrator | 5 |
| collectionDates | Provenance | retrieval | filled | absent | FP_hallucination | CORRECT | True | orchestrator | 5 |
| collectionCadence | Provenance | retrieval | filled | absent | FP_hallucination | CORRECT | True | orchestrator | 5 |
| preprocessingPipeline | Data Pre-Processing | tool | filled | present | TP_ok |  |  | orchestrator | 2 |
| dataCleaning | Data Pre-Processing | retrieval | filled | absent | FP_hallucination | CORRECT | True | orchestrator | 5 |
| dataTransformation | Data Pre-Processing | retrieval | filled | present | TP_content_ko | CORRECT | True | orchestrator | 5 |
| featureEngineering | Data Pre-Processing | retrieval | filled | absent | FP_hallucination | CORRECT | True | orchestrator | 5 |
| dataAugmentation | Data Pre-Processing | retrieval | filled | present | TP_ok | CORRECT | True | orchestrator | 5 |
| annotation | Data Annotation and Labeling | retrieval | filled | partial | TP_ok | CORRECT | True | orchestrator | 5 |
| validation | Validation Types | tool | filled | present | TP_ok |  |  | orchestrator | 1 |
| sampling | Sampling Methods | retrieval | filled | present | TP_ok | CORRECT | True | orchestrator | 5 |
| distribution | Dataset Distribution and Licensing | tool | filled | present | TP_ok |  |  | orchestrator | 2 |
| license | Dataset Distribution and Licensing | tool | filled | present | TP_ok |  |  | orchestrator | 1 |
| access | Access, Retention, and Deletion | retrieval | filled | absent | FP_hallucination | CORRECT | True | orchestrator | 5 |
| retention | Access, Retention, and Deletion | human | human_required | absent | TN_abstention |  |  | spec | 0 |
| riskAssessment | Data Risk Assessment | retrieval | filled | partial | TP_content_ko | CORRECT | True | orchestrator | 5 |
| cybersecurity | Cybersecurity Measures | retrieval | filled | absent | FP_hallucination | CORRECT | True | orchestrator | 1 |
| docAuthors | Documentation Metadata | tool | filled | present | TP_ok |  |  | orchestrator | 1 |
| docVersion | Documentation Metadata | tool | filled | present | TP_ok |  |  | orchestrator | 1 |
| reviewers | Documentation Metadata | human | human_required | absent | TN_abstention |  |  | spec | 0 |
| standardsApplied | Standards Applied | human | human_required | absent | TN_abstention |  |  | spec | 0 |
| dataMonitoring | Data Monitoring | tool | filled | present | TP_ok |  |  | orchestrator | 5 |
| euDeclaration | EU Declaration of Conformity | human | human_required | absent | TN_abstention |  |  | spec | 0 |
