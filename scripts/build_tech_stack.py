import re
import os
import subprocess

TECH_STACK_SVG = "/home/akashbiswas/Downloads/akashbiswas7074/assets/tech-stack.svg"
PREVIEW_SVG = "/home/akashbiswas/Downloads/blu3-bird/assets/tech-stack.svg"
CACHE_DIR = "/home/akashbiswas/Downloads/akashbiswas7074/scripts/icon_cache"

# 1. Load original 22 icons directly from commit 5c919701 (clean baseline with zero duplicates)
data = subprocess.check_output(["git", "show", "5c919701:assets/tech-stack.svg"], cwd="/home/akashbiswas/Downloads/akashbiswas7074").decode("utf-8")
raw_svgs = re.findall(r"(<svg width=\"48\" height=\"48\".*?<\/svg>)", data, re.DOTALL)
orig_names = [
    "python", "javascript", "typescript", "html5", "css3", "flask",
    "django", "fastapi", "tensorflow", "pytorch", "nixos", "nextjs",
    "scikitlearn", "postgresql", "mysql", "sqlite", "docker", "linux",
    "git", "github", "vscode", "neovim"
]
orig_map = dict(zip(orig_names, raw_svgs))

def make_simple_icon(slug, bg, fill, scale=6.6667, translate=(48, 48)):
    cache_file = os.path.join(CACHE_DIR, f"{slug}.svg")
    with open(cache_file, "r") as f:
        svg_content = f.read()

    paths = re.findall(r'<path[^>]*d="([^"]+)"', svg_content)
    path_elements = "".join([f'<path fill="{fill}" d="{p}"/>' for p in paths])
    tx, ty = translate
    return f'''<svg width="48" height="48" viewBox="0 0 256 256" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="256" height="256" fill="{bg}" rx="60"/>
  <g transform="translate({tx}, {ty}) scale({scale})">
    {path_elements}
  </g>
</svg>'''

def make_devicon(filename, bg, scale=1.25, translate=(48, 48)):
    cache_file = os.path.join(CACHE_DIR, filename)
    with open(cache_file, "r") as f:
        svg_content = f.read()

    inner = re.search(r'<svg[^>]*>(.*?)</svg>', svg_content, re.DOTALL).group(1).strip()
    tx, ty = translate
    return f'''<svg width="48" height="48" viewBox="0 0 256 256" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="256" height="256" fill="{bg}" rx="60"/>
  <g transform="translate({tx}, {ty}) scale({scale})">
    {inner}
  </g>
</svg>'''

