---
name: paper-reproduction-flow
description: "This skill should be used when the user provides a paper PDF, a paper text file, or a paper link, or issues a reproduction instruction such as 复现, 复现代码, reproduce this paper, or paper reproduction. It is especially suited to networking and security papers like BGP routing security, interdomain routing, RPKI or BGPsec, and simulation-driven systems papers. It orchestrates a multi-agent reproduction pipeline where the main agent is the Orchestrator (coordination only) and every other role is a NAMED subagent dispatched via the Agent tool. It auto selects the agent count by paper type (10 / 6 / 3), asks the user to pick an effort tier, creates an isolated dated RUN_WORKSPACE with a fixed folder layout (paper_text.txt, sources, results, datasets, logs, etc), and checks the environment before running. If the environment is insufficient, it stops and tells the user exactly what is missing."
agent_created: true
---

# Paper Reproduction Flow (多 Agent 论文复现流水线)

## Overview

把"论文复现"做成一条可调用、可复用、可反馈闭环的**真实多 Agent**流水线。

本技能的关键执行契约(务必遵守):

1. **主 Agent = 编排协调官(A0 · ORCH),只做协调,不做具体事务。**
   主 Agent 不得亲自撰写复现代码、运行实验、绘制图表或做统计验证。所有领域工作
   一律**通过 Agent 工具派发给对应命名子 Agent** 完成。主 Agent 只负责:
   建 `RUN_WORKSPACE`、维护任务依赖图、派发/并行调度子 Agent、回收产物、驱动
   "验证→归因→定向回溯"闭环、判定收敛、交付。
2. **每个 agent 都有名字与唯一职责。** 派发子 Agent 时,`description` 必须以角色
   代号开头(如 `ANALYST-解析Cohen2016`),使运行时可辨识"到底跑了哪些 agent"。
   角色命名表见下方 §Agent Roster 与 `references/agent_architecture.md` §A。
3. **agents 数量 = 1(协调官) + 所选档位里的角色子 Agent 数。** 选了几档就必须
   真派发几个子 Agent;即使"精简版 3 agents"也要派发 2 个子 Agent(复现 + 验证),
   协调官绝不把这两个角色合并到自己身上。
4. **先建隔离目录,后落盘**:本次复现的一切产物只进 `RUN_WORKSPACE`
   (`YYYYMMDD-论文核心机制`),按固定目录桶归位(见 §Workspace Layout)。

> 角色职责、共享工作台(Blackboard)结构、反馈闭环见 `references/agent_architecture.md`
> (含 **§G Agent 派发协议 / 波次表 / 子 Agent 提示词模板**)。
> 环境自检见 `scripts/env_check.py`;目录创建见 `scripts/create_run_workspace.py`。

---

## Agent Roster(命名与档位)

每个 agent 都有**代号 + 中文名 + 唯一职责**。协调官(A0)恒为主 Agent 本身,其余均为
被派发的命名子 Agent。三档配置如下(总数 = 1 协调官 + N 子 Agent):

### 完整版 · 10 agents(仿真 / 系统安全类,如 BGP 路由安全)
| # | 代号 | 名称 | 类型 | 唯一职责 |
|---|------|------|------|---------|
| A0 | ORCH | 编排协调官 Orchestrator | 主 Agent | 只协调:建目录、依赖图、派发/回溯、收敛判定、交付 |
| A1 | ANALYST | 论文解析师 Paper Analyst | 子 Agent | 论文→可复现清单(claim/预期值/容差/歧义) |
| A2 | ARCHITECT | 方法重构师 Method Architect | 子 Agent | prose→伪代码/数据结构 + 维护假设台账 |
| A3 | DATAENV | 数据与环境工程师 Data&Env | 子 Agent | 数据获取/对齐、环境锁定(依赖/种子/数据版本) |
| A4 | IMPL | 实现工程师 Implementation | 子 Agent | 按设计写代码 + 单测,不改方法 |
| A5 | RUNNER | 实验执行官 Experiment Runner | 子 Agent | 参数扫描、批量跑、记录 run manifest/日志 |
| A6 | VERIFIER | 验证分析师 Verifier | 子 Agent | 逐项 pass/fail 判定(只读不改)+ 统计检查 |
| A7 | DIAG | 调试归因师 Diagnostician | 子 Agent | 差异归五类根因、开定向回溯工单 |
| A8 | REPORTER | 可视化报告官 Reporter | 子 Agent | 复现图表 + 撰写复现报告 |
| A9 | CRITIC | 评审质控官 Critic | 子 Agent | 防过拟合、查基线公平、审假设披露 |

