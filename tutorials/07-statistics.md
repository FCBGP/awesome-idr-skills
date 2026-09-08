# Tutorial — Statistics & Experimental Design (5 skills)

This category covers designing studies before data collection, computing power/sample size, analyzing data with the right tests, automated EDA, and rigorous statistical modeling. Use these to plan, analyze, and report research.

---

## 1. `statistical-analysis`

**What it does.** Guided statistical analysis with **test selection** and reporting — choosing appropriate tests for your data, assumption checking, power analysis, and **APA-formatted results**. Best for academic research reporting.

**Use it when** you need help choosing a test, checking assumptions, or producing APA-style results. (For implementing specific models programmatically, use `statsmodels`.)

**Example scenario.** A researcher analyzing survey data wants APA results:
> "Use **statistical-analysis** to choose the right test for my survey data (Likert vs. continuous), check assumptions, and report the result in **APA format**."

---

## 2. `statistical-power`

**What it does.** Sample-size and statistical power calculations for planning studies — a priori power analysis, minimum detectable effect (MDE), power curves, and sample-size justification for grants, IRB protocols, or pre-registration. Covers closed-form power for t-tests/ANOVA/proportions/correlations/chi-square/regression, plus Monte Carlo simulation power for designs without a formula (logistic/Poisson regression, mixed models, cluster-randomized trials, survival, interactions).

**Use it when** you're asked "how many subjects/samples/replicates do I need" or you need to justify a sample size. Trigger it even if the request only mentions an effect size, alpha, or "80% power" without saying "power analysis" explicitly.

**Example scenario.** A clinical trial planner wants a sample-size justification:
> "How many patients do I need for this RCT to detect a **0.15 effect size at 80% power with alpha 0.05**? Use **statistical-power** to give me a power curve and a defensible sample size."

---

## 3. `experimental-design`

**What it does.** Design experiments and studies **BEFORE data is collected** — choosing a design, randomizing, blocking, and laying out treatment combinations so results are interpretable. Covers randomization, blocking, stratification, controls, factorial/fractional-factorial, DOE, screening, response-surface, crossover, repeated-measures, split-plot, cluster randomization, Latin squares, plate layouts, batch effects, replication vs. pseudoreplication, sequential designs.

**Use it when** you're planning a study, assigning subjects/samples to groups, or want to avoid confounding. Trigger it even for informal phrasings like "how should I set up this experiment" or "assign these mice to conditions." (For sample size/power, use `statistical-power`; for analyzing data already collected, use `statistical-analysis`.)

**Example scenario.** A biologist wants to set up a dose-response study cleanly:
> "Use **experimental-design** to design my **6-factor dose-response screen** — assign the 96-well plate layout, block for batch effects, and avoid confounding."

---

## 4. `exploratory-data-analysis`

**What it does.** Performs comprehensive **EDA on scientific data files across 200+ formats** — auto-detects file type and generates detailed Markdown reports with format-specific analysis, quality metrics, and downstream analysis recommendations. Covers chemistry, bioinformatics, microscopy, spectroscopy, proteomics, metabolomics, and general formats.

**Use it when** you need to understand the structure, content, quality, and characteristics of any scientific data file.

**Example scenario.** A proteomics lab wants to profile an unfamiliar dataset:
> "Use **exploratory-data-analysis** on this **mass-spectrometry file** — detect the format, profile quality metrics, and recommend what downstream analyses to run."

---

## 5. `statsmodels`

**What it does.** Statistical models library for Python — specific model classes (OLS, GLM, mixed models, ARIMA) with detailed diagnostics, residuals, and inference. Best for econometrics, time series, and rigorous inference with coefficient tables.

**Use it when** you need a specific model class with detailed diagnostics. (For guided test selection with APA reporting, use `statistical-analysis`.)

**Example scenario.** An econometrician wants rigorous model diagnostics:
> "Use **statsmodels** to fit an **ARIMA** model to my GDP series — report the coefficients, residuals, and diagnostics for my regression table."

---