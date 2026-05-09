#!/usr/bin/env python3
import argparse, re, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKINS_DIR = ROOT / 'skins'
SCREENSHOTS_DIR = ROOT / 'screenshots'
HEX_RE = re.compile(r'^#[0-9A-Fa-f]{6}$')
REQUIRED_COLORS = [
    'banner_border','banner_title','banner_accent','banner_dim','banner_text',
    'ui_accent','ui_label','ui_ok','ui_error','ui_warn',
    'prompt','input_rule','response_border','session_label','session_border',
    'status_bar_bg','status_bar_text','status_bar_strong','status_bar_dim',
    'status_bar_good','status_bar_warn','status_bar_bad','status_bar_critical',
    'voice_status_bg','completion_menu_bg','completion_menu_current_bg',
    'completion_menu_meta_bg','completion_menu_meta_current_bg',
]
OPTIONAL_EXTENDED_COLORS = [
    'response_text','reasoning_border','reasoning_text','selection_bg',
    'blade_glow','blade_edge',
]
REQUIRED_SPINNER = ['waiting_faces','thinking_faces','thinking_verbs','wings']
REQUIRED_BRANDING = ['agent_name','welcome','goodbye','response_label','prompt_symbol','help_header']

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--require-screenshots', action='store_true')
    args = ap.parse_args()
    errors=[]
    def err(skin,msg): errors.append(f'[{skin}] {msg}')
    files=sorted(SKINS_DIR.glob('*.yaml'))
    if not files:
        errors.append('No skins found')
    for path in files:
        skin=path.stem
        try:
            data=yaml.safe_load(path.read_text(encoding='utf-8')) or {}
        except Exception as e:
            err(skin, f'YAML parse error: {e}')
            continue
        if data.get('name') != skin:
            err(skin, f"name '{data.get('name')}' does not match filename '{skin}'")
        colors=data.get('colors') or {}
        for key in REQUIRED_COLORS:
            if key not in colors:
                err(skin, f'missing color key: {key}')
            elif not HEX_RE.match(str(colors[key])):
                err(skin, f'invalid color {key}: {colors[key]}')
        for key in OPTIONAL_EXTENDED_COLORS:
            if key in colors and not HEX_RE.match(str(colors[key])):
                err(skin, f'invalid extended color {key}: {colors[key]}')
        spinner=data.get('spinner') or {}
        for key in REQUIRED_SPINNER:
            if key not in spinner or not isinstance(spinner[key], list) or not spinner[key]:
                err(skin, f'spinner.{key} must be a non-empty list')
        branding=data.get('branding') or {}
        for key in REQUIRED_BRANDING:
            if key not in branding:
                err(skin, f'missing branding key: {key}')
        for field in ['banner_logo','banner_hero','tool_prefix']:
            if field not in data:
                err(skin, f'missing field: {field}')
        if args.require_screenshots and not (SCREENSHOTS_DIR / f'{skin}.png').exists():
            err(skin, f'missing screenshot: screenshots/{skin}.png')
    if errors:
        print(f'FAILED, {len(errors)} error(s):')
        for e in errors: print('  ' + e)
        return 1
    print(f'OK, {len(files)} skin(s) valid')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
