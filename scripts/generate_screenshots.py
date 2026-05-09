#!/usr/bin/env python3
"""Render simple HTML previews for all skins. PNG capture can be added via html2image once Chromium is available."""
from pathlib import Path
import html, yaml
ROOT = Path(__file__).resolve().parents[1]
out = ROOT / 'screenshots' / 'html'
out.mkdir(parents=True, exist_ok=True)
for path in sorted((ROOT/'skins').glob('*.yaml')):
    data = yaml.safe_load(path.read_text(encoding='utf-8')) or {}
    c = data.get('colors', {})
    body = f"""
<html><body style="margin:0;background:{c.get('status_bar_bg','#0d1117')};color:{c.get('banner_text','#fff')};font:16px monospace;">
<pre style="padding:24px;border:2px solid {c.get('banner_border','#888')};white-space:pre-wrap;">
{html.escape(data.get('banner_logo',''))}

{html.escape(data.get('banner_hero',''))}

{html.escape(data.get('description',''))}

Response label: {html.escape((data.get('branding') or {}).get('response_label',''))}
Prompt: {html.escape((data.get('branding') or {}).get('prompt_symbol',''))}
</pre></body></html>
"""
    (out / f'{path.stem}.html').write_text(body, encoding='utf-8')
print(f'Wrote HTML previews to {out}')
