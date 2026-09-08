#!/usr/bin/env python3
"""
create_run_workspace.py — 为一次论文复现创建隔离的工作目录 (Run Workspace)

目录命名规则: {YYYYMMDD}-{slug}
  YYYYMMDD : 执行当天的日期(本地时区)
  slug     : 论文核心机制短标识(英文小写、连字符分隔, 2~5 词),
             由调用方(编排协调官)从论文标题/方法推导, 例如:
             Cohen 2016 PEV      -> path-end-validation  (或缩写 PEV)
             RPKI ROV 测量论文    -> route-origin-validation
             BGPsec 部分部署研究  -> bgpsec-partial-deploy

用法:
    python create_run_workspace.py --slug path-end-validation
    python create_run_workspace.py --slug PEV --root "D:/proj/paper-repro"
    python create_run_workspace.py --slug bgpsec-partial-deploy --date 20260713
    python create_run_workspace.py --slug pev --paper-text "D:/proj/paper-repro/paper_text.txt"

行为:
  - 在 --root (默认当前目录) 下创建 {YYYYMMDD}-{slug}/
  - 若同名目录已存在且非空(含任何文件), 自动追加 -2 / -3 ... 避免覆盖历史复现
  - 预建标准目录桶(见 SUBDIRS):
        sources/            放复现代码
        datasets/           放数据集合
        logs/               放代码日志 + 原始运行结果(manifest/stdout/raw)
        results/            放结果与分析产物(规格/方法/假设台账/验证表/评审/归因/报告/图)
          results/figures/  图表
          results/diagnoses/ 归因工单
        etc/                放需要用户定义的内容(参数覆盖、手工确认的假设、配置)
  - 在工作目录根下放置 paper_text.txt(论文可读文本):
        若提供 --paper-text 且为文本文件 -> 复制其内容;
        否则创建一个占位 paper_text.txt(内含提示, 待解析师/用户填入正文)。
  - 仅打印最终绝对路径到 stdout (供 CodeBuddy 捕获并设为 RUN_WORKSPACE)
  - 退出码 0 = 成功创建/复用, 1 = 失败(如 root 不可写、slug 非法)

本脚本只建目录 + 放 paper_text.txt, 不联网、不改写工作区其他任何文件。
"""
import os
import re
import sys
import shutil
import argparse
from datetime import date


# 预建的标准目录桶：所有本次复现的生成物按类别归位
SUBDIRS = [
    "sources",            # 代码
    "datasets",           # 数据集合
    "logs",               # 代码日志 + 原始运行结果
    "results",            # 结果与分析产物
    "results/figures",    # 图表
    "results/diagnoses",  # 归因工单
    "etc",                # 用户自定义内容
]

# 工作目录根下的论文文本文件名
PAPER_TEXT_NAME = "paper_text.txt"

PAPER_TEXT_PLACEHOLDER = (
    "# paper_text.txt — 论文可读文本\n"
    "#\n"
    "# 本文件用于存放本次复现所依据的论文正文(纯文本)。\n"
    "# 由“论文解析师(Paper Analyst)”从 PDF/链接抽取, 或由用户直接粘贴。\n"
    "# 所有下游子 Agent 读取本文件获取论文内容, 不再各自去解析 PDF。\n"
    "#\n"
    "# (占位内容 — 请用论文正文替换本段)\n"
)


def slugify(raw: str) -> str:
    """把任意字符串规范成文件系统安全的短 slug：小写、连字符、去首尾横线。"""
    s = raw.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)        # 非字母数字 -> 单连字符
    s = re.sub(r"-{2,}", "-", s)             # 合并连续横线
    s = s.strip("-")
    if not s:
        raise ValueError("slug 经清洗后为空, 请检查论文核心机制标识")
    return s[:48]                            # 限长, 避免路径过长


def resolve_name(root: str, base: str) -> str:
    """返回可用的目录名：若 base 已存在且非空, 追加 -2/-3... 直到空闲。"""
    candidate = os.path.join(root, base)
    if not os.path.exists(candidate):
        return candidate
    # 已存在：仅当为空目录时复用, 否则递增后缀
    if not any(os.scandir(candidate)):
        return candidate
    i = 2
    while True:
        alt = os.path.join(root, f"{base}-{i}")
        if not os.path.exists(alt):
            return alt
        i += 1


def place_paper_text(workspace: str, paper_text_src: str | None) -> None:
    """在 workspace 根下生成 paper_text.txt：有源则复制, 无源则写占位。"""
    dst = os.path.join(workspace, PAPER_TEXT_NAME)
    if os.path.exists(dst):
        return  # 复用已有目录时不覆盖
    if paper_text_src:
        src = os.path.abspath(paper_text_src)
        if os.path.isfile(src):
            shutil.copyfile(src, dst)
            return
        # 源不存在则退化为占位, 并在 stderr 提示(不影响退出码)
        print(f"⚠ 指定的 --paper-text 不存在, 已写占位: {src}", file=sys.stderr)
    with open(dst, "w", encoding="utf-8") as f:
        f.write(PAPER_TEXT_PLACEHOLDER)


def main():
    ap = argparse.ArgumentParser(description="创建论文复现工作目录 (Run Workspace)")
    ap.add_argument("--slug", required=True, help="论文核心机制短标识, 如 path-end-validation / PEV")
    ap.add_argument("--root", default=os.getcwd(), help="项目根目录 (默认当前目录)")
    ap.add_argument("--date", default=None, help="覆盖日期 YYYYMMDD (默认今天)")
    ap.add_argument("--paper-text", default=None,
                    help="论文纯文本源文件路径; 提供则复制为 <workspace>/paper_text.txt")
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        print(f"❌ root 不是有效目录: {root}", file=sys.stderr)
        sys.exit(1)

    try:
        slug = slugify(args.slug)
    except ValueError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)

    if args.date:
        if not re.fullmatch(r"\d{8}", args.date):
            print("❌ --date 必须是 YYYYMMDD 八位日期", file=sys.stderr)
            sys.exit(1)
        ymd = args.date
    else:
        ymd = date.today().strftime("%Y%m%d")

    base = f"{ymd}-{slug}"
    path = resolve_name(root, base)

    try:
        os.makedirs(path, exist_ok=True)
        for sub in SUBDIRS:
            os.makedirs(os.path.join(path, sub), exist_ok=True)
        place_paper_text(path, args.paper_text)
    except OSError as e:
        print(f"❌ 创建目录失败: {e}", file=sys.stderr)
        sys.exit(1)

    print(path)  # 唯一 stdout 输出: 供 CodeBuddy 捕获为 RUN_WORKSPACE
    sys.exit(0)


if __name__ == "__main__":
    main()
