#!/usr/bin/env bash
set -euo pipefail
skin="${1:-kensei}"
repo="https://raw.githubusercontent.com/Sahil-SS9/hermes-ACII-Skins/main"
mkdir -p "$HOME/.hermes/skins"
curl -fsSL "$repo/skins/$skin.yaml" -o "$HOME/.hermes/skins/$skin.yaml"
hermes config set display.skin "$skin"
echo "Installed $skin. Restart Hermes to load it from config."
