# 多 Agent 论文复现 · 角色架构与协作机制(详细参考)

> 本文档供本技能在执行时按需加载,描述**命名角色**的精确职责、共享工作台结构、
> "执行→验证→归因→回溯"闭环、"论文类型 → agents 配置"映射,以及
> **§G Agent 派发协议**(主 Agent 如何把每个命名角色派发为真实子 Agent)。

## A. 角色总览(命名注册表)

每个 agent 都有**代号 + 中文名 + 唯一职责**。协调官(A0)恒为主 Agent 本身,其余均为
被派发的命名子 Agent。派发时 `description` 以代号开头,便于运行时辨识真实 agent 数量。

| 层 | 代号 | 角色 | 是否子 Agent | 定位 | 核心产物 |
|----|------|------|------------|------|---------|
| 协调 | A0 · ORCH | 编排协调官 Orchestrator | **否(=主 Agent)** | 复现"项目负责人",只协调 | 任务依赖图、状态、收敛决策 |
| ①理解 | A1 · ANALYST | 论文解析师 Paper Analyst | 是 | 把论文翻译成可复现清单 | `results/repro_spec.md` |
| ①理解 | A2 · ARCHITECT | 方法重构师 Method Architect | 是 | 把 prose 变可实现方法 | `results/method_design.md` + `results/assumption_ledger.md` |
| ②构建 | A3 · DATAENV | 数据与环境工程师 Data&Env | 是 | 供好数据+可复现环境 | `datasets/` + `results/env_lock.md` |
| ②构建 | A4 · IMPL | 实现工程师 Implementation | 是 | 把方法落成代码 | `sources/` |
| ③执行 | A5 · RUNNER | 实验执行官 Experiment Runner | 是 | 跑实验、管扫描 | `logs/`(manifest/日志/原始结果) |
| ③执行 | A6 · VERIFIER | 验证分析师 Verifier | 是 | 判定每项是否成功(只读不改) | `results/verification_table.md` |
| ③执行 | A7 · DIAG | 调试归因师 Diagnostician | 是 | 定位差异根因、开回溯工单 | `results/diagnoses/tickets.md` |
| ④交付 | A8 · REPORTER | 可视化报告官 Reporter | 是 | 复现图表+报告 | `results/figures/` + `results/report.md` |
| 质控 | A9 · CRITIC | 评审质控官 Critic | 是(横切) | 防过拟合、守科学性 | `results/review_notes.md`(放行/打回) |

精简版专用合并角色:

| 代号 | 角色 | 合并了谁 | 唯一职责 |
|------|------|---------|---------|
| R1 · REPRO | 复现工程师 Reproduction Engineer | A1+A2+A3+A4+A5+A8 | 解析→方法→数据→实现→执行→出图报告 |

**强制三件套**:A0(主 Agent)+ 复现主体 + A6/VERIFIER。任何档位都不得少于此三,
且后两者必须是**真实派发的命名子 Agent**,不得由协调官兼任。

> **关键区分**:除 A0/ORCH 是主 Agent 本身外,其余角色都是被派发的子 Agent。
> 选 N 档 = 主 Agent + (N-1) 个命名子 Agent。三档命名清单见 SKILL.md §Agent Roster。

## B. 角色卡片(职责要点)

### A0 · ORCH 编排协调官 Orchestrator(=主 Agent,只协调)
拆复现目标为"可复现单元"→ 建任务依赖图 → **逐角色派发命名子 Agent** → 回收 Blackboard
产物 → 驱动反馈闭环 → 判定收敛。产物:任务图、进度、每轮决策、结论汇总。
**禁止亲自做**:解析/方法设计/写代码/跑实验/绘图/统计验证。只允许直接执行两个脚手架脚本
(`create_run_workspace.py`、`env_check.py`)。

