#!/usr/bin/env python3
"""Render Hermes Agent skin previews to HTML.

For each YAML in skins/, renders banner_logo, banner_hero, a sample response
panel, reasoning panel, spinner line, prompt rule, and status bar with real
Rich truecolor markup, then exports inline-styled HTML to screenshots/html/.

If skins/kensei.flagship-candidate.yaml exists, also writes a side-by-side
comparison to screenshots/preview/kensei-compare.html plus standalone
kensei-before.html and kensei-after.html.

ANSI/HTML pipeline approach inspired by joeynyc/hermes-skins (MIT).
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

import yaml
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

ROOT = Path(__file__).resolve().parents[1]
SKINS_DIR = ROOT / "skins"
HTML_OUT = ROOT / "screenshots" / "html"
PREVIEW_OUT = ROOT / "screenshots" / "preview"

CONSOLE_WIDTH = 108

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>{title}</title>
<style>
  html, body {{ margin:0; padding:0; background:{bg}; }}
  body {{ color:{fg}; font-family:'JetBrains Mono','Fira Code','Cascadia Code',Consolas,'Liberation Mono',monospace; font-size:13px; line-height:1.4; }}
  .skin-frame {{ padding:24px; background:{bg}; min-height:100vh; box-sizing:border-box; }}
  .skin-frame pre {{ margin:0; white-space:pre; font-family:inherit; color:{fg}; }}
  .skin-label {{ display:inline-block; padding:4px 10px; background:rgba(255,255,255,0.07); color:{fg}; font-family:inherit; font-size:11px; letter-spacing:1px; border-radius:3px; margin-bottom:14px; opacity:0.7; }}
</style>
</head>
<body><div class="skin-frame">{label_html}<pre>{code}</pre></div></body></html>
"""

CARD_TEMPLATE = (
    '<div class="skin-frame" style="background:{bg};color:{fg};padding:24px;min-height:100vh;box-sizing:border-box;">'
    '{label_html}'
    '<pre style="margin:0;white-space:pre;font-family:\'JetBrains Mono\',\'Fira Code\',Consolas,monospace;font-size:13px;line-height:1.4;color:{fg};">{code}</pre>'
    '</div>'
)

COMPARE_TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>KENSEI — current vs flagship-tier candidate</title>
<style>
  html, body {{ margin:0; padding:0; background:#0a0a0a; color:#fff;
                font-family:'JetBrains Mono','Fira Code',Consolas,monospace; }}
  .compare-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:0; }}
  .compare-cell {{ overflow:auto; border-right:1px solid rgba(255,255,255,0.08); }}
  .compare-cell:last-child {{ border-right:none; }}
  .compare-header {{ position:sticky; top:0; padding:8px 16px;
                     background:rgba(0,0,0,0.85); color:#FFD700;
                     font-size:11px; letter-spacing:2px;
                     border-bottom:1px solid rgba(255,255,255,0.15); z-index:10; }}
  @media (max-width: 1100px) {{ .compare-grid {{ grid-template-columns:1fr; }} }}
</style>
</head>
<body>
<div class="compare-grid">
  <div class="compare-cell"><div class="compare-header">CURRENT — skins/kensei.yaml</div>{card_a}</div>
  <div class="compare-cell"><div class="compare-header">FLAGSHIP CANDIDATE — skins/kensei.flagship-candidate.yaml</div>{card_b}</div>
