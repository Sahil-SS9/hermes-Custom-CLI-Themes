#!/usr/bin/env bash
# Install a skin from this repo into your local Hermes Agent config.
# Usage: ./install.sh <skin-name>   (default: kensei)

set -euo pipefail
skin="${1:-kensei}"
repo="https://raw.githubusercontent.com/Sahil-SS9/hermes-Custom-CLI-Theme/main"
skins_dir="$HOME/.hermes/skins"
config="$HOME/.hermes/config.yaml"

mkdir -p "$skins_dir"
curl -fsSL "$repo/skins/$skin.yaml" -o "$skins_dir/$skin.yaml"
echo "Installed $skin to $skins_dir/$skin.yaml"

cat <<EOF

To activate this skin, set it as default in $config:

  display:
    skin: $skin

Or activate for the current session only by typing this inside Hermes:

  /skin $skin

EOF