### A1 · ANALYST 论文解析师 Paper Analyst
**第一步(必须)**:穷举论文中**全部**实验、图、表、原型实现。对每一项标注 scope:
`in`(需要复现,需仿真/代码)或 `out`(不在此次复现范围)。`out` 必须写明理由,如"需要不可获取的数据集""纯数学推导""未来工作讨论、非结论性实验"。
穷举结果写入 `results/repro_spec.md` 的 **§0 覆盖率清单**(COVERAGE_INVENTORY),列:编号|图表名|scope|理由(out 时必填)。
第二步:对 scope=in 的项,产出结构化条目:①claim 清单;②每条对应图/表与**预期数值/曲线趋势 + 容差**;③数据集、指标定义、关键参数;④**歧义清单**;⑤建议 slug。只回答"要复现什么、达到什么数才算成功",不写代码。

### A2 · ARCHITECT 方法重构师 Method Architect
把方法还原为伪代码+数据结构+参数表;对论文没写全处做有据可依的假设,全部登记进
`results/assumption_ledger.md`。仿真类论文成败关键。高风险假设须升级给用户确认。
若 `etc/scope_override.md` 存在(用户选了非全部实验),只对 scope=in 的条目做方法设计。

### A3 · DATAENV 数据与环境工程师 Data&Env
获取/对齐数据集、预处理与关系推断;必要时给合成数据;锁定运行环境(依赖版本、随机
种子、数据版本)。产出清洗后数据集(`datasets/`)、拓扑对象、`results/env_lock.md`。

### A4 · IMPL 实现工程师 Implementation
严格按设计落地代码(写入 `sources/`),写单测保证与伪代码一致,关注规模与性能(全网仿真
需高效/抽样)。不自行改方法。若 `etc/scope_override.md` 存在,仅实现 scope=in 项所需的实验代码。

### A5 · RUNNER 实验执行官 Experiment Runner
管理配置与参数扫描(部署比例、top-k、种子等),批量执行,完整记录每个 run 的配置/
环境/原始输出/日志到 `logs/`,保证可追溯。产物:`logs/` 下 manifest 与日志。
若 `etc/scope_override.md` 存在,仅跑 scope=in 项对应的实验,不浪费算力在 excluded 项上。

### A6 · VERIFIER 验证分析师 Verifier(只读不改)
把原始结果与 `results/repro_spec.md` 预期值/趋势对齐,逐项给 pass/fail 与偏差(delta、
趋势、容差);做统计检查(方差、样本量)。**不修复任何东西**,只判定,写
`results/verification_table.md`。若 `etc/scope_override.md` 存在,仅对照 scope=in 的条目做判定,
其余标为 N/A(out-of-scope)。

### A7 · DIAG 调试归因师 Diagnostician
差异归类到**五类根因**,开**定向回溯工单**(`results/diagnoses/tickets.md`)给对应上游:
1. 读错目标/指标 → A1 · ANALYST
2. 假设/方法有误 → A2 · ARCHITECT
3. 数据不一致 → A3 · DATAENV
4. 实现 bug → A4 · IMPL
5. 配置错/采样不足 → A5 · RUNNER
并能判定"论文本身可能不可复现"并上报协调官。**只回溯到出错那一环,不整体重来。**

**每项偏差必须给收敛状态**: `must_fix`(影响结论方向,必须修复) / `should_fix`(改善精度,建议修复) / `disclose`(披露即可,不改变结论)。对于 `should_fix` 和 `disclose`,须写**收敛理由**:为什么不修、若修需要什么资源(数据/算力/代码改动量)、当前偏差是否改变定性结论。

### A8 · REPORTER 可视化报告官 Reporter
按论文风格重画图表(与原图并排,写入 `results/figures/`),撰写复现报告(写入
`results/report.md`):成功/偏差/原因/假设/结论。草稿交 CRITIC,定稿交用户。
若 `etc/scope_override.md` 存在,报告中须明确标注本次复现范围(哪些图/实验在范围内,
哪些被排除),避免读者误认为覆盖了论文全部实验。

