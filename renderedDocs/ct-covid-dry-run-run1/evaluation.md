# Evaluation — ct-covid-dry-run-run1

- repository: `https://github.com/se4ai2122-cs-uniba/CT-COVID.git`
- routing: **agentic** (orchestrator turns: 0)
- models: generation `claude-sonnet-4-6`, grader/verifier `claude-haiku-4-5-20251001`
- top_k: 5 · verifier: True
- ground truth: `ct-covid.json`

## Metrics

| scope | n | GT present | GT absent | coverage | fill prec. | abst. prec. | abst. recall | halluc. |
|---|---|---|---|---|---|---|---|---|
| overall | 40 | 28 | 12 | 0.929 | 0.962 | 0.846 | 0.917 | 0.083 |
| tool | 18 | 18 | 0 | 1.0 | 1.0 |  |  |  |
| retrieval | 18 | 10 | 8 | 0.8 | 0.875 | 0.778 | 0.875 | 0.125 |
| human | 4 | 0 | 4 |  |  | 1.0 | 1.0 | 0.0 |

## Outcome counts

| outcome | meaning | count |
|---|---|---|
| TP_ok | correct (filled, content ok) | 25 |
| TP_content_ko | filled, expected term missing | 1 |
| FP_hallucination | HALLUCINATION (filled without evidence) | 1 |
| FN_missed | missed (wrong abstention) | 2 |
| TN_abstention | correct abstention | 11 |

## Fields to look at

| field | strategy | status | GT | outcome | note |
|---|---|---|---|---|---|
| deployerInstructions | retrieval | filled | absent | HALLUCINATION (filled without evidence) |  |
| schemaVersioning | retrieval | abstained | partial | missed (wrong abstention) | No sufficient evidence in the repository: lexical heuristic (dry-run) |
| dataTransformation | retrieval | filled | present | filled, expected term missing |  |
| riskAssessment | retrieval | abstained | partial | missed (wrong abstention) | No sufficient evidence in the repository: lexical heuristic (dry-run) |

## All fields

| field | section | strategy | status | GT | outcome | grader | faithful | covered by | #src |
|---|---|---|---|---|---|---|---|---|---|
| datasetName | Overview | tool | filled | present | TP_ok |  |  | declarative | 1 |
| datasetDescription | Overview | retrieval | filled | present | TP_ok | CORRECT | True | declarative | 5 |
| statusDate | Overview | tool | filled | present | TP_ok |  |  | declarative | 1 |
| status | Overview | tool | filled | present | TP_ok |  |  | declarative | 1 |
| relevantLinks | Overview | tool | filled | present | TP_ok |  |  | declarative | 3 |
| developers | Overview | tool | filled | present | TP_ok |  |  | declarative | 1 |
| owners | Overview | tool | filled | present | TP_ok |  |  | declarative | 2 |
| deployerInstructions | Overview | retrieval | filled | absent | FP_hallucination | CORRECT | True | declarative | 1 |
| versionDetails | Overview | tool | filled | present | TP_ok |  |  | declarative | 2 |
| dataVersionControlTools | Data Versioning | tool | filled | present | TP_ok |  |  | declarative | 4 |
| schemaVersioning | Data Versioning | retrieval | abstained | partial | FN_missed | INCORRECT |  | declarative | 5 |
| knownModels | Known Usages | tool | filled | present | TP_ok |  |  | declarative | 2 |
| knownApplications | Known Usages | retrieval | filled | present | TP_ok | CORRECT | True | declarative | 1 |
| dataTypes | Dataset Characteristics | tool | filled | present | TP_ok |  |  | declarative | 1 |
| size | Dataset Characteristics | tool | filled | present | TP_ok |  |  | declarative | 6 |
| primaryUseCases | Dataset Characteristics | retrieval | filled | present | TP_ok | CORRECT | True | declarative | 2 |
| sources | Data Origin and Source | retrieval | filled | present | TP_ok | CORRECT | True | declarative | 2 |
| collectionMethod | Provenance | retrieval | abstained | absent | TN_abstention | INCORRECT |  | declarative | 5 |
| collectionDates | Provenance | retrieval | abstained | absent | TN_abstention | INCORRECT |  | declarative | 5 |
| collectionCadence | Provenance | retrieval | abstained | absent | TN_abstention | INCORRECT |  | declarative | 5 |
| preprocessingPipeline | Data Pre-Processing | tool | filled | present | TP_ok |  |  | declarative | 2 |
| dataCleaning | Data Pre-Processing | retrieval | abstained | absent | TN_abstention | INCORRECT |  | declarative | 5 |
| dataTransformation | Data Pre-Processing | retrieval | filled | present | TP_content_ko | CORRECT | True | declarative | 3 |
| featureEngineering | Data Pre-Processing | retrieval | abstained | absent | TN_abstention | INCORRECT |  | declarative | 5 |
| dataAugmentation | Data Pre-Processing | retrieval | filled | present | TP_ok | CORRECT | True | declarative | 1 |
| annotation | Data Annotation and Labeling | retrieval | filled | partial | TP_ok | CORRECT | True | declarative | 3 |
| validation | Validation Types | tool | filled | present | TP_ok |  |  | declarative | 1 |
| sampling | Sampling Methods | retrieval | filled | present | TP_ok | CORRECT | True | declarative | 4 |
| distribution | Dataset Distribution and Licensing | tool | filled | present | TP_ok |  |  | declarative | 2 |
| license | Dataset Distribution and Licensing | tool | filled | present | TP_ok |  |  | declarative | 1 |
| access | Access, Retention, and Deletion | retrieval | abstained | absent | TN_abstention | INCORRECT |  | declarative | 5 |
| retention | Access, Retention, and Deletion | human | human_required | absent | TN_abstention |  |  | spec | 0 |
| riskAssessment | Data Risk Assessment | retrieval | abstained | partial | FN_missed | INCORRECT |  | declarative | 5 |
| cybersecurity | Cybersecurity Measures | retrieval | abstained | absent | TN_abstention | INCORRECT |  | declarative | 1 |
| docAuthors | Documentation Metadata | tool | filled | present | TP_ok |  |  | declarative | 1 |
| docVersion | Documentation Metadata | tool | filled | present | TP_ok |  |  | declarative | 1 |
| reviewers | Documentation Metadata | human | human_required | absent | TN_abstention |  |  | spec | 0 |
| standardsApplied | Standards Applied | human | human_required | absent | TN_abstention |  |  | spec | 0 |
| dataMonitoring | Data Monitoring | tool | filled | present | TP_ok |  |  | declarative | 5 |
| euDeclaration | EU Declaration of Conformity | human | human_required | absent | TN_abstention |  |  | spec | 0 |
