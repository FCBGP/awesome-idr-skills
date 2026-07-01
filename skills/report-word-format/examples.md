# Examples

## Create a Report Section

User request:

```text
补充 3.2.4 实验环境与工具链调研，介绍 RouteViews、RIPE RIS、BGPStream、FRRouting、Routinator 的接入方式。
```

Agent steps:

1. Read `WRITING_SPEC.md`.
2. Draft section using `###` / `####` levels.
3. Use `1）` for long parallel items.
4. Add citations in first-appearance order.
5. Update bibliography using `REFERENCE_RULES.md`.
6. Run `scripts/check_references.py`.
7. Run `scripts/build_docx.sh`.

## Insert a Figure

Markdown:

```markdown
RPKI架构如图 3-2-1-1 所示。

![](media/rpki-architecture.png)

图 3-2-1-1 RPKI体系架构图
```

Do not write:

```markdown
![图 3-2-1-1 RPKI体系架构图](media/rpki-architecture.png)
```

## Insert a Table

Markdown:

```markdown
总体变化趋势如表 3-2-1-1 所示。

表 3-2-1-1 全球RPKI部署发展趋势

| 指标 | 2019年 | 2022年 | 2025年 |
| --- | --- | --- | --- |
| IPv4 ROA覆盖率 | <20% | 约35%~40% | >50% |
| IPv6 ROA覆盖率 | 约20% | 约45%~50% | >60% |
```

The Word three-line table is produced by `postprocess_docx.py`.

## Bibliography

Markdown:

```markdown
PBFT是经典拜占庭容错协议[1]，HotStuff进一步降低了视图变更复杂度[2]。

参考文献

[1] Castro M, Liskov B. Practical byzantine fault tolerance[C]//Proc. of OSDI. USENIX, 1999: 173-186.

[2] Yin M, Malkhi D, Reiter M K, et al. HotStuff: BFT consensus with linearity and responsiveness[C]//Proc. of PODC. ACM, 2019: 347-356.
```

## Build

```bash
python3 scripts/check_references.py /path/to/report.md
scripts/build_docx.sh /path/to/report.md
```

Output:

```text
/path/to/output/report.docx
```
