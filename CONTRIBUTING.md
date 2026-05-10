# Contributing a skin

Drop a YAML in `skins/`, validate, screenshot, open a PR. Detail below.

## Quick start

1. **Copy the template**
   ```
   cp template.yaml skins/my-skin.yaml
   ```

2. **Set the name** in the YAML to match the filename stem:
   ```yaml
   name: my-skin
   ```

3. **Pick a palette.** Every colour value must be a full `#RRGGBB` hex string (no shorthand, no named colours). See `SCHEMA.md` for what each colour key affects.

4. **Theme the branding.** `welcome`, `goodbye`, `response_label`, `prompt_symbol`, `help_header`, the spinner faces/verbs/wings — all should reinforce one coherent theme. KENSEI is the reference for flagship-tier: every choice ties to "sword saint".

5. **Banner art.** Two options:
   - **Image-derived** — generate or source a high-contrast monochrome image, run `scripts/img2braille.py` (in `/tmp/hermes-skins/` during development) to convert to braille, wrap in Rich markup colour tags.
   - **Hand-composed** — box-drawing chars + Rich markup, KENSEI-style (block-ASCII title + themed subtitle).

6. **Validate**
   ```
   python3 scripts/validate_skins.py
   ```
   Must print `OK, N skin(s) valid`. The CI workflow runs the same check on every PR.

7. **Generate a screenshot**
   ```
   python3 scripts/generate_screenshots.py
   ```
   Then convert `screenshots/html/<my-skin>.html` to PNG via your tool of choice and commit at `screenshots/<my-skin>.png`. (PNG screenshots in CI are planned for v0.2.)

8. **Add a row** to the gallery table in `README.md`.

## House rules

- **No copyrighted character names or trademarked logos.** Archetypes only. "the Lord Commander" not "Vader". "the Tarnished" not "Sung Jin-Woo".
- **British English** in docs (colour, organise, behaviour).
- **No em-dashes** in user-facing strings — use commas, semicolons, or full stops.
- **One clear visual idea per skin.** No random colour vomit.
- **Themed thinking verbs.** Not "processing" / "analysing" / "computing". Make them sound like operations from your source material.
- **Sensitive subjects** (politics, religion, war) — handle with restraint and dignity. The `free-palestine` skin is the reference for how to do this without being gimmicky.

## What the validator checks

- 28 required colour keys, all `^#[0-9A-Fa-f]{6}$`
- 6 optional extended colour keys (`response_text`, `reasoning_border`, `reasoning_text`, `selection_bg`, `blade_glow`, `blade_edge`) validated if present
- 4 spinner keys (`waiting_faces`, `thinking_faces`, `thinking_verbs`, `wings`) non-empty
- 6 branding keys (`agent_name`, `welcome`, `goodbye`, `response_label`, `prompt_symbol`, `help_header`)
- `banner_logo`, `banner_hero`, `tool_prefix` present
- `name` matches filename

`--require-screenshots` additionally checks for `screenshots/<name>.png`. CI will enforce this once we ship v0.2.

## Editor config

The repo ships an `.editorconfig` (YAML = 2 spaces, LF line endings, trim trailing whitespace, final newline). Any editor that respects EditorConfig will pick this up automatically. Otherwise: 2-space YAML indentation, LF, trim trailing whitespace.