</div>
</body></html>
"""


def render_skin(yaml_path: Path, label: str | None = None) -> tuple[str, str]:
    """Return (full_page_html, card_html_fragment) for the skin at yaml_path."""
    data = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
    colors = data.get("colors") or {}
    branding = data.get("branding") or {}
    spinner = data.get("spinner") or {}
    name = data.get("name", yaml_path.stem)

    console = Console(
        record=True,
        width=CONSOLE_WIDTH,
        force_terminal=True,
        color_system="truecolor",
        legacy_windows=False,
        emoji=False,
        markup=True,
        file=io.StringIO(),
    )

    banner_logo = data.get("banner_logo") or ""
    banner_hero = data.get("banner_hero") or ""
    if banner_logo:
        console.print(banner_logo)
    if banner_hero:
        console.print(banner_hero)
    console.print()

    welcome = branding.get("welcome") or ""
    if welcome:
        console.print(welcome)
    console.print()

    response_border = colors.get("response_border", "#FFFFFF")
    response_text_color = colors.get("response_text", colors.get("banner_text", "#FFFFFF"))
    response_label = branding.get("response_label", " Agent ")
    sample_body = Text(
        "Sample agent response. The agent answers, draws from context, and\n"
        "calls tools when needed. Lorem ipsum dolor sit amet, consectetur\n"
        "adipiscing elit, sed do eiusmod tempor incididunt ut labore.",
        style=response_text_color,
    )
    title_color = colors.get("banner_title", "#FFFFFF")
    response_panel = Panel(
        sample_body,
        border_style=response_border,
        title=f"[{title_color}]{response_label}[/]",
        title_align="left",
        width=CONSOLE_WIDTH - 4,
    )
    console.print(response_panel)
    console.print()

    if "reasoning_border" in colors:
        reasoning_border = colors["reasoning_border"]
        reasoning_text_color = colors.get("reasoning_text", "#CCCCCC")
        reasoning_panel = Panel(
            Text(
                "(reasoning) Considering options. Weighing the cleanest cut.\n"
                "Looking for the line of least noise.",
                style=reasoning_text_color,
            ),
            border_style=reasoning_border,
            title=f"[{reasoning_border}]reasoning[/]",
            title_align="left",
            width=CONSOLE_WIDTH - 4,
        )
        console.print(reasoning_panel)
        console.print()

    waiting_faces = spinner.get("waiting_faces") or ["(.)"]
    thinking_faces = spinner.get("thinking_faces") or ["(.)"]
    verbs = spinner.get("thinking_verbs") or ["thinking"]
    wings = spinner.get("wings") or []
    accent = colors.get("ui_accent", "#FFFFFF")
    label_color = colors.get("ui_label", "#CCCCCC")

    spinner_line = Text()
    wing_pair = wings[0] if wings else None
    if wing_pair and len(wing_pair) >= 2:
        spinner_line.append(f"{wing_pair[0]} ", style=accent)
    spinner_line.append(f"{thinking_faces[0]} ", style=accent)
    spinner_line.append(verbs[0], style=label_color)
    if wing_pair and len(wing_pair) >= 2:
        spinner_line.append(f" {wing_pair[1]}", style=accent)
    console.print(spinner_line)
    console.print()

    rule_line = Text("─" * (CONSOLE_WIDTH - 8), style=colors.get("input_rule", "#888888"))
    console.print(rule_line)
    prompt_line = Text()
    prompt_line.append(branding.get("prompt_symbol", "> "), style=colors.get("prompt", "#FFFFFF"))
    prompt_line.append("your message here", style=colors.get("banner_text", "#CCCCCC"))
    console.print(prompt_line)
    console.print()

    status_bg = colors.get("status_bar_bg", "#1a1a2e")
    status_text = colors.get("status_bar_text", "#FFFFFF")
    status_strong = colors.get("status_bar_strong", "#FFD700")
    status_dim = colors.get("status_bar_dim", "#888888")
    status_good = colors.get("status_bar_good", "#5B8C5A")
    status = Text()
    status.append(" model: ", style=f"{status_dim} on {status_bg}")
    status.append("claude-sonnet-4-6", style=f"{status_strong} on {status_bg}")
    status.append("  │  ", style=f"{status_dim} on {status_bg}")
    status.append("ctx: ", style=f"{status_dim} on {status_bg}")
    status.append("32k/200k", style=f"{status_text} on {status_bg}")
    status.append("  │  ", style=f"{status_dim} on {status_bg}")
    status.append("✓ ready", style=f"{status_good} on {status_bg}")
    pad = max(0, CONSOLE_WIDTH - 60)
    status.append(" " * pad, style=f"{status_text} on {status_bg}")
    console.print(status)

    code = console.export_html(inline_styles=True, code_format="{code}")

    bg = colors.get("status_bar_bg", "#0a0a0a")
    fg = colors.get("banner_text", "#e8dcc6")
    label_html = f'<div class="skin-label">{label}</div>' if label else ""

    full_page = PAGE_TEMPLATE.format(title=name, bg=bg, fg=fg, label_html=label_html, code=code)
    card_label_html = (
        f'<div class="skin-label" style="background:rgba(255,255,255,0.07);color:{fg};display:inline-block;padding:4px 10px;font-family:inherit;font-size:11px;letter-spacing:1px;border-radius:3px;margin-bottom:14px;opacity:0.7;">{label}</div>'
        if label
        else ""
    )
    card = CARD_TEMPLATE.format(bg=bg, fg=fg, label_html=card_label_html, code=code)
    return full_page, card


def main() -> int:
    HTML_OUT.mkdir(parents=True, exist_ok=True)
    PREVIEW_OUT.mkdir(parents=True, exist_ok=True)

    skin_files = sorted(SKINS_DIR.glob("*.yaml"))
    rendered = 0
    for path in skin_files:
        if "flagship-candidate" in path.stem:
            continue
        try:
            full_page, _card = render_skin(path)
        except Exception as exc:
            print(f"  [!] {path.name}: {exc}", file=sys.stderr)
            continue
        (HTML_OUT / f"{path.stem}.html").write_text(full_page, encoding="utf-8")
        rendered += 1
    print(f"Wrote {rendered} preview(s) to {HTML_OUT}")

    candidate = SKINS_DIR / "kensei.flagship-candidate.yaml"
    current = SKINS_DIR / "kensei.yaml"
    if candidate.exists() and current.exists():
        _, card_current = render_skin(current, label="CURRENT")
        _, card_candidate = render_skin(candidate, label="FLAGSHIP CANDIDATE")
        compare_html = COMPARE_TEMPLATE.format(card_a=card_current, card_b=card_candidate)
        (PREVIEW_OUT / "kensei-compare.html").write_text(compare_html, encoding="utf-8")
        full_current, _ = render_skin(current, label="CURRENT")
        full_candidate, _ = render_skin(candidate, label="FLAGSHIP CANDIDATE")
        (PREVIEW_OUT / "kensei-before.html").write_text(full_current, encoding="utf-8")
        (PREVIEW_OUT / "kensei-after.html").write_text(full_candidate, encoding="utf-8")
        print(f"Wrote comparison preview to {PREVIEW_OUT / 'kensei-compare.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
