# Tutorial — Databases & Data Access (2 skills)

Both skills give your agent reproducible access to scientific and ML data. Use them when you need to look something up with explicit provenance, or discover datasets/models for a domain.

---

## 1. `database-lookup`

**What it does.** Deterministically queries **78 public databases** (PubChem, ChEMBL, UniProt, PDB, AlphaFold, KEGG, Reactome, STRING, ClinVar, COSMIC, ClinicalTrials.gov, FDA, FRED, USPTO, SEC EDGAR, and more) through documented REST APIs, with explicit filters, pagination, and provenance.

**Use it when** you need a reproducible lookup of a compound, gene, protein, pathway, variant, clinical trial, patent, economic indicator, structure, astronomy object, or database-backed scientific fact — where the endpoint, filter, and provenance must be explicit and verifiable.

**Example scenario.** A pharmacologist wants to verify drug-target interactions:
> "Look up **ChEMBL** for the target **dopamine receptor D3** and retrieve the bioactivity endpoints (IC50, Ki), then cross-check the gene in **UniProt** and the pathway in **KEGG**. Report each result with its endpoint and provenance so I can cite them."

**Why it's reliable.** Because it makes deterministic REST calls with explicit endpoints and pagination, the results are reproducible and traceable — ideal for work you'll include in a paper or report.

---

## 2. `hugging-science`

**What it does.** A curated catalog of scientific datasets, models, blog posts, and interactive Spaces across **17 domains** (biology, chemistry, physics, astronomy, climate, genomics, materials, medicine, ecology, energy, engineering, math, drug discovery, protein design, weather modeling, theorem proving, single-cell, PDE solving), with usage patterns for `datasets`, `transformers`, the HF Inference API, and `gradio_client`.

**Use it when** you're doing AI/ML work in a scientific domain and need to discover or use a dataset, model, or demo Space.

**Example scenario.** A materials scientist wants a pretrained model for property prediction:
> "Use **hugging-science** to find a Hugging Face dataset and pretrained model for **electrochemical property prediction**, load it with `datasets`/`transformers`, and run a quick inference example via the HF Inference API."

**Why it's useful.** It shortens the hunt for domain-specific ML resources — one skill to find datasets, models, and demos instead of searching the Hub manually.

---