# Tutorial — Research Methodology & Ideation (10 skills)

This category covers the research lifecycle — ideating, forming hypotheses, testing them, critical evaluation, multi-perspective deliberation, scenario exploration, autonomous improvement, grant writing, notebooks, and paper reproduction. Use these when you're planning, refining, or critically assessing research.

---

## 1. `scientific-brainstorming`

**What it does.** Creative research **ideation and exploration** — open-ended brainstorming, interdisciplinary connections, challenging assumptions, identifying research gaps. Best for early-stage research planning with no specific observations yet.

**Use it when** you need open-ended ideation or to explore research gaps. (For formulating testable hypotheses from data, use `hypothesis-generation`.)

**Example scenario.** A PI wants to explore new directions:
> "Use **scientific-brainstorming** to brainstorm **open questions in RNA therapeutics** — explore interdisciplinary connections and identify research gaps for my next proposal."

---

## 2. `hypothesis-generation`

**What it does.** Structured hypothesis formulation from observations — testable hypotheses with predictions, proposed mechanisms, and experiments to test them. Follows the scientific-method framework.

**Use it when** you have experimental observations/data and need to formulate testable hypotheses with predictions and mechanisms. (For open-ended ideation, use `scientific-brainstorming`; for automated LLM-driven hypothesis testing on datasets, use `hypogenic`.)

**Example scenario.** A researcher with pilot data wants formal hypotheses:
> "Use **hypothesis-generation** to formulate **testable hypotheses** from my pilot data — with predictions, proposed mechanisms, and experiments to test them."

---

## 3. `hypogenic`

**What it does.** **Automated LLM-driven hypothesis generation and testing** on tabular datasets — systematically explores hypotheses about patterns in empirical data (e.g., deception detection, content analysis). Combines literature insights with data-driven hypothesis testing.

**Use it when** you want to systematically explore hypotheses about patterns in empirical data. (For manual formulation use `hypothesis-generation`; for creative ideation use `scientific-brainstorming`.)

**Example scenario.** A social-science researcher wants to explore patterns in survey data:
> "Use **hypogenic** to **systematically generate and test hypotheses** about patterns in my survey dataset — combining literature insights with data-driven testing."

---

## 4. `scientific-critical-thinking`

**What it does.** Evaluates **scientific claims and evidence quality** — assessing experimental design validity, identifying biases and confounders, applying evidence grading frameworks (GRADE, Cochrane Risk of Bias), or teaching critical analysis.

**Use it when** you need to assess evidence quality, identify flaws in a design, or apply an evidence-grading framework. (For formal peer review writing, use `peer-review`.)

**Example scenario.** A reviewer wants to assess a claim's evidence:
> "Use **scientific-critical-thinking** to evaluate this **clinical claim's evidence quality** — check the experimental design for bias and apply the **GRADE** framework."

---

## 5. `consciousness-council`

**What it does.** Runs a multi-perspective **Mind Council deliberation** on any question, decision, or creative challenge — diverse viewpoints, devil's advocate, exploring a problem from multiple angles.

**Use it when** you want diverse viewpoints, help making a tough decision, a council/panel/board discussion, or devil's-advocate analysis — "what would different experts think", "think through this from all sides", "council mode".

**Example scenario.** A decision-maker facing a complex choice wants multiple perspectives:
> "Use **consciousness-council** to deliberate on whether to pursue **therapy A or B** for my patient cohort — I want a council of diverse experts and a devil's advocate."

---

## 6. `what-if-oracle`

**What it does.** Runs structured **What-If scenario analysis** with 4–6 branch exploration (best, likely, worst, wild card, contrarian, second-order) — speculative questions about uncertain futures, strategic forks, contingency planning, or stress-testing a decision.

**Use it when** you face speculative what-if questions, strategic forks, or need to stress-test a decision before committing.

**Example scenario.** A strategist wants to stress-test a launch decision:
> "Use **what-if-oracle** to explore the **best, likely, worst, and wild-card scenarios** for launching my new product — testing the decision before I commit."

---

## 7. `arbor`

**What it does.** Autonomously improves a real artifact (code, training recipe, agent harness, data pipeline, prompt) against an objective and an evaluator, using **Hypothesis Tree Refinement (HTR)** — iterative experiment-and-evaluate loops without overfitting.

**Use it when** you want to iteratively optimize something over many experiments — "get my model's eval score up", "improve this agent/harness", "tune this pipeline", "beat the baseline on this benchmark", "run a search over approaches and keep the best", "do an MLE-bench / Kaggle-style optimization".

**Example scenario.** A researcher wants to beat a benchmark on an eval:
> "Use **arbor** to iteratively optimize my pipeline to **beat the baseline on this benchmark** — run many experiments with Hypothesis Tree Refinement and keep the best, without overfitting to the dev set."

---

## 8. `research-grants`

**What it does.** Writes competitive research proposals for **NSF, NIH, DOE, DARPA, and Taiwan NSTC** — agency-specific formatting, review criteria, budget preparation, broader impacts, significance, innovation narratives, and compliance.

**Use it when** you need a competitive grant proposal with agency-specific formatting and review-criteria alignment.

**Example scenario.** A researcher wants a competitive NIH proposal:
> "Use **research-grants** to draft my **NIH R01 proposal** — with significance statements, innovation narrative, budget preparation, and compliance with NIH review criteria."

---

## 9. `open-notebook`

**What it does.** Self-hosted, open-source alternative to **NotebookLM** for AI-powered research and document analysis — organizing research into notebooks, ingesting diverse sources (PDFs, videos, audio, web, Office), generating AI notes and summaries, creating multi-speaker podcasts, chatting with documents, and full-text/vector search. Supports 16+ AI providers with complete data privacy via self-hosting.

**Use it when** you need to organize research materials into notebooks, ingest diverse content, generate AI summaries/podcasts, or chat with documents.

**Example scenario.** A researcher wants to organize a literature corpus into notebooks:
> "Use **open-notebook** to ingest my **PDFs, web pages, and videos** into research notebooks — generate AI notes and summaries, and build a multi-speaker podcast from my findings."

---

## 10. `paper-reproduction-flow`

**What it does.** Orchestrates a **multi-agent paper reproduction pipeline** (Orchestrator + named subagents) for reproducing papers from a PDF/URL/text — auto-selects agent count by paper type (10/6/3), asks for an effort tier, creates an isolated dated RUN_WORKSPACE, and checks the environment. Especially suited to networking/security papers (BGP routing, interdomain routing, RPKI, BGPsec) and simulation-driven systems papers.

**Use it when** the user provides a paper PDF, a paper text file, or a paper link, or issues a reproduction instruction like **复现, 复现代码, reproduce this paper**, or paper reproduction.

**Example scenario.** A researcher wants to reproduce a networking paper's experiments:
> "Reproduce the experiments in this **BGP routing-security paper** with **paper-reproduction-flow** — I'll pick the effort tier, and you'll orchestrate the subagents to verify the results."

---