### A9 · CRITIC 评审质控官 Critic(横切)
审查是否反向调参过拟合;比较是否公平(基线、口径一致);假设是否合理且已披露;结论
是否被证据支持。在方法定稿、报告定稿节点可**放行/打回**,写 `results/review_notes.md`。

**必须额外检查**(新增):
1. **覆盖完整性**: `repro_spec.md` 的 COVERAGE_INVENTORY 是否穷举了论文全部实验? 若有遗漏,打回 A1·ANALYST 补全。
2. **收敛完整性**: 对每个 FAIL/COND-PASS, `diagnoses/tickets.md` 是否有修复记录(回溯已执行)或收敛理由(为何不修)? 缺少收敛理由的 FAIL 不得放行,打回 A7·DIAG 补理由。

### R1 · REPRO 复现工程师 Reproduction Engineer(仅精简版)
在精简版一人承担 A1+A2+A3+A4+A5+A8:读论文→定规格→设计方法+记假设→备数据→写代码
→跑实验→出图与报告草稿。产物覆盖对应文件。**但绝不自任验证**——判定必须交 A6/VERIFIER。

## C. 共享工作台 Blackboard(数据结构 → 目录桶映射)

所有子 Agent 读写同一份结构化状态,统一放在 **`RUN_WORKSPACE`** 下(由
`scripts/create_run_workspace.py` 创建,命名 `YYYYMMDD-论文核心机制`)。目录桶与角色映射:

| 目录桶 / 文件 | 归属角色 | 说明 |
|--------------|---------|------|
| `paper_text.txt` | A1/ANALYST(写) | 论文可读文本;所有子 Agent 从此读论文正文 |
| `sources/` | A4/IMPL | 复现代码 |
| `datasets/` | A3/DATAENV | 数据集合(清洗后) |
| `logs/` | A5/RUNNER | 代码日志 + 原始运行结果(manifest/stdout/raw) |
| `results/repro_spec.md` | A1/ANALYST | 可复现清单 |
| `results/method_design.md` | A2/ARCHITECT | 方法设计/伪代码 |
| `results/assumption_ledger.md` | A2/ARCHITECT | 假设台账 |
| `results/env_lock.md` | A3/DATAENV | 环境锁定 |
| `results/verification_table.md` | A6/VERIFIER | 逐项 pass/fail |
| `results/diagnoses/tickets.md` | A7/DIAG | 回溯工单 |
| `results/figures/` | A8/REPORTER | 图表 |
| `results/report.md` | A8/REPORTER | 复现报告 |
| `results/review_notes.md` | A9/CRITIC | 评审放行/打回 |
| `etc/scope_override.md` | 协调官(写) / 全下游(读) | 用户选定的复现范围(若非"全部实验");ARCHITECT/IMPL/RUNNER/VERIFIER/REPORTER 须读此文件,仅处理 scope=in 的项 |
| `etc/` | 用户 / 协调官 | 用户自定义内容:参数覆盖、手工确认的高风险假设、配置 |

> 子 Agent 互不共享记忆;角色间**只通过 `RUN_WORKSPACE` 文件交接**。协调官在每波
> 结束后读回这些文件做决策。`etc/` 是用户输入面:高风险假设需用户拍板时,协调官把
> 待确认项写入 `etc/`,用户回填后子 Agent 再读取。

## D. 主流程与反馈闭环

1. 协调官建 `RUN_WORKSPACE`(+放 `paper_text.txt`)→ 派发 A1/ANALYST → `results/repro_spec.md`。
2. 派发 A2/ARCHITECT → `results/method_design.md` + `results/assumption_ledger.md`(依赖 1)。
3. 并行派发 A3/DATAENV + A4/IMPL(依赖 2)。
4. 派发 A5/RUNNER → `logs/`(依赖 3)。
5. 派发 A6/VERIFIER → `results/verification_table.md`(依赖 4)。
6. **通过** → 跳至 8。
   **不通过**(存在 FAIL) → 派发 A7/DIAG → `results/diagnoses/tickets.md`。
