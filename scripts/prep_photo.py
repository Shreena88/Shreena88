import os
import cv2
import numpy as np
from PIL import Image
from rembg import remove

# Density ramp specified in user prompt
DENSITY_RAMP = " .`:-=+*cs#%@"

def process_photo(input_path, output_txt_path, target_width=100, target_height=55):
    print(f"Loading image from {input_path}...")
    img_pil = Image.open(input_path).convert("RGBA")
    
    # 1. Background removal using rembg
    print("Removing background with rembg...")
    nobg_pil = remove(img_pil)
    
    # Create white/transparent combined image on black background for crisp dark mode ASCII
    # Or composite onto black background so transparent areas map to space ' '
    bg = Image.new("RGBA", nobg_pil.size, (0, 0, 0, 255))
    composite = Image.alpha_composite(bg, nobg_pil).convert("L")
    
    # Convert PIL Image to OpenCV numpy array
    img_np = np.array(composite)
    
    # 2. Apply CLAHE contrast enhancement with OpenCV
    print("Applying CLAHE contrast enhancement...")
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced_np = clahe.apply(img_np)
    
    # 3. Resize to target width and height (~100x55)
    print(f"Resizing image to {target_width}x{target_height}...")
    resized_np = cv2.resize(enhanced_np, (target_width, target_height), interpolation=cv2.INTER_AREA)
    
    # 4. Map pixel brightness using density ramp
    # Pixel values 0-255 map to indices 0..(len(DENSITY_RAMP)-1)
    ramp_len = len(DENSITY_RAMP)
    ascii_lines = []
    
    for row in resized_np:
        line_chars = []
        for val in row:
            idx = int((val / 255.0) * (ramp_len - 1))
            line_chars.append(DENSITY_RAMP[idx])
        ascii_lines.append("".join(line_chars))
    
    ascii_art = "\n".join(ascii_lines)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_txt_path), exist_ok=True)
    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write(ascii_art)
        
    print(f"ASCII art saved to {output_txt_path} ({target_width}x{target_height})")
    return ascii_art

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_image = os.path.join(base_dir, "assets", "profile.jpg")
    output_txt = os.path.join(base_dir, "data", "ascii_art.txt")
    process_photo(input_image, output_txt, target_width=100, target_height=55)
