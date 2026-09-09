#!/bin/bash
# link_skills.sh
# Symlinks all directories under ./skills into ~/.agents/skills
# Usage:  ./link_skills.sh
#         ~/.agents/skills must already exist (created by Claude Code)

set -euo pipefail

# Source: the skills directory in the current repo
SKILLS_SRC="$PWD/skills"

# Destination: where Claude Code loads skills from
DEST="${HOME}/.agents/skills"

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