### 标准版 · 6 agents(实证 / 数据驱动 / ML 数值实验)
| # | 代号 | 名称 | 合并了谁 | 唯一职责 |
|---|------|------|---------|---------|
| A0 | ORCH | 编排协调官 Orchestrator | — | 只协调 |
| A1 | ANALYST | 论文解析师 Paper Analyst | +A2 方法重构 | 解析 + 方法设计 + 假设台账 |
| A3 | DATAENV | 数据与环境工程师 Data&Env | — | 数据 + 环境锁定 |
| A4 | IMPL | 实现执行工程师 Impl&Runner | +A5 执行 | 写代码 + 跑实验 + 记录 |
| A6 | VERIFIER | 验证分析师 Verifier | +A7 归因 | 判定 + 差异归因 |
| A8 | REPORTER | 可视化报告官 Reporter | +A9 质控 | 图表 + 报告 + 自评审 |

### 精简版 · 3 agents(理论 / 形式化 / 轻量复现)
| # | 代号 | 名称 | 合并了谁 | 唯一职责 |
|---|------|------|---------|---------|
| A0 | ORCH | 编排协调官 Orchestrator | — | 只协调 |
| R1 | REPRO | 复现工程师 Reproduction Eng. | A1+A2+A3+A4+A5+A8 | 解析→方法→数据→实现→执行→出图报告 |
| A6 | VERIFIER | 验证分析师 Verifier | +A7 归因 | 判定 + 差异归因 |

> **强制三件套**:协调官 + 复现主体 + 验证分析师。任何档位都不得少于此三,且后两者
> 必须是**真实派发的命名子 Agent**,不得由协调官兼任。合并只发生在同类相邻角色之间,
> 且"验证与复现分离"这条红线在任何档位都不合并。

---

## Workspace Layout(RUN_WORKSPACE 固定目录桶)

`scripts/create_run_workspace.py` 会在项目根下创建 `YYYYMMDD-<slug>/`,并预建以下固定结构。
**本次复现一切产物只进这里,按桶归位,不散落项目根。**

```
YYYYMMDD-<slug>/
├── paper_text.txt          # 论文可读文本(输入;所有子 Agent 从此读论文正文)
├── sources/                # 复现代码(A4/IMPL 维护)
├── datasets/               # 数据集合(A3/DATAENV 维护)
├── logs/                   # 代码日志 + 原始运行结果(A5/RUNNER 维护:manifest/stdout/raw)
├── results/                # 结果与分析产物
│   ├── repro_spec.md       #   可复现清单(A1/ANALYST)
│   ├── method_design.md    #   方法设计(A2/ARCHITECT)
│   ├── assumption_ledger.md#   假设台账(A2/ARCHITECT)
│   ├── verification_table.md#  逐项判定(A6/VERIFIER)
│   ├── review_notes.md     #   评审意见(A9/CRITIC)
│   ├── report.md           #   复现报告(A8/REPORTER)
│   ├── figures/            #   图表(A8/REPORTER)
│   └── diagnoses/          #   归因工单(A7/DIAG)
└── etc/                    # 需要用户定义的内容(参数覆盖、手工确认的高风险假设、配置)
```

> 目录桶与角色/Blackboard 的完整映射见 `references/agent_architecture.md` §C。

---

## When to Trigger

满足以下任一条件即自动调用本技能:

- 用户给出**论文文档**:PDF、`.txt` 全文、或含论文本体的文件。
- 用户给出**论文链接**(arXiv / ACM DL / 出版社页 / 开放获取仓库)。
- 用户发出**复现指令**:"复现这篇论文""复现代码""reproduce this paper"
  "paper reproduction" 等。
