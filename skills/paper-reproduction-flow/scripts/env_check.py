#!/usr/bin/env python3
"""
env_check.py — 论文复现环境自检 (paper-reproduction-flow skill)

用法:
    python env_check.py [workspace]

检查内容(全部本机、无需联网):
  1. 运行时: python3 / node 是否可用
  2. 数据集: 工作区内是否存在论文规格书标注所需的数据文件(占位探测)
  3. 常用依赖: PDF 解析(pypdf)、压缩(bz2 内置)、绘图(matplotlib)、网络拓扑(networkx)
  4. 算力风险: 若疑似大规模仿真,给抽样建议

退出码: 0 = 满足(或仅有可忽略警告), 1 = 不满足(需用户补齐后再跑)

本脚本只探测并报告,绝不自行联网下载或改写任何文件。
"""
import os
import sys
import shutil
import subprocess
import textwrap

REQUIRED_PY = (3, 8)
OPTIONAL_DEPS = {
    "pypdf": "PDF 文本抽取 (pip install pypdf)",
    "matplotlib": "复现图表绘制 (pip install matplotlib)",
    "networkx": "AS 拓扑图计算 (pip install networkx)",
    "numpy": "数值计算 (pip install numpy)",
}

# 论文规格书里常见会引用、需用户自备的数据线索(文件名子串)
DATA_HINTS = [".as-rel", "as-rel.txt", ".bz2", "caida", "topology", "dataset"]


def have_runtime():
    problems = []
    py = shutil.which("python3") or shutil.which("python")
    ok_py = False
    if py:
        try:
            out = subprocess.run([py, "-c", "import sys;print(sys.version_info[:2])"],
                                 capture_output=True, text=True, timeout=10)
            major, minor = eval(out.stdout.strip())
            ok_py = (major, minor) >= REQUIRED_PY
        except Exception:
            ok_py = False
    if not ok_py:
        problems.append(f"需要 Python >= {REQUIRED_PY[0]}.{REQUIRED_PY[1]} (未找到或版本过低)")
    if not shutil.which("node"):
        problems.append("可选: 未检测到 node.js (数值/前端可视化时可能需要)")
    return problems


def have_data(workspace):
    # 仅做存在性探测: 工作区内是否存在任何疑似数据集的文件
    found = []
    for root, _, files in os.walk(workspace):
        for f in files:
            low = f.lower()
            if any(h in low for h in DATA_HINTS):
                found.append(os.path.relpath(os.path.join(root, f), workspace))
        if len(found) >= 8:
            break
    return found


def have_deps():
    missing = []
    for mod, why in OPTIONAL_DEPS.items():
        try:
            __import__(mod)
        except Exception:
            missing.append((mod, why))
    return missing


def main():
    workspace = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    workspace = os.path.abspath(workspace)
    print(f"== 论文复现环境自检 ==")
    print(f"工作区: {workspace}\n")

    blockers = []          # 必须解决
    warnings = []          # 建议补齐

    rt = have_runtime()
    blockers.extend(rt)

    data_files = have_data(workspace)
    if not data_files:
        warnings.append("未在工作区发现数据集文件(.as-rel/.bz2/caida/topology 等)。"
                        "若论文需要数据,请先下载/放置到工作区。")
    else:
        print(f"[数据] 发现 {len(data_files)} 个疑似数据集文件, 例如:")
        for f in data_files[:5]:
            print(f"      - {f}")

    missing = have_deps()
    for mod, why in missing:
        warnings.append(f"缺少依赖 {mod}: {why}")

    print()
    print("[运行时] " + ("OK" if not rt else "缺失: " + "; ".join(rt)))
    if missing:
        print("[依赖] 缺失: " + "; ".join(m for m, _ in missing))
    else:
        print("[依赖] OK (所需绘图/拓扑库均已安装)")

    print()
    # 算力风险: 若发现大拓扑数据,提示抽样
    big = [f for f in data_files if f.endswith(".bz2") or "as-rel" in f.lower()]
    if big:
        warnings.append("检测到疑似大规模拓扑数据, 全网仿真可能很慢/吃内存。"
                        "建议: 先用合成小拓扑(如 pev/topology.py generate_synthetic)跑通, "
                        "再在小种子抽样下跑真实拓扑, 取均值。")

    ok = not blockers
    if blockers:
        print("❌ 环境不满足, 请先补齐以下必需项:")
        for b in blockers:
            print(f"   - {b}")
    else:
        print("✅ 必需项已满足, 可进入复现流程。")

    if warnings:
        print("\n⚠️ 建议补齐(非阻塞, 但可能影响复现范围/质量):")
        for w in warnings:
            print("   - " + textwrap.shorten(w, 120))

    print("\n结论: " + ("可继续" if ok else "请补齐后重跑 env_check.py"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
