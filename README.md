# Awesome IDR Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.md)
[![Skills](https://img.shields.io/badge/Skills-72-brightgreen.svg)](#-available-skills)
[![Agent Skills](https://img.shields.io/badge/Standard-Agent_Skills-blueviolet.svg)](https://agentskills.io/)
[![Works with](https://img.shields.io/badge/Works_with-Cursor_|_Claude_Code_|_Codex_|_Google_Antigravity-blue.svg)](#-getting-started)


**A curated collection of 72 scientific and research skills for any AI agent that supports the open [Agent Skills](https://agentskills.io/) standard.** Built by [K-Dense](https://k-dense.ai) and working with **Cursor, Claude Code, Codex, Google Antigravity, and more**, these skills turn your coding agent into a research assistant that can run multi-step scientific workflows — searching the literature, querying 78+ public databases, analyzing data, training models, and producing publication-ready figures, papers, and reports.

> The agent can already write code with any Python package or call any API. These skills add curated documentation, working examples, and best practices so common research workflows run faster and more reliably.

> ⭐ **If these skills save you time, please [star the repo](https://github.com/K-Dense-AI/scientific-agent-skills).** It helps other scientists find the project and tells us which workflows are worth expanding.

---

## 📋 Table of Contents

- [Why Use This?](#-why-use-this)
- [Getting Started](#-getting-started)
- [Prerequisites](#-prerequisites)
- [Quick Examples](#-quick-examples)
- [Available Skills](#-available-skills)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Why Use This?

- **Skip the boilerplate** — no more hunting through API docs or wiring up integrations by hand. Each skill ships with tested examples and best practices.
- **Run multi-step workflows from one prompt** — chain literature search, database lookups, analysis, modeling, and reporting in a single request.
- **Reproducible by design** — the `database-lookup` skill makes deterministic REST calls with explicit endpoints, filters, pagination, and provenance.
- **Portable across agents** — one open standard, many hosts (Cursor, Claude Code, Codex, Gemini CLI, Google Antigravity, OpenClaw, Pi, and more).
- **Actively maintained** — continuously updated and security-scanned by the K-Dense team and community contributors.

---

## 🎯 Getting Started

### Option 1: npx (all platforms)

```bash
npx skills add K-Dense-AI/scientific-agent-skills
```

This is the standard way to install Agent Skills across **all platforms**, including **Claude Code**, **Codex**, **Gemini CLI**, **Google Antigravity**, **Cursor**, **OpenClaw**, **Pi**, and any other agent that supports the open [Agent Skills](https://agentskills.io/) standard.

### Option 2: GitHub CLI (`gh skill`)

With the [GitHub CLI](https://cli.github.com/) (v2.90.0+):

```bash
# Browse and install interactively
gh skill install K-Dense-AI/scientific-agent-skills

# Install a single skill
gh skill install K-Dense-AI/scientific-agent-skills database-lookup

# Target a specific agent host
gh skill install K-Dense-AI/scientific-agent-skills --agent claude-code
gh skill install K-Dense-AI/scientific-agent-skills --agent cursor
gh skill install K-Dense-AI/scientific-agent-skills --agent codex

# Pin to a release tag or commit for reproducible installs
gh skill install K-Dense-AI/scientific-agent-skills --pin v2.52.0

# Keep installed skills up to date
gh skill update --all
```

`gh skill` installs to the right directory for your agent host and records provenance metadata for supply-chain integrity.

### Option 3: Clone directly

Any compliant client that scans the shared skills directory will discover them automatically:

```bash
# User-level install
git clone https://github.com/K-Dense-AI/scientific-agent-skills.git ~/.agents/skills/scientific-agent-skills

# Project-level install
git clone https://github.com/K-Dense-AI/scientific-agent-skills.git .agents/skills/scientific-agent-skills
```

> 💡 **Tip:** You don't need every skill. Install the topical subset you actually use — it keeps your agent's context lean and reduces the surface area you need to trust (see [Security Disclaimer](#%EF%B8%8F-security-disclaimer)).

**That's it.** Your agent discovers relevant skills automatically, and you can always invoke one by name in your prompt.

---

## ⚙️ Prerequisites

- **Python**: 3.13+ for repository tooling; individual skills may support broader ranges (check each `SKILL.md`).
- **uv**: Python package manager used to install skill dependencies.
- **A compatible agent**: any host that supports the [Agent Skills](https://agentskills.io/) standard (Cursor, Claude Code, Codex, Gemini CLI, Google Antigravity, etc.).
- **OS**: macOS, Linux, or Windows with WSL2.

### Installing uv

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify with `uv --version`. For more options, see the [official uv docs](https://docs.astral.sh/uv/).

---

## 💡 Quick Examples

Once installed, ask your agent to run end-to-end research workflows. A few examples using skills in this collection:

### 📚 Systematic Literature Review
```
Search PubMed, arXiv, and bioRxiv via paper-lookup for recent work on CRISPR base
editing, pull structured experimental details with bgpt-paper-search, synthesize a
systematic review with literature-review, verify and format references with
citation-management, and write up the findings with scientific-writing.
```
**Skills used:** paper-lookup, bgpt-paper-search, literature-review, citation-management, scientific-writing

### 🔎 Reproducible Database Lookup
```
Use database-lookup to retrieve compound properties from PubChem and ChEMBL, map
target genes through UniProt and STRING, pull matching studies from
ClinicalTrials.gov, and report each result with its endpoint and provenance.
```
**Skills used:** database-lookup

### 📊 Data Analysis & Reporting
```
Load this large CSV with polars, run exploratory-data-analysis to profile it, choose
and run the right tests with statistical-analysis, build publication-quality figures
with scientific-visualization, and export the results to an Excel workbook with xlsx.
```
**Skills used:** polars, exploratory-data-analysis, statistical-analysis, scientific-visualization, xlsx

### 🤖 Machine Learning Pipeline
```
Train a classifier with scikit-learn (or pytorch-lightning for a neural net), reduce
dimensionality with umap-learn for visualization, explain predictions with shap, and
write up methods and results with scientific-writing.
```
**Skills used:** scikit-learn, pytorch-lightning, umap-learn, shap, scientific-writing

### 📈 Zero-Shot Forecasting
```
Forecast this sensor time series with timesfm-forecasting, cross-check against an
ARIMA baseline from statsmodels, and visualize forecasts with prediction intervals.
```
**Skills used:** timesfm-forecasting, statsmodels, scientific-visualization

> 📖 See [docs/examples.md](docs/examples.md) for more detailed workflow examples.

---

## 📚 Available Skills

This repository contains **72 skills**. The listings below are *explicitly defined* skills — curated with documentation, examples, and best practices. They are not a ceiling: your agent can install and use any Python package or call any API even without a dedicated skill; these simply make common workflows faster and more dependable.

### 🗄️ Databases & Data Access (2)
- **database-lookup** — Deterministic REST access to 78 public scientific, biomedical, materials, regulatory, finance, and demographics databases (PubChem, ChEMBL, UniProt, PDB, AlphaFold, KEGG, Reactome, STRING, ClinVar, COSMIC, ClinicalTrials.gov, FDA, FRED, USPTO, SEC EDGAR, and more) with explicit filters, pagination, and provenance.
- **hugging-science** — Curated catalog of scientific datasets, models, blog posts, and interactive Spaces across 17 domains, with usage patterns for `datasets`, `transformers`, the HF Inference API, and `gradio_client`.

### 🔎 Literature & Web Search (9)
- **paper-lookup** — Search 10 academic databases (PubMed, PMC, bioRxiv, medRxiv, arXiv, OpenAlex, Crossref, Semantic Scholar, CORE, Unpaywall).
- **bgpt-paper-search** — Structured experimental data (25+ fields per paper) extracted from full text via the BGPT MCP server.
- **literature-review** — Systematic, multi-database literature reviews with verified citations and formatted output.
- **citation-management** — Search, validate, and generate BibTeX; convert DOIs; ensure reference accuracy.
- **pyzotero** — Programmatic access to Zotero libraries via the Web API v3.
- **paperzilla** — Project recommendations, canonical paper details, and feed export via Paperzilla.
- **exa-search** — Web search and URL extraction tuned for scientific/scholarly content via Exa.
- **parallel-web** — All-in-one web toolkit (search, extraction, bulk enrichment, deep research) emphasizing academic sources.
- **research-lookup** — Routed current-research lookup across parallel-cli, the Parallel Chat API, and Perplexity.

### ✍️ Scientific Writing & Evaluation (4)
- **scientific-writing** — Manuscripts in flowing prose with IMRAD structure, citations, and reporting guidelines (CONSORT/STROBE/PRISMA).
- **peer-review** — Checklist-based manuscript/grant review with methodology and reporting-standards assessment.
- **scholar-evaluation** — Quantitative scholarly assessment via the ScholarEval framework.
- **venue-templates** — LaTeX templates and submission requirements for major journals, conferences, posters, and grants.

### 📄 Documents (6)
- **pdf** — Read, create, merge/split, OCR, fill forms, and manipulate PDF files.
- **docx** — Create, read, and edit Word documents with rich formatting.
- **pptx** — Create, read, and edit PowerPoint presentations.
- **xlsx** — Create, edit, and analyze Excel workbooks (formulas, multi-sheet, financial models).
- **markitdown** — Convert PDF/Office/images/audio/HTML and more to Markdown.
- **liteparse** — Local document/PDF parsing with bounding boxes, OCR, and layout-preserved JSON for RAG.

### 🎨 Presentations & Visuals (8)
- **scientific-slides** — Slide decks for research talks (PowerPoint and LaTeX Beamer).
- **latex-posters** — Conference posters in LaTeX (beamerposter, tikzposter, baposter).
- **pptx-posters** — HTML/CSS posters exportable to PDF or PPTX.
- **scientific-schematics** — Publication-quality diagrams (architectures, pathways, flowcharts) via AI generation.
- **scientific-visualization** — Meta-skill for journal-ready multi-panel figures with significance annotations and colorblind-safe palettes.
- **markdown-mermaid-writing** — Text-based diagrams and documents with style guides, diagram references, and templates.
- **infographics** — Professional infographics (10 types, 8 styles, colorblind-safe palettes).
- **generate-image** — General-purpose AI image generation and editing (FLUX, Nano Banana).

### 📊 Data Processing & Visualization (7)
- **polars** — High-performance, expression-based DataFrames with lazy/streaming execution.
- **dask** — Distributed computing for larger-than-RAM pandas/NumPy workflows.
- **vaex** — Out-of-core DataFrames for billions of rows on a single machine.
- **zarr-python** — Chunked, compressed N-D arrays for cloud-scale scientific data.
- **matplotlib** — Low-level plotting for full publication-grade control.
- **seaborn** — Statistical visualization with attractive defaults and pandas integration.
- **networkx** — Create, analyze, and visualize graphs and complex networks.

### 📐 Statistics & Experimental Design (5)
- **statistical-analysis** — Guided test selection, assumption checking, and APA-formatted reporting.
- **statistical-power** — A priori sample-size and power calculations (closed-form and simulation-based).
- **experimental-design** — Design studies before data collection (randomization, blocking, factorial/DOE, crossover, sequential).
- **exploratory-data-analysis** — Automated EDA across 200+ scientific file formats with quality metrics.
- **statsmodels** — Rigorous statistical models (OLS, GLM, mixed models, ARIMA) with diagnostics and inference.

### 🤖 Machine Learning & AI (12)
- **scikit-learn** — Classical supervised/unsupervised learning, model evaluation, and pipelines.
- **pytorch-lightning** — Organized, scalable neural-network training (multi-GPU, DDP/FSDP/DeepSpeed).
- **transformers** — Hugging Face models, pipeline inference, generation, and Trainer fine-tuning.
- **shap** — Model interpretability and feature attribution across model types.
- **umap-learn** — Nonlinear dimensionality reduction and embeddings.
- **torch-geometric** — Graph neural networks (GCN, GAT, GraphSAGE, GIN, heterogeneous graphs).
- **pymc** — Bayesian modeling, MCMC (NUTS), variational inference, and model comparison.
- **pymoo** — Multi-objective optimization (NSGA-II/III, MOEA/D, Pareto fronts).
- **aeon** — Time-series ML (classification, regression, clustering, forecasting, anomaly detection).
- **timesfm-forecasting** — Zero-shot univariate forecasting with Google's TimesFM foundation model.
- **stable-baselines3** — Production-ready RL algorithms with a scikit-learn-like API.
- **pufferlib** — High-performance, vectorized RL for fast parallel and multi-agent training.

### 🌍 Geospatial Science (2)
- **geomaster** — Remote sensing, GIS, spatial analysis, and Earth-observation ML (Sentinel/Landsat/MODIS/SAR, STAC/COG, 500+ examples).
- **geopandas** — Vector geospatial data: spatial joins, overlays, reprojection, and choropleth mapping.

### 🧮 Simulation & Mathematics (3)
- **simpy** — Process-based discrete-event simulation (queues, resources, logistics).
- **sympy** — Exact symbolic mathematics (algebra, calculus, symbolic linear algebra).
- **matlab** — MATLAB/GNU Octave numerical computing and Python interoperability.

### ⚙️ Infrastructure & Platforms (5)
- **modal** — Serverless cloud compute, on-demand GPUs, and scalable batch/inference jobs.
- **optimize-for-gpu** — GPU-accelerate Python with CuPy, Numba CUDA, Warp, and the RAPIDS stack (cuDF, cuML, cuGraph, …).
- **get-available-resources** — Detect CPU/GPU/memory/disk and recommend a computational strategy before heavy work.
- **pi-agent** — Build with and use Pi, the minimal terminal coding harness (SDK, RPC, extensions, packages).
- **autoskill** — Detect repeated research workflows locally via screenpipe and draft new skills for them.

### 🎓 Research Methodology & Ideation (9)
- **scientific-brainstorming** — Open-ended creative research ideation and gap-finding.
- **hypothesis-generation** — Structured, testable hypotheses with predictions and mechanisms.
- **hypogenic** — Automated LLM-driven hypothesis generation and testing on tabular data.
- **scientific-critical-thinking** — Evaluate claims and evidence quality (GRADE, Cochrane risk of bias).
- **consciousness-council** — Multi-perspective deliberation and devil's-advocate analysis.
- **what-if-oracle** — Structured what-if scenario analysis with 4–6 branch exploration.
- **arbor** — Autonomously improve an artifact against an evaluator via Hypothesis Tree Refinement, with a held-out gate against overfitting.
- **research-grants** — Competitive proposals for NSF, NIH, DOE, DARPA, and Taiwan NSTC.
- **open-notebook** — Self-hosted NotebookLM alternative for research notebooks, multi-source ingestion, and podcast generation.

> 📖 For full details on every skill, see [docs/skills.md](docs/skills.md).

---

## 📄 License

Licensed under the **MIT License** .

> ⚠️ **Individual skills may carry different licenses.** Each skill's license is in the `license` field of its `SKILL.md`. You are responsible for reviewing and complying with those terms.

