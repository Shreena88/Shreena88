import os
import json
from datetime import datetime

def render_heatmap_svg(json_path, output_svg_path):
    print(f"Reading contribution data from {json_path}...")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    days = data.get("days", [])
    total_contribs = data.get("total_contributions", 0)
    current_streak = data.get("current_streak", 0)
    longest_streak = data.get("longest_streak", 0)
    best_day = data.get("best_day", {"date": "N/A", "count": 0})
    
    # Format best day date nicely e.g. "2026-06-07" -> "Jun 7, 2026"
    best_day_str = best_day["date"]
    if best_day_str != "N/A":
        try:
            dt = datetime.strptime(best_day_str, "%Y-%m-%d")
            best_day_str = dt.strftime("%b %d, %Y")
        except ValueError:
            pass
            
    # GitHub Level Colors
    level_colors = [
        "#161b22",  # Level 0
        "#0e4429",  # Level 1
        "#006d32",  # Level 2
        "#26a641",  # Level 3
        "#39d353"   # Level 4
    ]
    
    # Dimensions & Layout
    cell_size = 11
    cell_gap = 3
    stride = cell_size + cell_gap
    
    start_x = 45
    start_y = 75
    
    num_weeks = (len(days) + 6) // 7
    width = max(start_x + num_weeks * stride + 40, 840)
    height = 230
    
    bg_color = "#0d1117"
    border_color = "#30363d"
    title_bar_bg = "#161b22"
    sub_color = "#8b949e"
    key_color = "#58a6ff"
    val_color = "#c9d1d9"
    accent_green = "#3fb950"
    
    svg_lines = []
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg_lines.append('  <style>')
    svg_lines.append('    @import url("https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600;700&amp;display=swap");')
    svg_lines.append('    .bg { fill: ' + bg_color + '; rx: 10px; ry: 10px; stroke: ' + border_color + '; stroke-width: 1.5; }')
    svg_lines.append('    .title-bar { fill: ' + title_bar_bg + '; rx: 10px; ry: 10px; }')
    svg_lines.append('    .term-title { font-family: "Fira Code", monospace; font-size: 13px; fill: ' + sub_color + '; font-weight: 600; }')
    svg_lines.append('    .lbl { font-family: "Fira Code", monospace; font-size: 10px; fill: ' + sub_color + '; }')
    svg_lines.append('    .stat-title { font-family: "Fira Code", monospace; font-size: 11px; fill: ' + sub_color + '; font-weight: 600; }')
    svg_lines.append('    .stat-val { font-family: "Fira Code", monospace; font-size: 12px; fill: ' + accent_green + '; font-weight: 700; }')
    svg_lines.append('    .stat-sub { font-family: "Fira Code", monospace; font-size: 11px; fill: ' + val_color + '; }')
    svg_lines.append('    ')
    svg_lines.append('    /* Diagonal Reveal Animation */')
    svg_lines.append('    .day-box {')
    svg_lines.append('      rx: 2.5px;')
    svg_lines.append('      ry: 2.5px;')
    svg_lines.append('      opacity: 0;')
    svg_lines.append('      transform-origin: center;')
    svg_lines.append('      animation: diagReveal 0.35s ease-out forwards;')
    svg_lines.append('    }')
    svg_lines.append('    @keyframes diagReveal {')
    svg_lines.append('      0% { opacity: 0; transform: scale(0.2); }')
    svg_lines.append('      70% { opacity: 0.9; transform: scale(1.1); }')
    svg_lines.append('      100% { opacity: 1; transform: scale(1); }')
    svg_lines.append('    }')
    svg_lines.append('  </style>')
    
    # Background & Window Chrome
    svg_lines.append(f'  <rect width="{width}" height="{height}" class="bg" />')
    svg_lines.append(f'  <rect width="{width}" height="38" class="title-bar" />')
    svg_lines.append(f'  <rect width="{width}" height="10" y="28" fill="{title_bar_bg}" />')
    
    # Title bar buttons & label
    svg_lines.append('  <circle cx="20" cy="19" r="6" fill="#ff5f56" />')
    svg_lines.append('  <circle cx="40" cy="19" r="6" fill="#ffbd2e" />')
    svg_lines.append('  <circle cx="60" cy="19" r="6" fill="#27c93f" />')
    svg_lines.append(f'  <text x="{width/2}" y="24" text-anchor="middle" class="term-title">shreena88@github: ~/contributions.sh</text>')

    # Day of week labels (Mon, Wed, Fri)
    day_labels = [("Mon", 1), ("Wed", 3), ("Fri", 5)]
    for lbl, r_idx in day_labels:
        y_pos = start_y + r_idx * stride + 9
        svg_lines.append(f'  <text x="{start_x - 10}" y="{y_pos}" text-anchor="end" class="lbl">{lbl}</text>')

    # Month Labels
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    last_month = None
    
    for i, d in enumerate(days):
        col = i // 7
        row = i % 7
        
        # Check month change
        dt = datetime.strptime(d["date"], "%Y-%m-%d")
        if dt.month != last_month and row == 0:
            m_name = month_names[dt.month - 1]
            m_x = start_x + col * stride
            svg_lines.append(f'  <text x="{m_x}" y="{start_y - 8}" class="lbl">{m_name}</text>')
            last_month = dt.month

        # Render cell square
        x = start_x + col * stride
        y = start_y + row * stride
        level = min(d.get("level", 0), 4)
        color = level_colors[level]
        
        # Calculate diagonal animation delay based on col + row
        delay = (col + row) * 0.015
        
        svg_lines.append(f'  <rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" fill="{color}" class="day-box" style="animation-delay: {delay:.3f}s;">')
        svg_lines.append(f'    <title>{d["count"]} contributions on {d["date"]}</title>')
        svg_lines.append(f'  </rect>')

    # Heatmap Legend (Less -> Level 0..4 -> More)
    legend_x = start_x + num_weeks * stride - 120
    legend_y = start_y + 7 * stride + 15
    svg_lines.append(f'  <text x="{legend_x - 30}" y="{legend_y + 9}" class="lbl">Less</text>')
    for l_idx, l_col in enumerate(level_colors):
        lx = legend_x + l_idx * (cell_size + 3)
        svg_lines.append(f'  <rect x="{lx}" y="{legend_y}" width="{cell_size}" height="{cell_size}" fill="{l_col}" rx="2" ry="2"/>')
    svg_lines.append(f'  <text x="{legend_x + 5 * (cell_size + 3) + 5}" y="{legend_y + 9}" class="lbl">More</text>')

    # Footer Statistics Bar
    footer_y = height - 20
    # Equal distribution across 4 metric blocks
    metrics = [
        ("Total Yearly", f"{total_contribs} contribs"),
        ("Current Streak", f"{current_streak} days"),
        ("Longest Streak", f"{longest_streak} days"),
        ("Best Day", f"{best_day['count']} on {best_day_str}")
    ]
    
    col_width = (width - 60) // 4
    for idx, (m_title, m_val) in enumerate(metrics):
        cx = 30 + idx * col_width
        svg_lines.append(f'  <text x="{cx}" y="{footer_y}" class="stat-sub">')
        svg_lines.append(f'    <tspan class="stat-title">{m_title}: </tspan><tspan class="stat-val">{m_val}</tspan>')
        svg_lines.append(f'  </text>')

    svg_lines.append('</svg>')

    os.makedirs(os.path.dirname(output_svg_path), exist_ok=True)
    with open(output_svg_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
        
    print(f"contrib-heatmap.svg successfully written to {output_svg_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_file = os.path.join(base_dir, "data", "contributions.json")
    output_svg = os.path.join(base_dir, "assets", "contrib-heatmap.svg")
    render_heatmap_svg(json_file, output_svg)
