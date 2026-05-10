# Hermes Custom CLI Theme

Original visual skins for the [Hermes Agent](https://hermes-agent.nousresearch.com) CLI.

A small, opinionated skin pack. Each skin is a single YAML — palette, spinner, branding, ASCII banner art — themed end to end so the terminal feels like something specific, not "a colour scheme". Drop one in `~/.hermes/skins/`, point Hermes at it, restart, done.

## Install

**One-liner (any skin)**
```bash
curl -fsSL https://raw.githubusercontent.com/Sahil-SS9/hermes-Custom-CLI-Theme/main/scripts/install.sh | bash -s <skin>
```

**Manual**
```bash
mkdir -p ~/.hermes/skins
curl -fsSL https://raw.githubusercontent.com/Sahil-SS9/hermes-Custom-CLI-Theme/main/skins/kensei.yaml \
  -o ~/.hermes/skins/kensei.yaml
```

Then either set it as default in `~/.hermes/config.yaml`:
```yaml
display:
  skin: kensei
```

Or activate just for the current session by typing `/skin kensei` inside Hermes.

## Skins

| Skin | Theme | File |
| --- | --- | --- |
| **KENSEI** | Sword saint — deep ink, blood lacquer, old gold, parchment, drawn steel | [`skins/kensei.yaml`](skins/kensei.yaml) |
| **Shonen Surge** | Dark Naruto — nine-tails cloak, cursed chakra, magenta synthwave aura | [`skins/shonen-surge.yaml`](skins/shonen-surge.yaml) |
| **Free Palestine** | Sumud, watan, zaytoun. From the river to the sea, dignified solidarity | [`skins/free-palestine.yaml`](skins/free-palestine.yaml) |
| **Lord Commander** | Star Wars Imperial — superlaser primed, the rebellion ends here | [`skins/imperial.yaml`](skins/imperial.yaml) |
| **Legion** | Anonymous / V — matrix green, signal magenta, we do not forgive | [`skins/cyberpunk-anonymous.yaml`](skins/cyberpunk-anonymous.yaml) |
| **Tarnished** | Souls / Elden Ring — fell from grace, the Lands Between | [`skins/tarnished.yaml`](skins/tarnished.yaml) |
| **Voyager** | Lonely interstellar drifter — captain's-log calm, a pale blue dot fading | [`skins/voyager.yaml`](skins/voyager.yaml) |
| **Noir Signal** | Private investigator — case files, dossiers, the bulb's still on | [`skins/noir-signal.yaml`](skins/noir-signal.yaml) |
| **Shadow Monarch** | Solo Leveling — ARISE, the system has chosen, shadow soldiers | [`skins/solo-leveling-boss.yaml`](skins/solo-leveling-boss.yaml) |
| **Future Monkey** | Pink astronaut chimp — helmet glow, T-minus swagger, banana telemetry | [`skins/future-monkey.yaml`](skins/future-monkey.yaml) |
| **Snake** | Metal Gear Solid — tactical espionage, CODEC 140.85, war has changed | [`skins/metal-gear-solid.yaml`](skins/metal-gear-solid.yaml) |
| **CYBORG** | Terminator HUD — target acquired, threat assessed, termination protocol | [`skins/cyborg.yaml`](skins/cyborg.yaml) |

Screenshots are committed under `screenshots/` for the flagship skins. Run `python3 scripts/generate_screenshots.py` to render the full set as HTML.

## Creating your own

Copy `template.yaml` to `skins/<name>.yaml`, fill in your palette + branding, validate, screenshot, open a PR. Full guide in [`CONTRIBUTING.md`](CONTRIBUTING.md). Schema reference in [`SCHEMA.md`](SCHEMA.md).

## How it works

Hermes loads skin YAMLs from `~/.hermes/skins/`. Each skin overrides selected keys; missing keys inherit from the default skin. The schema supports:

- 28 standard colour keys
- 6 optional extended keys (`response_text`, `reasoning_border`, `reasoning_text`, `selection_bg`, plus skin-specific accents). Stock Hermes builds ignore unknown keys and fall back; newer/patched builds render them.
- Rich console markup in `banner_logo`, `banner_hero`, `welcome`, and `goodbye` — including per-character gradients (see SCHEMA.md).

See [`docs/compatibility.md`](docs/compatibility.md) for the extended-keys story and [`docs/design-notes.md`](docs/design-notes.md) for the quality bar.

## Validate

```bash
python3 scripts/validate_skins.py
```

CI runs the same check on every push and PR (`.github/workflows/validate.yml`).

## Licence

MIT. Validator workflow pattern and screenshot generator approach are adapted from [joeynyc/hermes-skins](https://github.com/joeynyc/hermes-skins) (MIT). The skins themselves, art pipeline, and content are this repo's own.
