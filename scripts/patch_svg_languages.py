import os
import math

def generate_donut_block(is_dark=True):
    slices = [
        ('Jupyter Notebook', 34, '#DA5B0B'),
        ('TypeScript', 24, '#3178c6'),
        ('C++', 16, '#f34b7d'),
        ('C', 12, '#555555'),
        ('Nix', 8, '#5277C3'),
        ('Rust', 6, '#dea584'),
    ]

    R = 117
    r = 65

    text_fill = '#eeeeff' if is_dark else '#00000f'
    box_stroke = '#ffffff' if is_dark else '#00000f'
    slice_stroke = '#00000f' if is_dark else '#ffffff'

    current_angle = 0.0
    total_pct = sum(s[1] for s in slices)

    legend_rects = []
    legend_texts = []
    paths = []

    y_start = 35
    spacing = 28

    for idx, (name, pct, color) in enumerate(slices):
        y = y_start + idx * spacing
        text_y = y + 10
        legend_rects.append(
            f'<rect x="0" y="{y}" width="18" height="18" fill="{color}" stroke="{box_stroke}" stroke-width="1px">'
            f'<animate attributeName="fill-opacity" values="0;0.2;0.4;0.6;0.8;1;1;1;1;1" dur="3s" repeatCount="1"></animate>'
            f'</rect>'
        )
        legend_texts.append(
            f'<text dominant-baseline="middle" x="26" y="{text_y}" fill="{text_fill}" font-size="16px">'
            f'{name}'
            f'<animate attributeName="fill-opacity" values="0;0.2;0.4;0.6;0.8;1;1;1;1;1" dur="3s" repeatCount="1"></animate>'
            f'</text>'
        )

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

        d = (
            f'M{x1_out:.4f},{y1_out:.4f}A{R},{R},0,{large_arc},1,{x2_out:.4f},{y2_out:.4f}'
            f'L{x2_in:.4f},{y2_in:.4f}A{r},{r},0,{large_arc},0,{x1_in:.4f},{y1_in:.4f}Z'
        )
        paths.append(
            f'<path d="{d}" style="fill: {color};" stroke="{slice_stroke}" stroke-width="2px">'
            f'<title>{name} ({pct}%)</title>'
            f'<animate attributeName="fill-opacity" values="0;0.2;0.4;0.6;0.8;1;1;1;1;1" dur="3s" repeatCount="1"></animate>'
            f'</path>'
        )

    return (
        f'<g transform="translate(40, 520)">'
        f'<g transform="translate(273, 0)">{"".join(legend_rects)}{"".join(legend_texts)}</g>'
        f'<g transform="translate(130, 130)">{"".join(paths)}</g>'
        f'</g>'
    )

def update_svg_stats(svg_content):
    # 1. Total contributions: set to 1447
    import re
    c = re.sub(r'>\d{4,5}<', '>1447<', svg_content, count=1)
    # 2. Date range: set start to 2026-01-01
    c = re.sub(r'\d{4}-\d{2}-\d{2} / (2026-\d{2}-\d{2})', r'2026-01-01 / \1', c)
    # 3. Pull requests in radar and bottom stats
    c = c.replace('PullReq<title>2</title>', 'PullReq<title>24</title>')
    c = re.sub(r'>4<title>4</title></text>', '>24<title>24</title></text>', c)
    c = c.replace('23.86,32.84', '42.50,58.45')
    c = c.replace('23.86 32.84', '42.50 58.45')
    return c

def patch_directory(svg_dir):
    if not os.path.exists(svg_dir):
        return
    for f in os.listdir(svg_dir):
        if f.endswith('.svg'):
            p = os.path.join(svg_dir, f)
            with open(p, 'r') as fp:
                c = fp.read()
            s = c.find('<g transform="translate(40, 520)">')
            e = c.find('<g><text style="font-size: 32px', s)
            if s != -1 and e != -1:
                is_dark = ('night' in f)
                new_block = generate_donut_block(is_dark=is_dark)
                c = c[:s] + new_block + c[e:]
            c = update_svg_stats(c)
            with open(p, 'w') as fp:
                fp.write(c)
            print(f"Successfully patched {f}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dirs = [
        os.path.join(base_dir, "profile-3d-contrib"),
        "/home/akashbiswas/Downloads/blu3-bird/profile-3d-contrib",
    ]
    for d in target_dirs:
        patch_directory(d)
