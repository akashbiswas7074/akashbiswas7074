import os
import re
import math

SVG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "profile-3d-contrib")

slices = [
    ('Jupyter Notebook', 32, '#DA5B0B'),
    ('TypeScript', 26, '#3178c6'),
    ('C++', 16, '#f34b7d'),
    ('C', 12, '#555555'),
    ('Rust', 8, '#dea584'),
    ('Nix', 6, '#7e7eff'),
]

R = 117
r = 65

current_angle = 0.0
total_pct = sum(s[1] for s in slices)

legend_rects = []
legend_texts = []
paths = []

y_start = 35
spacing = 28

for idx, (name, pct, color) in enumerate(slices):
    y = y_start + idx * spacing
    text_y = y + 9
    legend_rects.append(f'<rect x="0" y="{y}" width="18" height="18" fill="{color}" stroke="#ffffff" stroke-width="1px"><animate attributeName="fill-opacity" values="0;0.2;0.4;0.6;0.8;1;1;1;1;1" dur="3s" repeatCount="1"></animate></rect>')
    legend_texts.append(f'<text dominant-baseline="middle" x="26" y="{text_y}" fill="#eeeeff" font-size="16px">{name}<animate attributeName="fill-opacity" values="0;0.2;0.4;0.6;0.8;1;1;1;1;1" dur="3s" repeatCount="1"></animate></text>')

    angle_span = 2 * math.pi * (pct / total_pct)
    a1 = current_angle
    a2 = current_angle + angle_span
    current_angle = a2
    
    x1_out = R * math.sin(a1)
    y1_out = -R * math.cos(a1)
    x2_out = R * math.sin(a2)
    y2_out = -R * math.cos(a2)
    
    x1_in = r * math.sin(a1)
    y1_in = -r * math.cos(a1)
    x2_in = r * math.sin(a2)
    y2_in = -r * math.cos(a2)
    
    large_arc = 1 if (a2 - a1) > math.pi else 0
    
    d = f'M{x1_out:.4f},{y1_out:.4f}A{R},{R},0,{large_arc},1,{x2_out:.4f},{y2_out:.4f}L{x2_in:.4f},{y2_in:.4f}A{r},{r},0,{large_arc},0,{x1_in:.4f},{y1_in:.4f}Z'
    paths.append(f'<path d="{d}" style="fill: {color};" stroke="#00000f" stroke-width="2px"><title>{name} ({pct}%)</title><animate attributeName="fill-opacity" values="0;0.2;0.4;0.6;0.8;1;1;1;1;1" dur="3s" repeatCount="1"></animate></path>')

custom_donut_xml = f'<g transform="translate(40, 520)"><g transform="translate(273, 0)">{"".join(legend_rects)}{"".join(legend_texts)}</g><g transform="translate(130, 130)">{"".join(paths)}</g></g>'

pattern = re.compile(r'<g transform="translate\(40, 520\)">.*?</g></g>', re.DOTALL)

for f in os.listdir(SVG_DIR):
    if f.endswith('.svg'):
        p = os.path.join(SVG_DIR, f)
        with open(p, 'r') as fp:
            c = fp.read()
        nc = pattern.sub(custom_donut_xml, c)
        with open(p, 'w') as fp:
            fp.write(nc)
        print(f'Patched {f}')
