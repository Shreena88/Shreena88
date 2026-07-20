import os

def generate_info_card_svg(output_path):
    # Standard terminal styling
    bg_color = "#0d1117"
    border_color = "#30363d"
    title_bar_bg = "#161b22"
    prompt_color = "#3fb950"  # GitHub green
    key_color = "#58a6ff"     # Blue accent for keys
    val_color = "#c9d1d9"     # Light gray/white text
    sub_color = "#8b949e"     # Subdued gray
    accent_green = "#2ea043"

    # Exact information specified in prompt:
    sections = [
        ("Username", "shreena88@github"),
        ("Education", "BSc Information Technology"),
        ("Role", "AI & Machine Learning Student"),
        ("Location", "India"),
        ("Focus", ["Artificial Intelligence", "Computer Vision", "Natural Language Processing"]),
        ("Backend", ["FastAPI", "Flask"]),
        ("Database", ["MongoDB", "MySQL"]),
        ("Languages", ["Python", "C++", "Java"]),
        ("Frontend", ["HTML", "CSS", "JavaScript"]),
    ]

    projects = [
        "Agentic workflow automation",
        "Medical Report Analyzer",
        "Datasense-AI",
        "Briefly",
        "Email Spam Detection"
    ]

    # Calculate layout dimensions
    width = 540
    # Let's count total lines for vertical sizing
    # Title bar + padding + items + projects
    # Let's format lines
    formatted_lines = []
    
    formatted_lines.append(("prompt", "shreena88@github:~$ neofetch"))
    formatted_lines.append(("divider", "-" * 42))

    for key, val in sections:
        if isinstance(val, list):
            formatted_lines.append(("key", f"{key}:"))
            for v in val:
                formatted_lines.append(("val", f"  {v}"))
        else:
            formatted_lines.append(("key_val", (f"{key}:", f" {val}")))

    formatted_lines.append(("divider", "-" * 42))
    formatted_lines.append(("header", "Projects"))
    for proj in projects:
        formatted_lines.append(("bullet", f"• {proj}"))

    line_height = 20
    start_y = 65
    content_height = start_y + len(formatted_lines) * line_height + 25
    height = max(content_height, 680)

    # Build SVG content with SMIL and CSS animations
    svg_lines = []
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg_lines.append('  <style>')
    svg_lines.append('    @import url("https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600;700&amp;display=swap");')
    svg_lines.append('    .bg { fill: ' + bg_color + '; rx: 10px; ry: 10px; stroke: ' + border_color + '; stroke-width: 1.5; }')
    svg_lines.append('    .title-bar { fill: ' + title_bar_bg + '; rx: 10px; ry: 10px; }')
    svg_lines.append('    .term-title { font-family: "Fira Code", monospace; font-size: 13px; fill: ' + sub_color + '; font-weight: 600; }')
    svg_lines.append('    .txt { font-family: "Fira Code", "Consolas", monospace; font-size: 13px; }')
    svg_lines.append('    .p-user { fill: ' + prompt_color + '; font-weight: 700; }')
    svg_lines.append('    .p-host { fill: ' + key_color + '; font-weight: 700; }')
    svg_lines.append('    .key { fill: ' + key_color + '; font-weight: 600; }')
    svg_lines.append('    .val { fill: ' + val_color + '; }')
    svg_lines.append('    .sub { fill: ' + sub_color + '; }')
    svg_lines.append('    .proj-head { fill: ' + prompt_color + '; font-weight: 700; font-size: 14px; }')
    svg_lines.append('    .proj-bullet { fill: ' + val_color + '; font-weight: 500; }')
    svg_lines.append('    ')
    svg_lines.append('    /* Staggered Line Animation */')
    svg_lines.append('    .animated-line {')
    svg_lines.append('      opacity: 0;')
    svg_lines.append('      transform: translateY(12px);')
    svg_lines.append('      animation: fadeInUp 0.4s ease-out forwards;')
    svg_lines.append('    }')
    svg_lines.append('    @keyframes fadeInUp {')
    svg_lines.append('      to {')
    svg_lines.append('        opacity: 1;')
    svg_lines.append('        transform: translateY(0);')
    svg_lines.append('      }')
    svg_lines.append('    }')
    svg_lines.append('  </style>')

    # Background & Window Chrome
    svg_lines.append(f'  <rect width="{width}" height="{height}" class="bg" />')
    svg_lines.append(f'  <rect width="{width}" height="38" class="title-bar" />')
    svg_lines.append(f'  <rect width="{width}" height="10" y="28" fill="{title_bar_bg}" />') # clip bottom corners of titlebar
    
    # Title bar buttons
    svg_lines.append('  <circle cx="20" cy="19" r="6" fill="#ff5f56" />')
    svg_lines.append('  <circle cx="40" cy="19" r="6" fill="#ffbd2e" />')
    svg_lines.append('  <circle cx="60" cy="19" r="6" fill="#27c93f" />')
    svg_lines.append(f'  <text x="{width/2}" y="24" text-anchor="middle" class="term-title">shreena88@github: ~/neofetch</text>')

    # Lines rendering
    y_pos = start_y
    delay = 0.05

    for item in formatted_lines:
        kind = item[0]
        delay_str = f"{delay:.2f}s"

        svg_lines.append(f'  <g class="animated-line" style="animation-delay: {delay_str};">')

        if kind == "prompt":
            svg_lines.append(f'    <text x="25" y="{y_pos}" class="txt">')
            svg_lines.append(f'      <tspan class="p-user">shreena88</tspan><tspan class="sub">@</tspan><tspan class="p-host">github</tspan><tspan class="val">:~$ neofetch</tspan>')
            svg_lines.append(f'    </text>')
        elif kind == "divider":
            svg_lines.append(f'    <text x="25" y="{y_pos}" class="txt sub">{item[1]}</text>')
        elif kind == "key_val":
            k, v = item[1]
            svg_lines.append(f'    <text x="25" y="{y_pos}" class="txt">')
            svg_lines.append(f'      <tspan class="key">{k}</tspan><tspan class="val">{v}</tspan>')
            svg_lines.append(f'    </text>')
        elif kind == "key":
            svg_lines.append(f'    <text x="25" y="{y_pos}" class="txt key">{item[1]}</text>')
        elif kind == "val":
            svg_lines.append(f'    <text x="25" y="{y_pos}" class="txt val">{item[1]}</text>')
        elif kind == "header":
            svg_lines.append(f'    <text x="25" y="{y_pos}" class="txt proj-head">{item[1]}</text>')
        elif kind == "bullet":
            svg_lines.append(f'    <text x="25" y="{y_pos}" class="txt proj-bullet">{item[1]}</text>')

        svg_lines.append('  </g>')
        y_pos += line_height
        delay += 0.04

    svg_lines.append('</svg>')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
    print(f"info-card.svg successfully written to {output_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_file = os.path.join(base_dir, "assets", "info-card.svg")
    generate_info_card_svg(output_file)