# 7 Rows x 11 Icons = 77 Unique Tech Icons (0 duplicates)
ROWS = [
    # Row 1: Core Programming & Systems Languages
    [
        ("c", lambda: make_simple_icon("c", "#1B222D", "#A8B9CC")),
        ("cplusplus", lambda: make_devicon("cplusplus_cplusplus-original.svg", "#1B222D", scale=1.25, translate=(48, 48))),
        ("rust", lambda: make_simple_icon("rust", "#CE412B", "#FFFFFF")),
        ("go", lambda: make_simple_icon("go", "#00ADD8", "#FFFFFF")),
        ("java", lambda: make_devicon("java_java-original.svg", "#1B222D", scale=1.25, translate=(48, 48))),
        ("kotlin", lambda: make_simple_icon("kotlin", "#7F52FF", "#FFFFFF")),
        ("python", lambda: orig_map["python"]),
        ("typescript", lambda: orig_map["typescript"]),
        ("javascript", lambda: orig_map["javascript"]),
        ("nixos", lambda: orig_map["nixos"]),
        ("gnubash", lambda: make_simple_icon("gnubash", "#242938", "#4EAA25")),
    ],
    # Row 2: AI / Machine Learning, Deep Learning & Data Science (1st Priority!)
    [
        ("pytorch", lambda: orig_map["pytorch"]),
        ("tensorflow", lambda: orig_map["tensorflow"]),
        ("scikitlearn", lambda: orig_map["scikitlearn"]),
        ("opencv", lambda: make_simple_icon("opencv", "#5C3EE8", "#FFFFFF")),
        ("pandas", lambda: make_simple_icon("pandas", "#150458", "#FFFFFF")),
        ("numpy", lambda: make_simple_icon("numpy", "#013243", "#FFFFFF")),
        ("jupyter", lambda: make_simple_icon("jupyter", "#F37626", "#FFFFFF")),
        ("huggingface", lambda: make_simple_icon("huggingface", "#FFD21E", "#000000")),
        ("keras", lambda: make_simple_icon("keras", "#D00000", "#FFFFFF")),
        ("fastapi", lambda: orig_map["fastapi"]),
        ("binance", lambda: make_simple_icon("binance", "#F0B90B", "#FFFFFF")),
    ],
    # Row 3: Game Development & Computer Graphics / 3D
    [
        ("unrealengine", lambda: make_simple_icon("unrealengine", "#0E1128", "#FFFFFF")),
        ("unity", lambda: make_simple_icon("unity", "#000000", "#FFFFFF")),
        ("godotengine", lambda: make_simple_icon("godotengine", "#478CBF", "#FFFFFF")),
        ("blender", lambda: make_simple_icon("blender", "#EA7600", "#FFFFFF")),
        ("opengl", lambda: make_simple_icon("opengl", "#5586A4", "#FFFFFF")),
        ("webgl", lambda: make_simple_icon("webgl", "#990000", "#FFFFFF")),
        ("threedotjs", lambda: make_simple_icon("threedotjs", "#000000", "#FFFFFF")),
        ("vulkan", lambda: make_simple_icon("vulkan", "#AC162C", "#FFFFFF")),
        ("raylib", lambda: make_simple_icon("raylib", "#FFFFFF", "#000000")),
        ("webassembly", lambda: make_simple_icon("webassembly", "#654FF0", "#FFFFFF")),
        ("steam", lambda: make_simple_icon("steam", "#171A21", "#FFFFFF")),
    ],
    # Row 4: MERN Stack & Modern Web Frameworks
    [
        ("mongodb", lambda: make_simple_icon("mongodb", "#13AA52", "#FFFFFF")),
        ("express", lambda: make_simple_icon("express", "#000000", "#FFFFFF")),
        ("react", lambda: make_simple_icon("react", "#20232A", "#61DAFB")),
        ("nodedotjs", lambda: make_simple_icon("nodedotjs", "#339933", "#FFFFFF")),
        ("nextjs", lambda: orig_map["nextjs"]),
        ("bun", lambda: make_simple_icon("bun", "#1F1E1E", "#FBF0DF")),
        ("tailwindcss", lambda: make_simple_icon("tailwindcss", "#06B6D4", "#FFFFFF")),
        ("vuedotjs", lambda: make_simple_icon("vuedotjs", "#4FC08D", "#FFFFFF")),
        ("graphql", lambda: make_simple_icon("graphql", "#E10098", "#FFFFFF")),
        ("html5", lambda: orig_map["html5"]),
        ("css3", lambda: orig_map["css3"]),
    ],
    # Row 5: Mobile App Development & UI/UX Design
    [
        ("android", lambda: make_simple_icon("android", "#3DDC84", "#FFFFFF")),
        ("flutter", lambda: make_simple_icon("flutter", "#02569B", "#FFFFFF")),
        ("apple", lambda: make_simple_icon("apple", "#000000", "#FFFFFF")),
        ("figma", lambda: make_simple_icon("figma", "#1E1E1E", "#F24E1E")),
        ("framer", lambda: make_simple_icon("framer", "#0055FF", "#FFFFFF")),
        ("storybook", lambda: make_simple_icon("storybook", "#FF4785", "#FFFFFF")),
        ("postman", lambda: make_simple_icon("postman", "#FF6C37", "#FFFFFF")),
        ("vite", lambda: make_simple_icon("vite", "#1B222D", "#BD34FE")),
        ("terraform", lambda: make_simple_icon("terraform", "#7B42BC", "#FFFFFF")),
        ("django", lambda: orig_map["django"]),
        ("flask", lambda: orig_map["flask"]),
    ],
    # Row 6: Cloud Computing, DevOps & Databases
    [
        ("aws", lambda: make_devicon("amazonwebservices_amazonwebservices-original-wordmark.svg", "#232F3E", scale=1.1, translate=(44, 52))),
        ("googlecloud", lambda: make_simple_icon("googlecloud", "#1B222D", "#4285F4")),
        ("azure", lambda: make_devicon("azure_azure-original.svg", "#0078D4", scale=1.25, translate=(48, 48))),
        ("docker", lambda: orig_map["docker"]),
        ("kubernetes", lambda: make_simple_icon("kubernetes", "#326CE5", "#FFFFFF")),
        ("linux", lambda: orig_map["linux"]),
        ("postgresql", lambda: orig_map["postgresql"]),
        ("mysql", lambda: orig_map["mysql"]),
        ("sqlite", lambda: orig_map["sqlite"]),
        ("redis", lambda: make_simple_icon("redis", "#DC382D", "#FFFFFF")),
        ("nginx", lambda: make_simple_icon("nginx", "#009639", "#FFFFFF")),
    ],
    # Row 7: Blockchain, Web3 & Developer Tools
    [
        ("ethereum", lambda: make_simple_icon("ethereum", "#3C3C3D", "#FFFFFF")),
        ("solana", lambda: make_simple_icon("solana", "#1B222D", "#14F195")),
        ("bitcoin", lambda: make_simple_icon("bitcoin", "#F7931A", "#FFFFFF")),
        ("solidity", lambda: make_simple_icon("solidity", "#363636", "#FFFFFF")),
        ("polygon", lambda: make_simple_icon("polygon", "#8247E5", "#FFFFFF")),
        ("web3dotjs", lambda: make_simple_icon("web3dotjs", "#F16822", "#FFFFFF")),
        ("chainlink", lambda: make_simple_icon("chainlink", "#375BD2", "#FFFFFF")),
        ("ipfs", lambda: make_simple_icon("ipfs", "#65C2CB", "#FFFFFF")),
        ("git", lambda: orig_map["git"]),
        ("github", lambda: orig_map["github"]),
        ("neovim", lambda: orig_map["neovim"]),
    ]
]

