# Skin schema

Every skin is a single YAML file under `skins/<name>.yaml`. The loader merges your skin over the default; any key you omit inherits from the default.

## Top-level

| Key | Type | Required | Notes |
|---|---|---|---|
| `name` | string | yes | Must equal the filename stem |
| `description` | string | yes | One-line summary, shown in the README gallery |
| `colors` | mapping | yes | 28 required keys + 6 optional extended (see below) |
| `spinner` | mapping | yes | 4 keys, each a non-empty list |
| `branding` | mapping | yes | 6 string keys |
| `tool_prefix` | string | yes | Single character shown before tool names |
| `tool_emojis` | mapping | optional | Tool-name → glyph; missing tools fall back to default |
| `banner_logo` | string | yes | Block-ASCII title with Rich markup |
| `banner_hero` | string | yes | Decorative art below the logo |

## Colours

All values must be full `#RRGGBB` hex strings. No shorthand, no named colours.

### Required (28 keys)

**Banner panel**
| Key | UI element |
|---|---|
| `banner_border` | Banner outer border |
| `banner_title` | Banner agent-name colour |
| `banner_accent` | Banner highlight / accent |
| `banner_dim` | Banner muted/secondary text |
| `banner_text` | Default banner body text |

**General UI**
| Key | UI element |
|---|---|
| `ui_accent` | Input chrome, highlights |
| `ui_label` | Field labels |
| `ui_ok` | Success / OK states |
| `ui_error` | Error states |
| `ui_warn` | Warning states |

**Prompt + response**
| Key | UI element |
|---|---|
| `prompt` | Input prompt text colour |
| `input_rule` | Rule line above the input |
| `response_border` | Agent response panel border |

**Session identity**
| Key | UI element |
|---|---|
| `session_label` | Session label |
| `session_border` | Session ID border |

**Status bar**
| Key | UI element |
|---|---|
| `status_bar_bg` | Status bar background |
| `status_bar_text` | Default status bar text |
| `status_bar_strong` | Strong values (e.g. model name) |
| `status_bar_dim` | Muted labels (e.g. "model:") |
| `status_bar_good` | OK indicator |
| `status_bar_warn` | Warning indicator |
| `status_bar_bad` | Bad indicator |
| `status_bar_critical` | Critical indicator |
| `voice_status_bg` | Voice-mode badge background |

**Completion menu + selection**
| Key | UI element |
|---|---|
| `completion_menu_bg` | Menu background |
| `completion_menu_current_bg` | Current row background |
| `completion_menu_meta_bg` | Meta column background |
| `completion_menu_meta_current_bg` | Current meta column background |

### Extended (6 keys, optional)

Validated only when present. Supported by newer/patched Hermes builds; stock Hermes ignores them and the surfaces fall back to standard colours.

| Key | UI element |
|---|---|
| `response_text` | Body text of the agent response panel |
| `reasoning_border` | Border of the reasoning panel |
| `reasoning_text` | Body text of the reasoning panel |
| `selection_bg` | Mouse-selection / current-row highlight |
| `blade_glow` | KENSEI-specific accent (banner art) |
| `blade_edge` | KENSEI-specific accent (banner art) |

## Spinner

```yaml
spinner:
  waiting_faces:  # cycled while awaiting an API response
    - "(⚙)"
  thinking_faces: # cycled during model reasoning
    - "(◆)"
  thinking_verbs: # phrases shown alongside the face
    - "processing"
  wings:          # bracket pairs around the face: [left, right]
    - ["⟪⚡", "⚡⟫"]
```

All four keys are required and each list must be non-empty. Flagship skins use 4–5 faces, 8–12 verbs, and 3–4 wing pairs.

## Branding

```yaml
branding:
  agent_name:     "Agent"
  welcome:        "Welcome."           # Rich markup supported (gradient pattern below)
  goodbye:        "Session closed."    # Rich markup supported
  response_label: " ⚡ Agent "          # Padded with spaces for visual breathing room
  prompt_symbol:  "⚡ "                 # 1-3 chars
  help_header:    "(⚡) Commands"
```

All six keys required.

## tool_emojis

Optional dict. Maps a tool name to a single themed glyph.

Canonical tool names: `terminal`, `web_search`, `read_file`, `write_file`, `search_files`, `execute_code`, `browser_navigate`, `delegate_task`, `mixture_of_agents`, `memory`, `clarify`, `cronjob`, `process`, `todo`.

Missing tools fall back to the default skin's emoji. Flagship skins define 8+ entries with theme-coherent glyphs (e.g. KENSEI uses kanji: `read_file: 巻`, `memory: 心`, `mixture_of_agents: 衆`).

## Rich markup

`banner_logo`, `banner_hero`, `welcome`, and `goodbye` accept Rich console markup:

- Plain colour: `[#FFD700]text[/]`
- Bold: `[bold]text[/]` or `[bold #FFD700]text[/]`
- Background: `[#FFFFFF on #007A3D]text[/]`
- Per-character gradient: wrap every character in its own colour tag. Use a small helper:

```python
def hex2rgb(h): h=h.lstrip('#'); return int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
def rgb2hex(r,g,b): return f"#{int(r):02X}{int(g):02X}{int(b):02X}"
def gradient(stops, n):
    if n<=1: return [stops[0]]
    seg=len(stops)-1; out=[]
    for i in range(n):
        t=i/(n-1)*seg; idx=min(int(t),seg-1); u=t-idx
        s=hex2rgb(stops[idx]); e=hex2rgb(stops[idx+1])
        out.append(rgb2hex(s[0]+(e[0]-s[0])*u, s[1]+(e[1]-s[1])*u, s[2]+(e[2]-s[2])*u))
    return out
def apply(text, stops):
    cs = gradient(stops, len(text))
    return ''.join(f"[{c}]{ch}[/]" for c,ch in zip(cs, text))
```

Example: KENSEI's welcome uses stops `#D4A017 → #E34234 → #C0392B → #8B0000` across 34 characters.

## Validation

```
python3 scripts/validate_skins.py                       # schema check
python3 scripts/validate_skins.py --require-screenshots # also check screenshots/<name>.png exists
```

CI runs the schema check on every push and PR (`.github/workflows/validate.yml`).
