import subprocess
from datetime import datetime, timezone, timedelta

ist = timezone(timedelta(hours=5, minutes=30))
out = subprocess.check_output(['git', 'log', '--format=%aI'], cwd='/home/akashbiswas/Downloads/akashbiswas7074').decode()
hours = [0]*24
for line in out.strip().split('\n'):
    if not line: continue
    dt = datetime.fromisoformat(line).astimezone(ist)
    hours[dt.hour] += 1

max_val = max(hours)
print(f"Max commits in an hour: {max_val}")

# We will create a pristine SVG card matching the exact dimensions and theme
# Card width: 360, height: 210
# Chart area: x: 45 to 325 (width 280), y: 65 to 165 (height 100)
chart_x = 42
chart_y = 65
chart_w = 288
chart_h = 100
y_max = 350 # upper scale bound

bar_w = 9.5
gap = (chart_w - (24 * bar_w)) / 23

bars_svg = []
for h in range(24):
    cnt = hours[h]
    b_h = (cnt / y_max) * chart_h
    bx = chart_x + h * (bar_w + gap)
    by = chart_y + chart_h - b_h
    if b_h > 0:
        bars_svg.append(f'<rect class="bar" x="{bx:.2f}" y="{by:.2f}" width="{bar_w:.2f}" height="{b_h:.2f}" rx="2" fill="url(#barGrad)"><title>{h:02d}:00 IST: {cnt} commits</title></rect>')
    else:
        # minimal zero dot
        bars_svg.append(f'<rect class="bar zero" x="{bx:.2f}" y="{chart_y + chart_h - 1:.2f}" width="{bar_w:.2f}" height="1" fill="#21262D"/>')

svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="360" height="210" viewBox="0 0 360 210">
  <defs>
    <linearGradient id="yujiroBorder" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FF2A55"/>
      <stop offset="50%" stop-color="#FF5400"/>
      <stop offset="100%" stop-color="#800F2F"/>
    </linearGradient>
    <linearGradient id="barGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FF2A55"/>
      <stop offset="100%" stop-color="#800F2F"/>
    </linearGradient>
    <radialGradient id="ogreGlow" cx="50%" cy="40%" r="50%">
      <stop offset="0%" stop-color="#FF2A55" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#0D1117" stop-opacity="0"/>
    </radialGradient>
    <style>
      .title {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Ubuntu, sans-serif; font-size: 18px; font-weight: 600; fill: #FF2A55; }}
      .sub {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Ubuntu, sans-serif; font-size: 10px; fill: #8B949E; }}
      .axis-label {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Ubuntu, sans-serif; font-size: 10px; fill: #C9D1D9; text-anchor: middle; }}
      .y-label {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Ubuntu, sans-serif; font-size: 9px; fill: #8B949E; text-anchor: end; }}
      .grid {{ stroke: #21262D; stroke-width: 1; stroke-dasharray: 2 2; }}
      .axis {{ stroke: #30363D; stroke-width: 1; }}
      .bar:hover {{ fill: #FF758F; filter: drop-shadow(0 0 5px #FF2A55); cursor: pointer; }}
    </style>
  </defs>

  <!-- Background card -->
  <rect x="1" y="1" width="358" height="208" rx="8" fill="#0D1117" stroke="url(#yujiroBorder)" stroke-width="1.5"/>
  <rect x="1" y="1" width="358" height="208" rx="8" fill="url(#ogreGlow)"/>

  <!-- Header -->
  <text x="32" y="38" class="title">Commits (UTC +5:30)</text>
  <text x="32" y="52" class="sub">Peak coding: 09:00 - 22:00 IST · Total: {sum(hours):,} commits</text>

  <!-- Y Axis Grid & Labels -->
  <line x1="{chart_x}" y1="{chart_y}" x2="{chart_x + chart_w}" y2="{chart_y}" class="grid"/>
  <text x="{chart_x - 6}" y="{chart_y + 3}" class="y-label">300</text>

  <line x1="{chart_x}" y1="{chart_y + chart_h/2}" x2="{chart_x + chart_w}" y2="{chart_y + chart_h/2}" class="grid"/>
  <text x="{chart_x - 6}" y="{chart_y + chart_h/2 + 3}" class="y-label">150</text>

  <line x1="{chart_x}" y1="{chart_y + chart_h}" x2="{chart_x + chart_w}" y2="{chart_y + chart_h}" class="axis"/>
  <text x="{chart_x - 6}" y="{chart_y + chart_h + 3}" class="y-label">0</text>

  <!-- Bars -->
  {''.join(bars_svg)}

  <!-- X Axis Ticks & Labels -->
  <g transform="translate(0, {chart_y + chart_h + 14})">
    <text x="{chart_x + (0 * (bar_w + gap)) + bar_w/2:.1f}" class="axis-label">0</text>
    <text x="{chart_x + (6 * (bar_w + gap)) + bar_w/2:.1f}" class="axis-label">6</text>
    <text x="{chart_x + (12 * (bar_w + gap)) + bar_w/2:.1f}" class="axis-label">12</text>
    <text x="{chart_x + (18 * (bar_w + gap)) + bar_w/2:.1f}" class="axis-label">18</text>
    <text x="{chart_x + (23 * (bar_w + gap)) + bar_w/2:.1f}" class="axis-label">23</text>
    <text x="{chart_x + chart_w}" class="axis-label" style="text-anchor: end; fill: #8B949E; font-size: 9px;">hour of day</text>
  </g>
</svg>'''

with open("/home/akashbiswas/Downloads/akashbiswas7074/assets/productive-hours.svg", "w") as f:
    f.write(svg_content)

with open("/home/akashbiswas/Downloads/blu3-bird/assets/productive-hours.svg", "w") as f:
    f.write(svg_content)

print("Generated assets/productive-hours.svg successfully!")
