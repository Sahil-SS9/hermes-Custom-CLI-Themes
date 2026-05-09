# Skin schema

Skin files live under `skins/*.yaml`.

Required top-level keys:
- `name`
- `description`
- `colors`
- `spinner`
- `branding`
- `tool_prefix`
- `banner_logo`
- `banner_hero`

Standard colour keys follow Hermes Agent's skin schema. This repo also permits extended keys:
- `response_text`
- `reasoning_border`
- `reasoning_text`
- `selection_bg`

All colour values must be full `#RRGGBB` hex strings.
