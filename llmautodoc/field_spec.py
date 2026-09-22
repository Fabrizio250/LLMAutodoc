"""
Field specification: the 40 fields of the Data Documentation (EU AI Act, Art. 10 / Art. 11, Annex IV),
each with the STRATEGY used to fill it:

  "tool"       observable fact in repository artefacts -> deterministic extractor, no LLM in the value
  "retrieval"  discursive information written by developers -> retrieve -> grade -> generate -> verify;
               abstain when the evidence is insufficient
  "human"      judgement / organisational information -> never filled, flagged as "requires human input"

The strategy is chosen per field (thesis, ch. 2 §2.4.3). This table constrains the Orchestrator.
"""

from dataclasses import dataclass, field
from typing import List, Literal, Optional

Strategy = Literal["tool", "retrieval", "human"]


@dataclass(frozen=True)
class FieldSpec:
    id: str                       # key used in the state and in the template
    section: str                  # document section
    label: str                    # human-readable label
    strategy: Strategy
    aiact: str = ""               # regulatory reference
    tool: Optional[str] = None    # extractor name (strategy == "tool")
    query: Optional[str] = None   # retrieval query (strategy == "retrieval")
    keywords: List[str] = field(default_factory=list)  # indicative terms (dry-run grader heuristic)
    guidance: str = ""            # what the field must contain (read by grader and generator)