- 论文主题涉及**路由安全 / BGP / RPKI / BGPsec / 域间路由仿真 / 网络测量**
  等(当前最常见标定类型),或任何"用代码/实验重新得到论文结论"的任务。

---

## Workflow

### Step 1 — 解析论文(派发 A1 · ANALYST 子 Agent)

主 Agent(协调官)不要自己通读并产出规格书,而是**派发一个 Paper Analyst 子 Agent**:
用 Agent 工具, `subagent_type: "general-purpose"`, `description: "ANALYST-解析<论文短名>"`,
提示词包含角色卡(见 `references/agent_architecture.md` §B)、论文路径、`RUN_WORKSPACE`
路径、以及"产出 `results/repro_spec.md`"的要求。子 Agent 把论文翻译成可复现清单
(claim + 预期值/趋势 + 容差 + 数据集/指标 + 歧义点),并建议 slug。

**ANALYST 第一步必须穷举论文全部实验**(见 `agent_architecture.md` §B A1 更新):
产出 `results/repro_spec.md` 的 **§0 COVERAGE_INVENTORY** —— 论文中每张图、每个表、
每个原型/示例,逐条标注 scope: `in`(需复现)或 `out`(不在此次范围,须写理由)。
`out` 的正当理由示例:"需要不可获取的私有数据集""纯数学推导、无仿真""未来工作讨论、
非结论性实验"。用户可通过 `etc/` 覆盖 scope 决策。

> 若论文只有 PDF,ANALYST 需先抽取正文写入 `RUN_WORKSPACE/paper_text.txt`,供后续
> 子 Agent 统一读取(不再各自解析 PDF)。若项目根已有 `paper_text.txt`,见 Step 2 复制。

### Step 2 — 创建 RUN_WORKSPACE(协调官执行脚本)

协调官运行目录创建脚本(这是脚手架,非领域工作,可由主 Agent 直接执行):

```bash
python <skill>/scripts/create_run_workspace.py --slug <slug> --root <项目根> \
    [--paper-text <项目根>/paper_text.txt]
```

- 捕获打印出的绝对路径,记为 **`RUN_WORKSPACE`**;后续所有子 Agent 的读写都相对它。
- 目录名 `YYYYMMDD-<slug>`(如 `20260713-path-end-validation` / `20260713-pev`)。
- 自动预建 §Workspace Layout 的固定桶(`sources/ datasets/ logs/ results/{figures,diagnoses} etc/`)。
- `--paper-text` 若指向项目根已有的论文文本,会复制成 `RUN_WORKSPACE/paper_text.txt`;
  否则脚本写一个占位文件,由 ANALYST 后续填入正文。

> slug 推导:取论文核心机制/方法英文简称。Cohen 2016 PEV → `path-end-validation`
> (或 `pev`);RPKI ROV → `route-origin-validation`;BGPsec 部分部署 →
> `bgpsec-partial-deploy`。中文/空格会被自动净化。

### Step 3 — 判定论文类型并决定 agents 配置

按论文类型映射到档位与命名角色集(映射表见 `references/agent_architecture.md` §E)。
**硬性下限:至少含 ORCH + 复现主体 + VERIFIER 三个 agents。**

| 论文类型 | 推荐档位 | 命名角色(除 ORCH 外) |
|---------|---------|----------------------|
| 仿真/系统安全(BGP 路由安全、协议仿真) | 完整版 10 | ANALYST+ARCHITECT+DATAENV+IMPL+RUNNER+VERIFIER+DIAG+REPORTER+CRITIC |
| 实证/数据驱动(测量、数据集实验) | 标准版 6 | ANALYST+DATAENV+IMPL(含执行)+VERIFIER+REPORTER |
| ML/数值实验 | 标准版 6 | ANALYST+DATAENV+IMPL(含执行)+VERIFIER+REPORTER |
| 理论/形式化 | 精简版 3 | REPRO+VERIFIER |

> 无论哪种,**验证与复现必须分离**(验证只读不改、只判定对错),并维护
> **假设台账(Assumption Ledger)** 记录所有论文未写明、由本系统补全的假设。