# Generate composite SVG
out_lines = [
    '<svg width="704" height="448" viewBox="0 0 704 448"',
    '  xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
]

seen_names = set()
for row_idx, row in enumerate(ROWS):
    y = 8 + row_idx * 64
    for col_idx, (name, fn) in enumerate(row):
        assert name not in seen_names, f"Duplicate detected: {name}"
        seen_names.add(name)
        x = 8 + col_idx * 64
        # Calculate smooth diagonal floating delay
        delay = round(((row_idx * 0.15) + (col_idx * 0.08)) % 2.0, 2)
        icon_svg = fn()
        out_lines.append(f'  <g transform="translate({x},{y})">')
        out_lines.append('    <g transform="translate(0,0)">')
        out_lines.append('      <g>')
        out_lines.append('        <animateTransform attributeName="transform" type="translate"')
        out_lines.append(f'          values="0 0; 0 -8; 0 0" dur="2s" begin="{delay}s" repeatCount="indefinite"')
        out_lines.append('          calcMode="spline" keySplines="0.45 0 0.55 1; 0.45 0 0.55 1" keyTimes="0; 0.5; 1"/>')
        out_lines.append(f'        {icon_svg}')
        out_lines.append('      </g>')
        out_lines.append('    </g>')
        out_lines.append('  </g>')

out_lines.append('</svg>\n')
final_svg = "\n".join(out_lines)

with open(TECH_STACK_SVG, "w") as f:
    f.write(final_svg)

with open(PREVIEW_SVG, "w") as f:
    f.write(final_svg)

print(f"Successfully generated {TECH_STACK_SVG} and {PREVIEW_SVG} with {len(seen_names)} UNIQUE icons!")
