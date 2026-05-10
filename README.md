# Hermes Custom CLI Theme

Original visual skins for the [Hermes Agent](https://hermes-agent.nousresearch.com) CLI.

A small, opinionated skin pack. Each skin is a single YAML — palette, spinner, branding, ASCII banner art — themed end to end so the terminal feels like something specific, not "a colour scheme". Drop one in `~/.hermes/skins/`, point Hermes at it, restart, done.

## Install

**One-liner (any skin)**
```bash
curl -fsSL https://raw.githubusercontent.com/Sahil-SS9/hermes-Custom-CLI-Themes/main/scripts/install.sh | bash -s <skin>
```

**Manual**
```bash
mkdir -p ~/.hermes/skins
curl -fsSL https://raw.githubusercontent.com/Sahil-SS9/hermes-Custom-CLI-Themes/main/skins/kensei.yaml \
  -o ~/.hermes/skins/kensei.yaml
```

Then either set it as default in `~/.hermes/config.yaml`:
```yaml
display:
  skin: kensei
```

Or activate just for the current session by typing `/skin kensei` inside Hermes.

## Skins

### KENSEI
> KENSEI -- sword saint. Deep ink, blood lacquer, and drawn steel.

![kensei](screenshots/kensei.png)

`skins/kensei.yaml`

### Tarnished
> Fell from grace. Pale gold, ember red, ash grey, and the long dark of the Lands Between.

![tarnished](screenshots/tarnished.png)

`skins/tarnished.yaml`

### Lord Commander
> The ultimate weapon stands ready. Superlaser primed, the galaxy bows, the rebellion ends here.

![imperial](screenshots/imperial.png)

`skins/imperial.yaml`

### Snake
> Tactical espionage CODEC -- Snake, do you copy?

![metal-gear-solid](screenshots/metal-gear-solid.png)

`skins/metal-gear-solid.yaml`

### Shonen Surge
> Shonen Surge -- nine-tails cloak. Cursed chakra. Aura unleashed.

![shonen-surge](screenshots/shonen-surge.png)

`skins/shonen-surge.yaml`

### Shadow Monarch
> Shadow Monarch terminal -- ARISE. The system has chosen.

![solo-leveling-boss](screenshots/solo-leveling-boss.png)

`skins/solo-leveling-boss.yaml`

### Legion
> Mask on. Legion at the wire. Matrix green, signal magenta, surveillance void -- we do not forgive, we do not forget.

![cyberpunk-anonymous](screenshots/cyberpunk-anonymous.png)

`skins/cyberpunk-anonymous.yaml`

### CYBORG
> Cyborg HUD -- target acquired, threat assessed, termination protocol engaged.

![cyborg](screenshots/cyborg.png)

`skins/cyborg.yaml`

### Future Monkey
> Pink astronaut chimp -- helmet glow, T-minus swagger, banana telemetry.

![future-monkey](screenshots/future-monkey.png)

`skins/future-monkey.yaml`

### Voyager
> Lonely interstellar drifter -- captain's-log calm, telemetry whispers, a pale blue dot fading behind.

![voyager](screenshots/voyager.png)

`skins/voyager.yaml`

### Noir Signal
> Private investigator's terminal. Case files, dossiers, the bulb's still on.

![noir-signal](screenshots/noir-signal.png)

`skins/noir-signal.yaml`

### Free Palestine
> Free Palestine -- sumud, watan, zaytoun. To remain is a victory.

![free-palestine](screenshots/free-palestine.png)

`skins/free-palestine.yaml`

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
