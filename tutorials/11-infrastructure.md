# Tutorial — Infrastructure & Platforms (5 skills)

This category covers serverless compute, GPU acceleration, resource detection, a terminal coding harness, and auto-detecting repeated workflows. Use these to set up and scale your computing environment.

---

## 1. `modal`

**What it does.** Serverless cloud platform for running Python on demand, including **on-demand GPUs** — deploying/serving AI/ML models, GPU workloads (training, fine-tuning, inference), serving web endpoints, scheduling batch jobs, or scaling Python to cloud containers with the Modal SDK.

**Use it when** you need serverless compute — GPU workloads, model serving, batch jobs, or cloud scaling.

**Example scenario.** A ML team wants to serve a model on demand GPUs:
> "Use **modal** to deploy my fine-tuned model as a **serverless endpoint** on GPUs — schedule batch inference jobs and scale the containers."

---

## 2. `optimize-for-gpu`

**What it does.** GPU-accelerate Python code using **CuPy, Numba CUDA, Warp, cuDF, cuML, cuGraph, and the RAPIDS stack** — speed up NumPy, pandas, scikit-learn, scikit-image, NetworkX, GeoPandas, or Faiss workloads. Covers physics simulation, rendering, mesh ray casting, particle systems, vector search, GPUDirect Storage, dashboards, geospatial, medical imaging, and sparse eigensolvers.

**Use it when** you see CPU-bound Python (loops, large arrays, ML pipelines, graph analytics, image processing) that would benefit from GPU acceleration — even if not explicitly requested.

**Example scenario.** A data scientist wants to speed up a pandas-heavy pipeline:
> "Use **optimize-for-gpu** to **GPU-accelerate** my NumPy/pandas preprocessing — using cuDF and RAPIDS to cut the runtime of my ML pipeline."

---

## 3. `get-available-resources`

**What it does.** Detects and reports available **system resources** (CPU cores, GPUs, memory, disk) at the start of any computationally intensive task — producing a JSON with resource info and strategic recommendations (parallel via joblib/multiprocessing, out-of-core via Dask/Zarr, GPU via PyTorch/JAX, or memory-efficient strategies).

**Use it when** you're about to run an analysis, train a model, process large data, or any task where resource constraints matter.

**Example scenario.** A researcher about to train a large model wants to know what's available:
> "Use **get-available-resources** before I train this model — check CPU, GPU, memory, and disk, and recommend whether to use parallel or GPU acceleration."

---

## 4. `pi-agent`

**What it does.** Build with and use **Pi**, the minimal terminal coding harness — install Pi, configure providers/models/settings, create Pi skills/extensions/packages/themes/prompt templates, embed via the SDK, integrate over RPC or JSON event streams, parse sessions, develop custom Pi providers and TUI components, or use ecosystem packages (pi-subagents, pi-mcp-adapter, pi-interview, pi-web-access).

**Use it when** you want to build, use, or extend the Pi coding harness — delegating, MCP servers, interactive forms, or web access.

**Example scenario.** A developer wants to automate tasks in Pi:
> "Use **pi-agent** to set up **pi-subagents** in my Pi session — delegate a research task and integrate with **pi-web-access** for web search."

---

## 5. `autoskill`

**What it does.** Observes the user's screen via **screenpipe**, detects repeated research workflows, matches them against existing skills, and drafts **new skills** (or composition recipes that chain existing ones) for patterns not yet covered.

**Use it when** you want to analyze recent work and propose skills based on what you actually do. Requires the screenpipe daemon running locally on port 3030 (the skill refuses to run if screenpipe is unreachable).

**Example scenario.** A researcher wants to automate a recurring workflow:
> "Analyze my recent sessions with **autoskill** — detect my repeated literature-review workflow and draft a new skill or a recipe that chains existing ones."

---