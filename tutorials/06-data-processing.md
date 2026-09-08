# Tutorial — Data Processing & Visualization (7 skills)

This category covers high-performance and out-of-core dataframes, chunked arrays, and plotting. Use them when you need to load, transform, analyze, or visualize scientific data efficiently.

---

## 1. `polars`

**What it does.** High-performance **DataFrame library** for Python ETL, analytics, and pandas migration — expression-based manipulation with lazy query optimization, parallel execution, streaming out-of-core processing, Arrow interoperability, and optional GPU execution.

**Use it when** you need fast, memory-efficient data manipulation of large tabular data — expression-based, lazy, or streaming — especially as an alternative to pandas.

**Example scenario.** A data analyst wants to process a large CSV quickly:
> "Load this **2M-row sales CSV** with **polars**, do lazy expression-based filtering and aggregation, and compute the per-region totals in parallel."

---

## 2. `dask`

**What it does.** Distributed computing for **larger-than-RAM** pandas/NumPy workflows — scales existing pandas/NumPy code beyond memory or across clusters. Best for parallel file processing, distributed ML, and integration with existing pandas code.

**Use it when** you need to scale existing pandas/NumPy beyond memory or across clusters. (For out-of-core analytics on a single machine use `vaex`; for in-memory speed use `polars`.)

**Example scenario.** A lab wants to analyze a dataset that exceeds RAM:
> "Use **dask** to run this pandas workflow on a **20GB dataset** across my cluster — parallel file reads and distributed aggregation."

---

## 3. `vaex`

**What it does.** Processes and analyzes **billions-of-rows tabular datasets** that exceed available RAM — out-of-core DataFrame operations, lazy evaluation, fast aggregations, efficient big-data visualization, and ML on large datasets.

**Use it when** you need to work with huge CSV/HDF5/Arrow/Parquet files, run fast statistics on massive datasets, visualize big data, or build ML pipelines that don't fit in memory.

**Example scenario.** A researcher wants fast stats on a massive dataset:
> "Use **vaex** to compute **summary statistics on this 5B-row genomics dataset** out-of-core, and produce quick visualizations without loading it into memory."

---

## 4. `zarr-python`

**What it does.** Chunked, compressed **N-D arrays** for cloud storage (Zarr-Python 3) — parallel I/O, S3/GCS via fsspec, NumPy/Dask/Xarray compatible, for large-scale scientific computing pipelines.

**Use it when** you need chunked, compressed arrays for cloud-scale scientific data that must be accessed in parallel.

**Example scenario.** A climate scientist wants to store and stream a huge simulation output:
> "Use **zarr-python** to store this **CMIP climate simulation** as chunked compressed arrays on S3, and stream it in parallel with Dask."

---

## 5. `matplotlib`

**What it does.** Low-level plotting library for full customization — fine-grained control over every plot element, novel plot types, and integration with specific scientific workflows. Export to PNG/PDF/SVG for publication.

**Use it when** you need precise, customizable plots. (For quick statistical plots use `seaborn`; for interactive use `plotly`; for publication-ready multi-panel figures use `scientific-visualization`.)

**Example scenario.** A researcher wants a highly customized plot:
> "Use **matplotlib** to build a **custom spectrogram plot** with exact axis scaling, color mapping, and annotations, exported to PDF for my paper."

---

## 6. `seaborn`

**What it does.** Statistical visualization with pandas integration and attractive defaults — box plots, violin plots, pair plots, heatmaps, and categorical comparisons. Built on matplotlib.

**Use it when** you need quick exploration of distributions, relationships, and categorical comparisons with clean defaults.

**Example scenario.** A analyst wants to explore a dataset visually:
> "Use **seaborn** to make a **pair plot and heatmap** of my survey data — distributions and correlations — for quick EDA."

---

## 7. `networkx`

**What it does.** Create, analyze, and visualize **complex networks and graphs** in Python — graph algorithms (shortest paths, centrality, clustering), community detection, synthetic networks (random, scale-free, small-world), file format read/write, and network topology drawing.

**Use it when** you work with network/graph data structures — social, biological, transportation, or citation networks.

**Example scenario.** A sociologist wants to analyze a collaboration network:
> "Use **networkx** to build and analyze my co-authorship network — compute **centrality and community structure**, and draw the topology for my paper."

---