7. 协调官读 tickets.md:对 `must_fix` 项**必须派发回溯**(再次派发出错角色子 Agent)并回到 4;对 `should_fix` 项询问用户是否修;对 `disclose` 项入台账。**不得在 must_fix 未修复、且缺少收敛理由的情况下进入报告阶段。**
8. 派发 A9/CRITIC (横切检查覆盖完整性 + 收敛完整性)→ 通过后派发 A8/REPORTER → 交付。

闭环要点:只回溯到出错环节;每次回溯在台账/工单留痕,供 CRITIC 复核,防止反复调参
中悄然过拟合。

## E. 论文类型 → agents 配置映射

| 类型 | 判定线索 | 默认档位 | 命名角色子 Agent(除 A0/ORCH 外) | 子 Agent 数 |
|------|---------|---------|--------------------------------|-----------|
| 仿真/系统安全(BGP 路由安全、协议仿真) | 有拓扑/仿真、攻击模型、隐含策略假设 | 完整版 10 | ANALYST+ARCHITECT+DATAENV+IMPL+RUNNER+VERIFIER+DIAG+REPORTER+CRITIC | 9 |
| 实证/数据驱动(网络测量、数据集实验) | 重数据获取、统计检验 | 标准版 6 | ANALYST(+方法)+DATAENV+IMPL(+执行)+VERIFIER(+归因)+REPORTER(+质控) | 5 |
| ML/数值实验 | 训练、超参、出图 | 标准版 6 | ANALYST(+方法)+DATAENV+IMPL(+执行)+VERIFIER(+归因)+REPORTER(+质控) | 5 |
| 理论/形式化 | 证明、推导、无实验 | 精简版 3 | REPRO+VERIFIER | 2 |

> 标准版 = 1 ORCH + 5 子 Agent = 6 agents;精简版 = 1 ORCH + 2 子 Agent = 3 agents;
> 完整版 = 1 ORCH + 9 子 Agent = 10 agents。无论哪种档位,强制三件套(协调官+复现+验证)
> 与两条地基(验证/修复分离、假设台账)不可省。

## F. 标定样例(本工作区)

Cohen 等 2016《Jumpstarting BGP Security with Path-End Validation》(SIGCOMM),
仿真型域间路由安全论文,属"仿真/系统安全类 → 完整版 10 agents"(A0 协调官 + 9 命名子 Agent)。
- 复现单元示例:部署比例 vs 受保护 AS 占比、不同部署策略(top-k ISP / 随机)对比、
  next-AS 攻击成功率。
- 关键隐含假设(须入假设台账):BGP 选路策略(Gao-Rexford:客户>对等>供应商,再最短路,
  再 tie-break)、无谷路径导出、攻击者 announce 模型、部署选取策略、"受保护"指标口径、
  攻防对采样方式。
- 现有资产:`paper_text.txt`、`data/20160101.as-rel.txt.bz2`(CAIDA Jan-2016 与论文
  快照一致)、`pev/topology.py`(CAIDA 解析+合成拓扑)。

## G. Agent 派发协议(执行核心)

本节规定主 Agent(A0/ORCH)如何把每个命名角色**真实派发为子 Agent**,是本技能区别于
"只跑 2 个 agent"的关键。

### G.1 派发原语

每个角色 = 一次 Agent 工具调用:

```
工具: Agent
参数:
  subagent_type: "general-purpose"        # 具完整工具(Read/Write/Edit/Bash)
  description: "<代号>-<本次任务短描述>"     # 必须以代号开头,如 "ANALYST-解析Cohen2016"
  prompt: |
    <见 G.3 子 Agent 提示词模板,必须自包含>
```

- **命名**:`description` 必须以角色代号(ANALYST/ARCHITECT/DATAENV/IMPL/RUNNER/
  VERIFIER/DIAG/REPORTER/CRITIC/REPRO)开头,使运行时可辨识真实派发了哪些 agent。
