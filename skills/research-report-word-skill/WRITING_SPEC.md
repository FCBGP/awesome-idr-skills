# Writing Spec

## Report Tone

- Write as a research survey report (`调研报告`), not an implementation plan.
- Prefer factual review: current status, representative systems, limitations, gaps, and relevance.
- Avoid overusing `本课题`; prefer `项目`, `该关键技术方向`, `平台`, or `后续平台`.
- Keep content tied to existing research, standards, datasets, platforms, and tools.

## Heading Levels

Use exactly four Markdown heading levels:

```markdown
项目调研报告

# 二、调研范围与方法

## 2.1 调研范围

## 2.2 调研方法

# 三、关键技术调研情况

## 3.2 关键技术2 分布式多源共识一致性验证技术

### 3.2.1 RPKI及路由起源验证技术现状

#### 3.2.1.1 RPKI/ROA/ROV基本机制
```

Rules:

- Chinese-number chapters (`一、二、三`) use `#`.
- `X.Y` sections use `##`.
- `X.Y.Z` sections use `###`.
- `X.Y.Z.W` sections use `####`.
- Do not create headings below `####`; use `（1）` or `1）` instead.

## Section-Level Substructure

Under `####`, use bold Chinese numbered subheadings:

```markdown
**（1）研究现状**

正文……

**（2）主要局限**

正文……
```

For long parallel points, use Chinese-style `1）`:

```markdown
1）多源数据接入与模板化治理。正文……

2）分组共识与可信视图生成。正文……
```

Do not use Markdown ordered lists like `1.` for this report style.

## Figures

Use four-level numbering:

```markdown
正文如图 3-2-2-1 所示。

![](media/fig-name.png)

图 3-2-2-1 基于领导节点的常态共识投票模式
```

Rules:

- Use empty alt text: `![](media/xxx.png)`.
- Figure caption is below the image.
- Caption format is `图 3-2-X-Y 标题`.
- Do not write captions inside image alt text.

## Tables

Use four-level numbering:

```markdown
对比如表 3-2-2-1 所示。

表 3-2-2-1 不同网络模型下经典BFT共识对比

| 协议类型 | 优势 | 局限 |
| --- | --- | --- |
| PBFT | 成熟 | 通信复杂 |
```

Rules:

- Table caption is above the table.
- Do not bold table captions.
- Write normal Markdown tables; Word three-line formatting is handled by postprocess.

## Inline Code and APIs

Use backticks for paths, fields, API endpoints, and parameters in Markdown:

```markdown
RouteViews 可通过 `https://archive.routeviews.org/bgpdata/` 获取数据。
```

The Word postprocess step restores inline code to body font.

## Images and Media

- Put images in `media/` next to the Markdown file.
- Reference images by relative path: `![](media/example.png)`.
- Check final Word manually for image/table page breaks.
