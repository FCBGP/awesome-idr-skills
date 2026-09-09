#!/bin/bash
# link_skills.sh
# Symlinks all directories under ./skills into a destination directory.
# Default destination: ~/.agents/skills (created by Claude Code).
#
# Usage:
#   ./link_skills.sh                # link into ~/.agents/skills (default)
#   ./link_skills.sh -h             # show help
#   ./link_skills.sh --help         # show help
#   ./link_skills.sh -d DIR         # link into DIR instead of ~/.agents/skills
#   ./link_skills.sh --dest DIR     # link into DIR instead of ~/.agents/skills

set -euo pipefail

# Source: the skills directory in the current repo
SKILLS_SRC="$PWD/skills"

# Destination: where Claude Code loads skills from (default)
DEST="${HOME}/.agents/skills"

# --- argument parsing ---------------------------------------------------------
show_help() {
  cat <<EOF
link_skills.sh — symlink every skill directory under ./skills into a destination.

USAGE
  ./link_skills.sh [OPTIONS]

OPTIONS
  -h, --help       Show this help message and exit.
  -d DIR, --dest DIR
                   Set the destination directory. Default is ~/.agents/skills.

EXAMPLES
  ./link_skills.sh              # link into ~/.agents/skills (default)
  ./link_skills.sh -d /tmp/sk   # link into /tmp/sk
  ./link_skills.sh --dest /tmp/sk

NOTES
  - The destination directory is created if it does not exist.
  - Existing non-symlink entries at the destination are replaced.
  - Re-run after pulling new skills to refresh the links.
EOF
}

DEST_ARG=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      show_help
      exit 0
      ;;
    -d|--dest)
      if [[ $# -lt 2 ]]; then
        echo "Error: $1 requires a directory argument" >&2
        show_help >&2
        exit 1
      fi
      DEST_ARG="$2"
      shift 2
      ;;
    -*)
      echo "Error: unknown option: $1" >&2
      show_help >&2
      exit 1
      ;;
    *)
      echo "Error: unexpected argument: $1" >&2
      show_help >&2
      exit 1
      ;;
  esac
done

if [[ -n "$DEST_ARG" ]]; then
  DEST="$DEST_ARG"
fi

# --- main ---------------------------------------------------------------------
if [[ ! -d "$SKILLS_SRC" ]]; then
  echo "Error: no skills/ directory found in $PWD" >&2
  exit 1
fi

mkdir -p "$DEST"

count=0
for dir in "$SKILLS_SRC"/*/; do
  # Only act on real directories (not the trailing-*/ match for a lone file)
  [[ -d "$dir" ]] || continue

  name="$(basename "$dir")"
  target="$DEST/$name"

  # Remove any existing non-symlink entry so we don't shadow the new link
  if [[ -e "$target" || -L "$target" ]]; then
    rm -rf "$target"
  fi

  ln -s "$dir" "$target"
  echo "linked: $name -> $target"
  count=$((count + 1))
done

echo
echo "Done: $count skills symlinked into $DEST"