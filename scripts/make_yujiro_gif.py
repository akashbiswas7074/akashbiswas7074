import numpy as np
from PIL import Image, ImageFilter
import math
import os

src_path = "/home/akashbiswas/.gemini/antigravity-ide/brain/228e0e78-0eb3-4eb5-86d2-487b1a9d1b6e/.user_uploaded/media_1791083742874.png"
raw_img = Image.open(src_path).convert("RGB")

# Zoom in on the Face & Head (y: 335 to 555, x: 225 to 445)
crop_y1, crop_y2 = 335, 555
crop_x1, crop_x2 = 225, 445
char_crop = raw_img.crop((crop_x1, crop_y1, crop_x2, crop_y2))

# Banner dimensions (FB cover ratio: 850 x 315)
BANNER_W = 850
BANNER_H = 315

# Scale face to prominently fill banner height (height = 305)
target_h = 305
aspect = char_crop.width / char_crop.height
target_w = int(target_h * aspect)
char_resized = char_crop.resize((target_w, target_h), Image.Resampling.LANCZOS)

char_arr = np.array(char_resized).astype(np.float32)

NUM_FRAMES = 24
frames = []

# Position centered in banner
pos_x = (BANNER_W - target_w) // 2
pos_y = (BANNER_H - target_h) // 2

# Scale factor for eyes
scale_factor = target_h / (crop_y2 - crop_y1)
# Original eyes at y=448, x=330 and x=349
eye_y = int((448 - crop_y1) * scale_factor)
eye_x1 = int((330 - crop_x1) * scale_factor)
eye_x2 = int((349 - crop_x1) * scale_factor)

# Seed random particles for embers
np.random.seed(42)
num_particles = 35
particles_x = np.random.uniform(pos_x - 80, pos_x + target_w + 80, num_particles)
particles_y = np.random.uniform(0, BANNER_H, num_particles)
particles_speed = np.random.uniform(1.8, 3.8, num_particles)

for f in range(NUM_FRAMES):
    phase = 2 * math.pi * (f / NUM_FRAMES)
    
    # 1. Base canvas: pitch black
    canvas = np.zeros((BANNER_H, BANNER_W, 3), dtype=np.float32)
    
    # 2. Breathing / pulsing multiplier for white lines
    pulse = 1.0 + 0.28 * math.sin(phase)
    red_pulse = 0.5 + 0.5 * math.sin(phase + math.pi/4)
    
    # Process character frame
    char_frame = char_arr.copy()
    brightness = np.mean(char_frame, axis=2, keepdims=True) / 255.0
    
    # Modulate white lines
    char_frame = char_frame * pulse
    
    # Add demonic crimson tinge to lines & edges
    red_glow = np.zeros_like(char_frame)
    red_glow[:, :, 0] = brightness[:, :, 0] * 100 * red_pulse
    char_frame += red_glow
    
    # Soft vertical fade at bottom of cropped neck so there is zero harsh edge
    fade_len = int(35 * scale_factor)
    for row_i in range(target_h - fade_len, target_h):
        alpha_row = (target_h - row_i) / fade_len
        char_frame[row_i, :] *= alpha_row

    # Place on canvas
    canvas[pos_y:pos_y+target_h, pos_x:pos_x+target_w] = np.maximum(
        canvas[pos_y:pos_y+target_h, pos_x:pos_x+target_w],
        char_frame
    )
    
    # 3. Glowing demonic red eye flares
    eye_intensity = 0.8 + 0.35 * math.sin(phase * 2)
    for ex in [pos_x + eye_x1, pos_x + eye_x2]:
        ey = pos_y + eye_y
        for dy in range(-4, 5):
            for dx in range(-7, 8):
                dist = math.sqrt((dx*1.0)**2 + (dy*1.8)**2)
                if dist < 6.0:
                    alpha = math.exp(-dist * 0.7) * eye_intensity
                    canvas[ey+dy, ex+dx, 0] = min(255, canvas[ey+dy, ex+dx, 0] + 255 * alpha)
                    canvas[ey+dy, ex+dx, 1] = min(255, canvas[ey+dy, ex+dx, 1] + 30 * alpha)
                    canvas[ey+dy, ex+dx, 2] = min(255, canvas[ey+dy, ex+dx, 2] + 30 * alpha)

    # 4. Drifting glowing embers in background
    for i in range(num_particles):
        py = (particles_y[i] - f * particles_speed[i]) % BANNER_H
        px = particles_x[i] + 6 * math.sin(phase + i)
        px_i, py_i = int(px), int(py)
        if 0 <= px_i < BANNER_W - 2 and 0 <= py_i < BANNER_H - 2:
            canvas[py_i, px_i] = [255, 100, 30]
            canvas[py_i+1, px_i] = [220, 50, 10]
            canvas[py_i, px_i+1] = [220, 50, 10]

    # Clip & convert to uint8
    canvas = np.clip(canvas, 0, 255).astype(np.uint8)
    frames.append(Image.fromarray(canvas))

# Save as optimized animated GIF
out_path = "/home/akashbiswas/Downloads/akashbiswas7074/assets/yujiro-banner.gif"
preview_path = "/home/akashbiswas/Downloads/blu3-bird/assets/yujiro-banner.gif"

frames[0].save(
    out_path,
    save_all=True,
    append_images=frames[1:],
    duration=65, # ~15 fps
    loop=0,
    optimize=True
)

import shutil
shutil.copyfile(out_path, preview_path)
print(f"Generated {out_path} ({os.path.getsize(out_path)} bytes)")