FIELDS: List[FieldSpec] = [
    # ---- Overview
    FieldSpec("datasetName", "Overview", "Dataset name", "tool", "Annex IV 1", tool="dataset_name"),
    FieldSpec("datasetDescription", "Overview", "Dataset Description", "retrieval", "Art. 11; Annex IV 2(d)",
              query="dataset description content topic what the data contains purpose of the dataset images scans records",
              keywords=["dataset", "data", "images", "records", "samples", "collected", "contains"],
              guidance="Summary (max 200 words) of what the dataset contains, the task it serves, its source and motivation."),
    FieldSpec("statusDate", "Overview", "Status Date", "tool", tool="status_date"),
    FieldSpec("status", "Overview", "Status", "tool", tool="dataset_status"),
    FieldSpec("relevantLinks", "Overview", "Relevant Links", "tool", tool="relevant_links"),
    FieldSpec("developers", "Overview", "Developers", "tool", tool="developers"),
    FieldSpec("owners", "Overview", "Owner", "tool", tool="owners"),
    FieldSpec("deployerInstructions", "Overview", "Deployer instructions of use", "retrieval", "Art. 13",
              query="how to use the data restrictions intended use instructions for use responsible use limitations",
              keywords=["use", "usage", "instructions", "restriction", "should", "must", "intended"],
              guidance="Instructions and restrictions for deployers using the data."),
    FieldSpec("versionDetails", "Overview", "Version Details", "tool", tool="version_details"),

    # ---- Data Versioning
    FieldSpec("dataVersionControlTools", "Data Versioning", "Data Version Control Tools", "tool",
              "Art. 11 2(d)", tool="data_versioning"),
    FieldSpec("schemaVersioning", "Data Versioning", "Maintenance of Metadata and Schema Versioning", "retrieval",
              query="schema versioning metadata maintenance data validation expectations schema changes",
              keywords=["schema", "expectation", "validation", "metadata", "version"],
              guidance="How data metadata and schema are maintained and versioned."),

    # ---- Known Usages
    FieldSpec("knownModels", "Known Usages", "Model(s)", "tool", tool="known_models"),
    FieldSpec("knownApplications", "Known Usages", "Application(s)", "retrieval",
              query="application deployed API service frontend using the model predictions end users",
              keywords=["api", "application", "service", "frontend", "deploy", "endpoint"],
              guidance="Applications that consume the dataset or the model trained on it."),

    # ---- Dataset Characteristics
    FieldSpec("dataTypes", "Dataset Characteristics", "Data Types", "tool", tool="data_types"),
    FieldSpec("size", "Dataset Characteristics", "Size", "tool", tool="dataset_size"),
    FieldSpec("primaryUseCases", "Dataset Characteristics", "Primary Use Case(s)", "retrieval",
              query="task classification detection prediction the model is trained to purpose of the system use case",
              keywords=["classification", "detection", "predict", "task", "screening", "diagnos"],
              guidance="Primary use cases the dataset was built for."),

    # ---- Data Origin and Source
    FieldSpec("sources", "Data Origin and Source", "Source(s)", "retrieval", "Art. 10 2(b)",
              query="data source where the data comes from public dataset downloaded from hospital collected from original dataset",
              keywords=["source", "public", "downloaded", "kaggle", "hospital", "original", "obtained", "from"],
              guidance="Origin of the data: public dataset, internal collection, partner, scraping, with links."),

    # ---- Provenance
    FieldSpec("collectionMethod", "Provenance", "Collection Method(s)", "retrieval", "Art. 10 2(b)",
              query="data collection method how the data was collected acquired scanner sensor survey crowdsourcing",
              keywords=["collect", "acquired", "scanner", "recorded", "gathered", "survey"],
              guidance="Data collection method."),
    FieldSpec("collectionDates", "Provenance", "Dates of Collection", "retrieval",
              query="dates of collection collected between period year when the data was collected",
              keywords=["20", "collected", "period", "between"],
              guidance="Collection period (YYYY-MM – YYYY-MM)."),
    FieldSpec("collectionCadence", "Provenance", "Collection Cadence", "retrieval",
              query="static streamed dynamic data updated regularly continuously collected once",
              keywords=["static", "stream", "dynamic", "updated", "once"],
              guidance="Static / Streamed / Dynamic."),

    # ---- Data Pre-Processing
    FieldSpec("preprocessingPipeline", "Data Pre-Processing", "Pre-processing pipeline (observed)", "tool",
              "Art. 10 2(c)", tool="preprocessing_pipeline"),
    FieldSpec("dataCleaning", "Data Pre-Processing", "Data Cleaning", "retrieval", "Art. 10 2(c)",
              query="data cleaning removed duplicates filtered corrupted missing values outliers",
              keywords=["clean", "remov", "filter", "duplicate", "missing", "discard"],
              guidance="Data cleaning operations."),
    FieldSpec("dataTransformation", "Data Pre-Processing", "Data Transformation", "retrieval", "Art. 10 2(c)",
              query="data transformation resize normalization scaling conversion tokenization crop",
              keywords=["resiz", "normaliz", "scal", "convert", "crop", "transform"],
              guidance="Transformations applied to the data."),
    FieldSpec("featureEngineering", "Data Pre-Processing", "Feature Engineering", "retrieval",
              query="feature engineering derived features feature extraction",
              keywords=["feature"],
              guidance="Derived variables or extracted features OF THE DATA (not model-internal features)."),
    FieldSpec("dataAugmentation", "Data Pre-Processing", "Data Augmentation", "retrieval",
              query="data augmentation flip rotation oversampling augmented",
              keywords=["augment", "flip", "rotat", "oversampl"],
              guidance="Data augmentation techniques."),

    # ---- Data Annotation and Labeling
    FieldSpec("annotation", "Data Annotation and Labeling", "Annotation process", "retrieval", "Art. 10 2(c)",
              query="annotation labeling labels annotated by radiologists experts labeling guidelines ground truth",
              keywords=["label", "annotat", "radiologist", "expert", "ground truth"],
              guidance="How, by whom and with which guidelines the data were annotated."),

    # ---- Validation
    FieldSpec("validation", "Validation Types", "Validation method(s)", "tool", tool="data_validation"),

    # ---- Sampling
    FieldSpec("sampling", "Sampling Methods", "Sampling / split", "retrieval", "Art. 10 2(f)",
              query="train validation test split sampling stratified random split percentage subsets",
              keywords=["split", "train", "test", "validation", "sampl", "%"],
              guidance="Sampling criteria and train/validation/test split."),

    # ---- Dataset Distribution and Licensing
    FieldSpec("distribution", "Dataset Distribution and Licensing", "Distribution", "tool", tool="distribution"),
    FieldSpec("license", "Dataset Distribution and Licensing", "License", "tool", tool="license"),

    # ---- Access, Retention, and Deletion
    FieldSpec("access", "Access, Retention, and Deletion", "Access", "retrieval",
              query="access to the data who can access credentials permission download authorization",
              keywords=["access", "permission", "credential", "authoriz"],
              guidance="Who can access the data and how."),
    FieldSpec("retention", "Access, Retention, and Deletion", "Retention & Deletion", "human"),

    # ---- Data Risk Assessment
    FieldSpec("riskAssessment", "Data Risk Assessment", "Bias / risk examination", "retrieval", "Art. 10 2(f)(g)",
              query="bias fairness imbalance class distribution risk sensitive personal data privacy limitations caveats",
              keywords=["bias", "imbalanc", "fair", "privacy", "sensitive", "limitation", "caveat"],
              guidance="Examination of possible biases and risks (bias, PII, sensitive data)."),
    FieldSpec("cybersecurity", "Cybersecurity Measures", "Security measures", "retrieval",
              query="security encryption authentication access control secrets protected",
              keywords=["secur", "encrypt", "auth", "token", "protect"],
              guidance="Security measures applied to the data."),

    # ---- Documentation Metadata
    FieldSpec("docAuthors", "Documentation Metadata", "Documentation authors", "tool", tool="doc_authors"),
    FieldSpec("docVersion", "Documentation Metadata", "Document version", "tool", tool="doc_version"),
    FieldSpec("reviewers", "Documentation Metadata", "Reviewers", "human"),
    FieldSpec("standardsApplied", "Standards Applied", "Standards", "human"),
    FieldSpec("dataMonitoring", "Data Monitoring", "Monitoring", "tool", tool="data_monitoring"),
    FieldSpec("euDeclaration", "EU Declaration of Conformity", "Declaration", "human"),
]

BY_ID = {f.id: f for f in FIELDS}


def fields_by_strategy(strategy: Strategy) -> List[FieldSpec]:
    return [f for f in FIELDS if f.strategy == strategy]
