import os

def generate_ascii_svg(txt_path, output_svg_path):
    print(f"Reading ASCII art from {txt_path}...")
    with open(txt_path, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\r\n") for line in f.readlines()]
        
    num_rows = len(lines)
    max_cols = max(len(line) for line in lines) if lines else 100
    
    char_w = 5.3
    line_h = 9.8
    x_offset = 20
    y_start = 65
    
    content_w = int(max_cols * char_w + x_offset * 2)
    content_h = int(num_rows * line_h + y_start + 40)
    
    width = max(content_w, 560)
    height = max(content_h, 640)
    
    bg_color = "#0d1117"
    border_color = "#30363d"
    title_bar_bg = "#161b22"
    sub_color = "#8b949e"
    text_color = "#c9d1d9"  # Monochrome ASCII brightness
    cursor_color = "#3fb950" # GitHub green cursor
    
    total_dur = 4.0 # 4 seconds total typing animation
    row_dur = total_dur / float(num_rows)
    
    svg_out = []
    svg_out.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg_out.append('  <style>')
    svg_out.append('    @import url("https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&amp;display=swap");')
    svg_out.append('    .bg { fill: ' + bg_color + '; rx: 10px; ry: 10px; stroke: ' + border_color + '; stroke-width: 1.5; }')
    svg_out.append('    .title-bar { fill: ' + title_bar_bg + '; rx: 10px; ry: 10px; }')
    svg_out.append('    .term-title { font-family: "Fira Code", monospace; font-size: 13px; fill: ' + sub_color + '; font-weight: 600; }')
    svg_out.append('    .ascii-text { font-family: "Fira Code", "Consolas", "Courier New", monospace; font-size: 8.5px; fill: ' + text_color + '; xml:space: preserve; }')
    svg_out.append('  </style>')
    
    # Clip paths definitions for each row reveal
    svg_out.append('  <defs>')
    for i in range(num_rows):
        y_pos = y_start + i * line_h
        t_start = i * row_dur
        svg_out.append(f'    <clipPath id="clip-row-{i}">')
        svg_out.append(f'      <rect x="{x_offset}" y="{y_pos - line_h + 2}" width="0" height="{line_h + 2}">')
        svg_out.append(f'        <animate attributeName="width" from="0" to="{max_cols * char_w + 10}" begin="{t_start:.3f}s" dur="{row_dur:.3f}s" fill="freeze" repeatCount="1"/>')
        svg_out.append(f'      </rect>')
        svg_out.append(f'    </clipPath>')
    svg_out.append('  </defs>')
    
    # Window Frame & Title Bar
    svg_out.append(f'  <rect width="{width}" height="{height}" class="bg" />')
    svg_out.append(f'  <rect width="{width}" height="38" class="title-bar" />')
    svg_out.append(f'  <rect width="{width}" height="10" y="28" fill="{title_bar_bg}" />')
    
    # Title bar buttons & label
    svg_out.append('  <circle cx="20" cy="19" r="6" fill="#ff5f56" />')
    svg_out.append('  <circle cx="40" cy="19" r="6" fill="#ffbd2e" />')
    svg_out.append('  <circle cx="60" cy="19" r="6" fill="#27c93f" />')
    svg_out.append(f'  <text x="{width/2}" y="24" text-anchor="middle" class="term-title">shreena88@github: ~/ascii-portrait</text>')
    
    # Render ASCII rows
    for i, line in enumerate(lines):
        y_pos = y_start + i * line_h
        # Escape XML entities
        safe_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&#160;")
        svg_out.append(f'  <text x="{x_offset}" y="{y_pos}" class="ascii-text" clip-path="url(#clip-row-{i})">{safe_line}</text>')
        
    # Animated Cursor
    # Generate keyTimes and x/y values for cursor animation
    cursor_x_vals = []
    cursor_y_vals = []
    key_times = []
    
    num_pts = num_rows * 2 + 1
    for i in range(num_rows):
        y_top = y_start + i * line_h - 7
        t1 = (i * row_dur) / total_dur
        t2 = ((i + 1) * row_dur) / total_dur
        
        if i == 0:
            key_times.append(f"{t1:.4f}")
            cursor_x_vals.append(f"{x_offset}")
            cursor_y_vals.append(f"{y_top:.1f}")
            
        key_times.append(f"{t2:.4f}")
        cursor_x_vals.append(f"{x_offset + max_cols * char_w:.1f}")
        cursor_y_vals.append(f"{y_top:.1f}")
        
        if i < num_rows - 1:
            next_y_top = y_start + (i + 1) * line_h - 7
            # Instant step to start of next line at t2
            key_times.append(f"{t2:.4f}")
            cursor_x_vals.append(f"{x_offset}")
            cursor_y_vals.append(f"{next_y_top:.1f}")

    # Fix keytimes normalization
    # Construct cursor element
    final_y = y_start + num_rows * line_h - 7
    svg_out.append(f'  <rect x="{x_offset}" y="{final_y}" width="6" height="9" fill="{cursor_color}">')
    svg_out.append(f'    <animate attributeName="x" values="{";".join(cursor_x_vals)}" keyTimes="{";".join(key_times)}" dur="{total_dur}s" fill="freeze" repeatCount="1"/>')
    svg_out.append(f'    <animate attributeName="y" values="{";".join(cursor_y_vals)}" keyTimes="{";".join(key_times)}" dur="{total_dur}s" fill="freeze" repeatCount="1"/>')
    svg_out.append(f'    <animate attributeName="opacity" values="1;0;1" dur="0.8s" repeatCount="indefinite" begin="0s"/>')
    svg_out.append('  </rect>')
    
    svg_out.append('</svg>')
    
    os.makedirs(os.path.dirname(output_svg_path), exist_ok=True)
    with open(output_svg_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_out))
        
    print(f"avi-ascii.svg successfully created at {output_svg_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    txt_file = os.path.join(base_dir, "data", "ascii_art.txt")
    output_svg = os.path.join(base_dir, "assets", "avi-ascii.svg")
    generate_ascii_svg(txt_file, output_svg)