- **自包含**:子 Agent 无本会话记忆,提示词必须写全:角色卡、RUN_WORKSPACE 绝对路径、
  论文路径(`paper_text.txt`)、要读的 Blackboard 文件、要写的 Blackboard 文件、依赖声明。
- **并行**:无依赖的角色在**同一条消息里发多个 Agent 调用**(如 DATAENV+IMPL)。
- **串行**:有依赖的角色,等上游 Blackboard 文件落盘后再派发。

### G.2 波次表(完整版 10 agents)

| 波次 | 派发的命名子 Agent | 依赖 | 写入的 Blackboard |
|------|------------------|------|------------------|
| W0 脚手架 | (A0 自执行) `create_run_workspace.py` + `env_check.py` | — | `RUN_WORKSPACE/` 目录 + `paper_text.txt` |
| W1 | A1 · ANALYST | — | `results/repro_spec.md`(+ 补全 `paper_text.txt`) |
| W2 | A2 · ARCHITECT | W1 | `results/method_design.md`, `results/assumption_ledger.md` |
| W3(并行) | A3 · DATAENV **与** A4 · IMPL | W2 | `datasets/`,`results/env_lock.md` **与** `sources/` |
| W4 | A5 · RUNNER(长任务,见 §G.6) | W3 | `logs/`(manifest/日志/原始结果) |
| W5 | A6 · VERIFIER | W4 | `results/verification_table.md` |
| W6(若失败) | A7 · DIAG → A0 按工单再派发出错角色 | W5 | `results/diagnoses/tickets.md` → 回溯到 W2/W3/W4 |
| W6.5 | A9 · CRITIC(收敛检查:覆盖完整性+收敛完整性) | W6 所有 must_fix 已修复/收敛理由已写 | `results/review_notes.md`(放行/打回) |
| W7 | A8 · REPORTER | W6.5 CRITIC 放行 | `results/figures/`, `results/report.md` |

> 子 Agent 总数 = 9(W1~W7 各命名角色),加 A0/ORCH = **10 agents**,与档位一致。
> 标准版(6)/精简版(3)按 §E 命名角色集对应裁剪,但**派发数量必须等于档位**,不得合并进协调官。

### G.3 子 Agent 提示词模板(自包含)

```
你是"论文复现流水线"中的【<代号 · 角色名>】(如 A1 · ANALYST 论文解析师)。
本次复现由协调官(主 Agent)调度,你只负责本角色工作,不要越权做其他角色的事。

# 你的职责(角色卡)
<从 §B 复制对应角色卡片要点>

# 工作目录(绝对路径,所有读写都在此之下)
RUN_WORKSPACE = <绝对路径,如 D:/.../20260713-path-end-validation>
  - 读论文正文: <RUN_WORKSPACE>/paper_text.txt
  - 你要读取的 Blackboard 文件: <列出,如 results/repro_spec.md>
  - 你要写出的 Blackboard 文件: <列出,如 results/method_design.md>
  - 代码放 sources/;数据放 datasets/;运行日志放 logs/;结果/图/报告放 results/;
    需用户定义的内容放 etc/。

# 依赖(必须先于你完成的角色产物,已存在于 RUN_WORKSPACE)
<如:W1 的 results/repro_spec.md 必须已存在>

# 任务
1. <具体步骤 1>
2. <具体步骤 2>
...
# 产出
严格把结果写入上述"你要写出的 Blackboard 文件"(遵守 §C 的目录桶),用清晰
Markdown/结构化格式。不要在本对话里只贴结论——结论必须落盘到 RUN_WORKSPACE 文件,
供协调官与其他子 Agent 读取。完成后用一句话汇报你写了哪些文件。
```

### G.4 协调官禁做清单(防止退回 2-agent 模式)

