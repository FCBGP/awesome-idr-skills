#!/usr/bin/env bash
# Chinese research report: Markdown -> Word.
# This portable skill version intentionally does not call crop_media_images.py.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REFERENCE_DOC="${SCRIPT_DIR}/调研报告-reference.docx"

if ! command -v pandoc >/dev/null 2>&1; then
  echo "错误: 未找到 pandoc，请先安装 pandoc。" >&2
  echo "macOS 示例: brew install pandoc" >&2
  exit 1
fi

if [[ $# -lt 1 ]]; then
  echo "用法: $0 <输入.md> [输出.docx]" >&2
  echo "示例: $0 /path/to/调研报告.md" >&2
  exit 1
fi

INPUT_MD="$1"
if [[ "${INPUT_MD}" != /* ]]; then
  INPUT_MD="$(pwd)/${INPUT_MD}"
fi

if [[ ! -f "${INPUT_MD}" ]]; then
  echo "错误: 找不到输入文件 ${INPUT_MD}" >&2
  exit 1
fi

INPUT_DIR="$(cd "$(dirname "${INPUT_MD}")" && pwd)"
MEDIA_DIR="${INPUT_DIR}/media"
OUTPUT_DIR="${INPUT_DIR}/output"
BASE_NAME="$(basename "${INPUT_MD}" .md)"

if [[ $# -ge 2 ]]; then
  OUTPUT_DOCX="$2"
  if [[ "${OUTPUT_DOCX}" != /* ]]; then
    OUTPUT_DOCX="$(pwd)/${OUTPUT_DOCX}"
  fi
else
  mkdir -p "${OUTPUT_DIR}"
  OUTPUT_DOCX="${OUTPUT_DIR}/${BASE_NAME}-导出.docx"
fi

if [[ "${OUTPUT_DOCX}" == "${INPUT_MD%.md}.docx" ]]; then
  echo "错误: 输出路径不能与输入 md 同名，避免覆盖源文件旁的人工版本。" >&2
  exit 1
fi

mkdir -p "$(dirname "${OUTPUT_DOCX}")"

python3 "${SCRIPT_DIR}/prepare_reference_docx.py"

if [[ ! -f "${REFERENCE_DOC}" ]]; then
  echo "错误: 样式母版生成失败 ${REFERENCE_DOC}" >&2
  exit 1
fi

RESOURCE_PATH="${INPUT_DIR}:${SCRIPT_DIR}"
if [[ -d "${MEDIA_DIR}" ]]; then
  RESOURCE_PATH="${RESOURCE_PATH}:${MEDIA_DIR}"
fi

pandoc "${INPUT_MD}" \
  -o "${OUTPUT_DOCX}" \
  --reference-doc="${REFERENCE_DOC}" \
  --resource-path="${RESOURCE_PATH}"

python3 "${SCRIPT_DIR}/postprocess_docx.py" "${OUTPUT_DOCX}"

echo "已生成: ${OUTPUT_DOCX}"
echo "打开 Word 后 Ctrl+A → F9 更新引用；检查图表是否跨页。"