### Step 4 — 让用户选择投入规模

调用 `AskUserQuestion` 给出档位选项(基于 Step 3 推荐上下浮动),并列出该档位**会派发的
具名 agents**,例如:

- **完整版(10 agents)**:ORCH + 9 子 Agent(见 §Agent Roster),高可信度,复杂仿真/系统论文。
- **标准版(6 agents)**:ORCH + 5 子 Agent,均衡,多数实证/数值论文。
- **精简版(3 agents)**:ORCH + REPRO + VERIFIER,快,理论或轻量复现。

同时说明每种档位的代价(耗时 / token / 可信度)。若 slug 未定,可在此一并请用户确认。
**用户选定后才进入执行。**

### Step 4b — 确认复现范围(新增)

在用户已确认 agents 投入规模、且 A1·ANALYST 已产出 `results/repro_spec.md`
(含 §0 COVERAGE_INVENTORY)之后,协调官读 COVERAGE_INVENTORY,汇总 scope=in 的实验
条目(含论文图号/表号/原型描述),调用 `AskUserQuestion` 让用户确认复现范围:

- **全部实验(推荐,默认)** — 复现 COVERAGE_INVENTORY 中所有 scope=in 的项。
  论文完整性最高。
- **仅核心图** — 只复现论文标志性主图/主要结论,跳过辅助性分析(Robustness tests、
  Geography-based deployment 等)。协调官将压缩范围写入 `etc/scope_override.md`,
  下游子 Agent(ARCHITECT/IMPL/RUNNER/VERIFIER/REPORTER)须读取该文件确定工作任务。
- **自定义** — 用户后续编辑 `etc/scope_override.md` 指定要复现的具体项。

若用户不回复(超时/跳过)或选"全部",采用默认"全部实验",不写 scope_override.md。
若选了非全部,协调官立即写 `etc/scope_override.md`,列明最终 scope=in 条目的图号/表号清单。
**下游每个子 Agent 在读取 repro_spec.md 时必须同时检查 scope_override.md,仅处理 scope=in 的项。**

### Step 5 — 运行环境自检

协调官运行 `scripts/env_check.py`(脚手架,可主 Agent 直接执行),传入项目根目录,
检查运行时 / 数据集 / 依赖 / 算力风险。

**若环境不满足**:停止后续步骤,用清单告诉用户"缺什么 + 怎么补",**不要**擅自联网
抓取或假装完成。待补齐后重跑自检。

### Step 6 — 按命名角色派发子 Agent 执行复现(核心)

**这是本技能与"只跑 2 个 agent"的根本区别。** 协调官依据所选档位,**逐角色派发命名
子 Agent**(每个角色 = 一次 Agent 工具调用 = 一个真实 agent,`description` 以角色代号
开头)。严格遵守 `references/agent_architecture.md` §G 的派发协议与波次表:

- 用 Agent 工具, `subagent_type: "general-purpose"`,每次提示词**必须自包含**:
  角色卡 + `RUN_WORKSPACE` 绝对路径 + 论文路径(`paper_text.txt`)+ 本角色要读的
  Blackboard 文件 + 要写的 Blackboard 文件 + 依赖(哪些上游角色的产出必须先存在)。
- 子 Agent 互不共享记忆,**只通过 `RUN_WORKSPACE` 下的文件(Blackboard)交接**。
- 独立角色在**同一条消息里并行派发多个 Agent 调用**;依赖角色等上游产物落盘后再派发。
- **协调官本人不写任何领域内容**,只在每波结束后读回 Blackboard 文件做决策。
- **验证不通过时的收敛规则(新增)**:
  若 W5 VERIFIER 存在 FAIL:
  (a) 协调官派发 A7/DIAG → `results/diagnoses/tickets.md`,每项偏差标注 convergence 状态;
  (b) 对 `must_fix` 项 → 协调官**必须**再次派发对应出错角色子 Agent 做定向回溯 → 回到 W4 重跑;
  (c) 对 `should_fix` 项 → 协调官用 `AskUserQuestion` 询问用户是否修;
  (d) 对 `disclose` 项 → DIAG 须在工单中写明**收敛理由**(为什么不修、若修需什么资源、偏差是否改变结论),协调官确认后入台账;
  (e) 协调官**不得**在存在 `must_fix` 未修复、且缺收敛理由的情况下进入 W7 报告阶段。
