# Tutorial — Machine Learning & AI (12 skills)

This category covers classical ML, deep learning, transformers, model interpretability, dimensionality reduction, graph neural networks, Bayesian modeling, multi-objective optimization, time-series ML, forecasting, and reinforcement learning. Use these when you're training, evaluating, or explaining models.

---

## 1. `scikit-learn`

**What it does.** Machine learning in Python with scikit-learn — supervised learning (classification, regression), unsupervised (clustering, dimensionality reduction), model evaluation, hyperparameter tuning, preprocessing, and building ML pipelines.

**Use it when** you need classical ML — a classifier, regressor, clustering, or a full pipeline with evaluation and tuning.

**Example scenario.** A data analyst wants a predictive model:
> "Use **scikit-learn** to build a **classifier for loan default** — preprocess the features, train a random forest, evaluate with cross-validation, and tune the hyperparameters."

---

## 2. `pytorch-lightning`

**What it does.** Deep learning framework (PyTorch Lightning) — organize PyTorch into LightningModules, configure Trainers for multi-GPU/TPU, data pipelines, callbacks, logging (W&B, TensorBoard, MLflow), and distributed training (DDP, FSDP, DeepSpeed).

**Use it when** you need scalable, organized neural-network training — multi-GPU, distributed, or with rich logging.

**Example scenario.** A deep-learning researcher wants scalable training:
> "Use **pytorch-lightning** to train a **vision transformer** with a LightningModule — multi-GPU DDP, TensorBoard logging, and a clean data pipeline."

---

## 3. `transformers`

**What it does.** Hugging Face Transformers — load Hub models, run pipeline inference, text generation, and **Trainer fine-tuning** on NLP, vision, audio, and multimodal tasks.

**Use it when** you work with AutoModel, pipelines, tokenizers, or TrainingArguments — fine-tuning a pretrained model or running inference.

**Example scenario.** An NLP engineer wants to fine-tune a model:
> "Use **transformers** to load a pretrained **BERT** model, fine-tune it with Trainer on my sentiment dataset, and run pipeline inference on new text."

---

## 4. `shap`

**What it does.** Model interpretability and explainability using **SHAP** — feature importance, SHAP plots (waterfall, beeswarm, bar, scatter, force, heatmap), model debugging, bias/fairness analysis, and explainable AI.

**Use it when** you need to explain model predictions, compute feature importance, or debug/bias-check a model.

**Example scenario.** A ML team wants to explain a model's decisions:
> "Use **shap** to explain my credit-model's predictions — generate **beeswarm and waterfall plots** showing which features drove each decision."

---

## 5. `umap-learn`

**What it does.** Nonlinear dimensionality reduction and embeddings with UMAP — 2D/3D embeddings, clustering preprocessing, supervised/semi-supervised UMAP, DensMAP, AlignedUMAP, Parametric UMAP.

**Use it when** you need to reduce high-dimensional data for visualization, clustering preprocessing, or embedding workflows.

**Example scenario.** A genomics researcher wants to visualize high-dimensional data:
> "Use **umap-learn** to project my **single-cell expression data** into 2D — reducing dimensionality for clustering and a scatter visualization."

---

## 6. `torch-geometric`

**What it does.** PyTorch Geometric (PyG) for **graph neural networks** — node/link/graph classification, message passing (GCN, GAT, GraphSAGE, GIN), heterogeneous graphs, neighbor sampling, and custom datasets.

**Use it when** you work with `torch_geometric` for graph models — not for general NetworkX analytics or non-graph PyTorch models.

**Example scenario.** A graph-ML researcher wants to classify nodes in a network:
> "Use **torch-geometric** to train a **GAT** on my protein-interaction graph — node classification with message passing and neighbor sampling."

---

## 7. `pymc`

**What it does.** Bayesian modeling with PyMC — hierarchical models, MCMC (NUTS), variational inference, LOO/WAIC comparison, posterior checks, for probabilistic programming and inference.

**Use it when** you need Bayesian modeling — uncertainty quantification, hierarchical structure, or probabilistic inference.

**Example scenario.** An epidemiologist wants Bayesian inference on an outbreak:
> "Use **pymc** to build a **hierarchical Bayesian model** for my infection-rate data — fit with NUTS MCMC and compare candidate models with WAIC."

---

## 8. `pymoo`

**What it does.** Multi-objective optimization framework — NSGA-II, NSGA-III, MOEA/D, Pareto fronts, constraint handling, benchmarks (ZDT, DTLZ), for engineering design and optimization.

**Use it when** you face multi-objective trade-offs — conflicting objectives, Pareto fronts, or constrained design optimization.

**Example scenario.** An engineer wants to optimize conflicting objectives:
> "Use **pymoo** to run **NSGA-II** on my truss design — minimize cost and weight simultaneously, and show the **Pareto front**."

---

## 9. `aeon`

**What it does.** Time-series ML with scikit-learn-compatible APIs — classification, regression, clustering, forecasting, anomaly detection, segmentation, and similarity search on temporal data.

**Use it when** you work with temporal data, sequential patterns, or time-indexed observations requiring specialized algorithms beyond standard ML.

**Example scenario.** A biologist wants to classify biosignals over time:
> "Use **aeon** to **classify my ECG time series** — train a time-series classifier and detect anomalies in the signal."

---

## 10. `timesfm-forecasting`

**What it does.** **Zero-shot time-series forecasting** with Google's TimesFM foundation model — univariate series (sales, sensors, energy, vitals, weather) without training a custom model, with point forecasts and prediction intervals. Includes a preflight system checker for RAM/GPU.

**Use it when** you need a fast forecast for a univariate time series without building a custom forecasting model.

**Example scenario.** A retailer wants to forecast next quarter's sales:
> "Use **timesfm-forecasting** to **forecast my daily sales series** for the next 90 days — point forecasts with prediction intervals, no custom training."

---

## 11. `stable-baselines3`

**What it does.** Production-ready reinforcement learning algorithms (PPO, SAC, DQN, TD3, DDPG, A2C) with a scikit-learn-like API — standard RL experiments, quick prototyping, and documented implementations for single-agent RL with Gymnasium.

**Use it when** you want standard, well-documented RL. (For high-performance parallel training, multi-agent, or custom vectorized environments, use `pufferlib`.)

**Example scenario.** A robotics team wants to train a control policy:
> "Use **stable-baselines3** to train **PPO** on my Cartpole gym environment — quick prototyping with a standard, well-documented RL algorithm."

---

## 12. `pufferlib`

**What it does.** High-performance reinforcement learning framework optimized for speed and scale — fast parallel training, vectorized environments, multi-agent systems, and integration with game environments (Atari, Procgen, NetHack). Achieves 2–10x speedups over standard implementations.

**Use it when** you need speed and scale — parallel training, multi-agent, or custom vectorized environments. (For quick prototyping, use `stable-baselines3`.)

**Example scenario.** A research team wants to scale multi-agent RL:
> "Use **pufferlib** to run **vectorized parallel training** for my multi-agent Atari experiment — targeting a 10x speedup over standard single-agent RL."

---