协调官(A0/ORCH)**不得**:
- 亲自通读论文并写出 `repro_spec.md`(派 A1/ANALYST);
- 亲自设计方法/写假设台账(派 A2/ARCHITECT);
- 亲自写复现代码(派 A4/IMPL);
- 亲自跑实验/收集结果(派 A5/RUNNER);
- 亲自画图表/写报告(派 A8/REPORTER);
- 亲自做逐项 pass/fail 判定(派 A6/VERIFIER)。

协调官**可以**:
- 执行 `create_run_workspace.py`、`env_check.py` 两个脚手架;
- 读回 Blackboard 文件做调度决策;
- 派发/并行/回溯命名子 Agent;
- 向用户汇报与交付。

### G.5 反馈闭环中的回溯派发

当 A6/VERIFIER 产物显示未通过:
1. 协调官派发 A7/DIAG 子 Agent,读 `results/verification_table.md` + 相关产物 →
   写 `results/diagnoses/tickets.md`(根因归类 + 责任角色代号)。
2. 协调官读工单,**再次派发**责任角色子 Agent(提示词附上工单上下文)做定向修复。
3. 修复后重派 A5/RUNNER(若代码/数据/配置变)→ 重派 A6/VERIFIER → 回到 G.5。
4. 循环直至收敛(全通过 / 判不可复现 / 需人工)。每次回溯在工单留痕。

### G.6 长任务、后台执行与唤醒契约(防"假完成"+ 幂等恢复)

本技能必须正确处理"长仿真(如 RUNNER 跑 18–22 分钟)"的中间等待,否则会出现
两种故障:(a) 协调官退化为"轮询 sleep"浪费资源;(b) 更危险的"假完成"——通知
早于产物触发,VERIFIER 在空目录上判定,闭环崩盘。

**1. 派发方式**:RUNNER 等长任务用 `run_in_background: true` 派发。
协调官在本轮正常 yield(回合结束),**不得 sleep、不得轮询**。

**2. 唤醒真相(必须写死,防止误解)**:协调官自身**不能自我唤醒**。
当后台子 Agent 完成时,**系统**会向对话注入一条 `<task-notification>`,
这等价于自动开启协调官的"下一轮"——协调官读回 Blackboard 产物,进入 W5。
快乐路径上是**系统唤醒**,不是 agent 自醒,因此**不是 man-in-the-loop**
(自治交接,用户无需任何操作)。

**3. 防假完成**:RUNNER 内部必须**前台阻塞**,直到 `logs/run_manifest.md`
与全部目标图落盘后才 return;**严禁**把仿真丢成后台 bash 就立即 return
(否则通知会早于产物触发 → 假完成 → VERIFIER 在空目录上判定)。

**4. 幂等恢复(降级兜底)**:若会话中断 / 通知丢失 / 运行时未自动恢复,流水线
会停。此时只需用户发一句"继续复现"(或重新触发技能),协调官**幂等恢复**:
- 任何重新进入(自动通知 or 手动重调 or 会话重载)都**先读 RUN_WORKSPACE Blackboard**;
- 按"哪些波次的产物已落盘"推进,**绝不允许假设"收到通知 = 已完成"**;
- 能从任意已完成波次无缝接续,不重跑已有产物。
降级路径仅一次人工兜底,一句指令即可接续,不破坏闭环。

**5. VERIFIER 闸门硬条件**:仅当 `logs/run_manifest.md` 与全部目标图已存在时,
协调官才派发 A6/VERIFIER;否则不推进,回到 W4 重派 RUNNER。

**6. 协调官 yield 时的恢复指引(必须向用户输出)**:协调官在派发 RUNNER 并 yield
前必须以明确文案告知用户,模板如下:

```
已派发 A5·RUNNER 在后台执行仿真(预计 ~<X> 分钟),完成后我会自动收到系统通知
并续跑 W5·VERIFIER,你无需做任何事。若 <X+5> 分钟后仍无动静,或会话被中断,
只需发一句"继续复现",我会读 Blackboard 从已完成的波次接着走。
```
