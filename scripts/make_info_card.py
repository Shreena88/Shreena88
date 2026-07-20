import os
import html

def generate_info_card_svg(output_path):
    bg_color = "#0d1117"
    border_color = "#30363d"
    title_bar_bg = "#161b22"
    prompt_color = "#3fb950"  # GitHub green
    key_color = "#58a6ff"     # Blue accent for keys
    val_color = "#c9d1d9"     # Light gray/white text
    sub_color = "#8b949e"     # Subdued gray

    sections = [
        ("Username", "shreena88@github"),
        ("Education", "BSc Information Technology"),
        ("Role", "AI & Machine Learning Student"),
        ("Focus", "Artificial Intelligence", "Computer Vision", "Natural Language Processing","Machine Learning"),
        ("Backend", "FastAPI", "Flask"),
        ("Database", "MongoDB", "MySQL"),
        ("Languages", "Python", "C++", "Java"),
        ("Frontend", "HTML", "CSS", "JavaScript"),
    ]

    width = 540
    formatted_lines = []
    formatted_lines.append(("prompt", "shreena88@github:~$ neofetch"))
    formatted_lines.append(("divider", "------------------------------------------"))

    for key, val in sections:
        if isinstance(val, list):
            formatted_lines.append(("key", f"{key}:"))
            for v in val:
                formatted_lines.append(("val", f"  {v}"))
        else:
            formatted_lines.append(("key_val", (f"{key}:", f" {val}")))

    formatted_lines.append(("divider", "------------------------------------------"))

    line_height = 20
    start_y = 65
    content_height = start_y + len(formatted_lines) * line_height + 25
    height = max(content_height, 580)

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append('  <style>')
    svg.append('    .bg { fill: ' + bg_color + '; rx: 10px; ry: 10px; stroke: ' + border_color + '; stroke-width: 1.5; }')
    svg.append('    .title-bar { fill: ' + title_bar_bg + '; rx: 10px; ry: 10px; }')
    svg.append('    .term-title { font-family: "Fira Code", "Consolas", monospace; font-size: 13px; fill: ' + sub_color + '; font-weight: 600; }')
    svg.append('    .txt { font-family: "Fira Code", "Consolas", monospace; font-size: 13px; }')
    svg.append('    .p-user { fill: ' + prompt_color + '; font-weight: 700; }')
    svg.append('    .p-host { fill: ' + key_color + '; font-weight: 700; }')
    svg.append('    .key { fill: ' + key_color + '; font-weight: 600; }')
    svg.append('    .val { fill: ' + val_color + '; }')
    svg.append('    .sub { fill: ' + sub_color + '; }')
    svg.append('  </style>')

    # Clip paths definitions for clean SMIL row reveals
    svg.append('  <defs>')
    delay = 0.05
    for i in range(len(formatted_lines)):
        y_pos = start_y + i * line_height
        delay_str = f"{delay:.2f}s"
        svg.append(f'    <clipPath id="ic-clip-{i}">')
        svg.append(f'      <rect x="20" y="{y_pos - 15}" width="0" height="24">')
        svg.append(f'        <animate attributeName="width" from="0" to="{width - 40}" begin="{delay_str}" dur="0.25s" fill="freeze" repeatCount="1" />')
        svg.append(f'      </rect>')
        svg.append(f'    </clipPath>')
        delay += 0.03
    svg.append('  </defs>')

    # Background & Window Chrome
    svg.append(f'  <rect width="{width}" height="{height}" class="bg" />')
    svg.append(f'  <rect width="{width}" height="38" class="title-bar" />')
    svg.append(f'  <rect width="{width}" height="10" y="28" fill="{title_bar_bg}" />')
    
    # Title bar buttons & label
    svg.append('  <circle cx="20" cy="19" r="6" fill="#ff5f56" />')
    svg.append('  <circle cx="40" cy="19" r="6" fill="#ffbd2e" />')
    svg.append('  <circle cx="60" cy="19" r="6" fill="#27c93f" />')
    svg.append(f'  <text x="{width/2}" y="24" text-anchor="middle" class="term-title">shreena88@github: ~/neofetch</text>')

    # Helper function to escape XML text
    def esc(t):
        return html.escape(str(t))

    # Lines rendering with clip-path
    for i, item in enumerate(formatted_lines):
        kind = item[0]
        y_pos = start_y + i * line_height

        if kind == "prompt":
            svg.append(f'  <text x="25" y="{y_pos}" class="txt" clip-path="url(#ic-clip-{i})">')
            svg.append(f'    <tspan class="p-user">shreena88</tspan><tspan class="sub">@</tspan><tspan class="p-host">github</tspan><tspan class="val">:~$ neofetch</tspan>')
            svg.append(f'  </text>')
        elif kind == "divider":
            svg.append(f'  <text x="25" y="{y_pos}" class="txt sub" clip-path="url(#ic-clip-{i})">{esc(item[1])}</text>')
        elif kind == "key_val":
            k, v = item[1]
            svg.append(f'  <text x="25" y="{y_pos}" class="txt" clip-path="url(#ic-clip-{i})">')
            svg.append(f'    <tspan class="key">{esc(k)}</tspan><tspan class="val">{esc(v)}</tspan>')
            svg.append(f'  </text>')
        elif kind == "key":
            svg.append(f'  <text x="25" y="{y_pos}" class="txt key" clip-path="url(#ic-clip-{i})">{esc(item[1])}</text>')
        elif kind == "val":
            svg.append(f'  <text x="25" y="{y_pos}" class="txt val" clip-path="url(#ic-clip-{i})">{esc(item[1])}</text>')

    svg.append('</svg>')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"info-card.svg successfully written to {output_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_file = os.path.join(base_dir, "assets", "info-card.svg")
    generate_info_card_svg(output_file)
