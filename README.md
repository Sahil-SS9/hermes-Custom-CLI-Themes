# Hermes ACII Skins

Original visual skins for the Hermes Agent CLI.

This repo is Sahil's public skin pack: samurai terminals, anime energy, superhero/noir consoles, dignified political palettes, haunted CRTs, mecha dashboards, and other terminal identities.

Note: the repo name intentionally follows the remote name `hermes-ACII-Skins`. If you meant `ASCII`, rename it on GitHub before this goes public properly.

## Skins

| Skin | Theme | File |
| --- | --- | --- |
| KENSEI | Sword-saint terminal: black ink, blood lacquer, old gold, parchment, drawn steel | `skins/kensei.yaml` |
| Shonen Surge | Anime battle energy, speed lines, aura colours | `skins/shonen-surge.yaml` |
| Masked Vigilante | Original comic-noir superhero terminal | `skins/masked-vigilante.yaml` |
| Sumud | Palestine-inspired, dignified, olive branch and steadfastness | `skins/sumud.yaml` |
| Cyber Ronin | Neon ronin, rain, gridlines, magenta/cyan steel | `skins/cyber-ronin.yaml` |
| Ghost Terminal | Haunted CRT, spectral green, fog grey | `skins/ghost-terminal.yaml` |
| Kaiju Alert | Emergency broadcast, monster-scale warning system | `skins/kaiju-alert.yaml` |
| Mecha Hangar | Industrial cockpit, steel diagnostics, warning yellow | `skins/mecha-hangar.yaml` |
| Noir Signal | Detective terminal, amber lamp, smoke grey | `skins/noir-signal.yaml` |
| Solar Forge | Ember orange, molten gold, dark forge heat | `skins/solar-forge.yaml` |

Screenshots are planned under `screenshots/`.

## Install a skin

```bash
mkdir -p ~/.hermes/skins
curl -fsSL https://raw.githubusercontent.com/Sahil-SS9/hermes-ACII-Skins/main/skins/kensei.yaml   -o ~/.hermes/skins/kensei.yaml
hermes config set display.skin kensei
```

Restart Hermes after changing the default skin.

## Extended Hermes keys

Some skins use extended colour keys supported by Sahil's current Hermes build:

- `response_text`
- `reasoning_border`
- `reasoning_text`

Stock Hermes builds that do not support these keys should still load the skins, but those surfaces may fall back to standard colours.

## Validate

```bash
python3 scripts/validate_skins.py
```

Use strict screenshot validation when screenshots exist:

```bash
python3 scripts/validate_skins.py --require-screenshots
```