- **长任务(RUNNER 等仿真类)必须后台派发**(见 `agent_architecture.md` §G.6):
  RUNNER 用 `run_in_background: true` 派发,协调官正常 yield 等**系统通知**自动续跑,
  **不得 sleep 或轮询**。若会话中断导致未自动恢复,协调官须**幂等恢复**:
  任何重新进入(通知/手动重调/重载)都先读 Blackboard,按产物落盘情况从对应波次接续,
  不重跑已有产物。yield 时必须给用户输出明确的"恢复指引"(见 §G.6)。

完整版(10 agents)的波次与子 Agent 映射见 §G;标准/精简版按 §E 的命名角色集对应裁剪,
但**派发数量与所选档位一致**,不得合并进协调官。

### Step 7 — 评审 + 报告(派发 A9 · CRITIC → A8 · REPORTER)

**CRITIC 先审,REPORTER 后写**(见 `agent_architecture.md` §D 更新后的波次 8):
协调官先派发 A9 · CRITIC 子 Agent 做横切检查:
- 覆盖完整性:`repro_spec.md` 的 COVERAGE_INVENTORY 是否穷举了论文全部实验?
- 收敛完整性:每项 FAIL/COND-PASS 是否有修复或收敛理由?
- 防过拟合、基线公平、假设披露。
CRITIC **放行**后才派发 A8 · REPORTER 子 Agent 撰写 `results/report.md`
(含成功/偏差/假设/收敛理由/不可复现判定)。报告草稿可选再经 CRITIC 一审后交付用户。

---

## Notes / Guardrails

- **主 Agent 只协调**:严禁协调官亲自做解析/方法/代码/实验/绘图/验证等具体事务;
  这些必须派发命名子 Agent。允许协调官直接执行的两类脚手架:`create_run_workspace.py`
  与 `env_check.py`(非领域工作)。
- **agents 数量与命名要对得上**:选了 N 档就派发 N-1 个具名子 Agent,数量不可偷减;
  精简版也必须派发 REPRO 与 VERIFIER 两个子 Agent。
- **先建目录,后落盘**:一切产物只进 `RUN_WORKSPACE`,按 §Workspace Layout 的桶归位。
- **不要为凑数字反向调参**:偏离论文的假设/配置必须在假设台账与报告中显式披露。
- **三步不可省**:验证与复现分离、假设台账、环境不满足即停。
- **穷举全覆盖(新增)**:A1·ANALYST 必须穷举论文**全部实验**(图/表/原型),逐项 scope=in/out 并写理由,写进 repro_spec.md §0 COVERAGE_INVENTORY。遗漏实验视为 ANALYST 执行不合格,CRITIC 审查时打回。
- **收敛强制(新增)**:W5 VERIFIER 有 FAIL 时必须进入 W6 DIAG 归因。协调官对 `must_fix` 项必须回溯修复、不得跳过;对 `disclose` 项必须确保有收敛理由(为什么不修、修需要什么、偏差是否改变结论);CRITIC 不放行缺少收敛理由的报告。**不得在未修复的 FAIL 且无收敛理由的情况下交付。**
- **唤醒与恢复**:长任务后台派发(见 `agent_architecture.md` §G.6),协调官 yield 后等
  系统通知、不轮询;支持幂等恢复,会话中断时用户一句"继续复现"即可从已完成波次接续。
- 论文链接需全文而本机没有时,优先请用户下载至工作区,而非擅自大文件抓取。
- 标定样例:Cohen 等 2016《Jumpstarting BGP Security with Path-End Validation》
  (SIGCOMM),仿真型域间路由安全,slug 建议 `path-end-validation`(或 `pev`)。
  本工作区已含 `paper_text.txt`、`data/20160101.as-rel.txt.bz2`、`pev/` 代码骨架。
