import numpy as np
from PIL import Image, ImageFilter
import math
import os

src_path = "/home/akashbiswas/.gemini/antigravity-ide/brain/228e0e78-0eb3-4eb5-86d2-487b1a9d1b6e/.user_uploaded/media_1791085459890.jpg"
img = Image.open(src_path).convert("RGB")

BANNER_W = 850
BANNER_H = 315

# Crop from y=0 (top fixed with ogre eyes) down to y=230 (zoomed face, hair, chest)
crop_y1, crop_y2 = 0, 230
crop_x1, crop_x2 = 0, 399

# 1. Full-width atmospheric background layer (stretched & blurred with no seams)
bg_crop = img.crop((crop_x1, crop_y1, crop_x2, crop_y2))
bg_resized = bg_crop.resize((BANNER_W, BANNER_H), Image.Resampling.LANCZOS)
bg_blurred = bg_resized.filter(ImageFilter.GaussianBlur(radius=8))
bg_arr_base = np.array(bg_blurred).astype(np.float32)

# 2. Foreground sharp character (centered, zoomed)
target_h = BANNER_H
scale = target_h / float(crop_y2 - crop_y1) # ~1.37
target_w = int((crop_x2 - crop_x1) * scale) # ~546 px

char_resized = bg_crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
char_arr_base = np.array(char_resized).astype(np.float32)

pos_x = (BANNER_W - target_w) // 2 # 152 px

# Eye positions in banner coordinates
ogre_eye_y = int(18 * scale) # ~25
ogre_eye_x1 = pos_x + int(142 * scale) # ~346
ogre_eye_x2 = pos_x + int(257 * scale) # ~504

yujiro_eye_y = int(121 * scale) # ~165
yujiro_eye_x1 = pos_x + int(191 * scale) # ~413
yujiro_eye_x2 = pos_x + int(205 * scale) # ~432

# 3. Soft cosine alpha mask for foreground character (feathered outer 65px)
feather_w = 65
char_mask = np.ones((target_h, target_w), dtype=np.float32)
for i in range(feather_w):
    alpha = 0.5 - 0.5 * np.cos(np.pi * (i / float(feather_w)))
    char_mask[:, i] = alpha
    char_mask[:, target_w - 1 - i] = alpha

# 4. Construct perfectly seamless base canvas
canvas_base = bg_arr_base.copy()
for c in range(3):
    canvas_base[:, pos_x:pos_x+target_w, c] = (
        char_arr_base[:, :, c] * char_mask + canvas_base[:, pos_x:pos_x+target_w, c] * (1.0 - char_mask)
    )

bg_col = np.array([13, 17, 23], dtype=np.float32) # #0D1117

# Flame weight across entire canvas
r = canvas_base[:, :, 0]
g = canvas_base[:, :, 1]
b = canvas_base[:, :, 2]
flame_weight = np.clip((r - np.maximum(g, b)) / 130.0, 0, 1.0)[:, :, np.newaxis]

NUM_FRAMES = 18
frames = []

np.random.seed(42)
num_particles = 55
particles_x = np.random.uniform(15, BANNER_W - 15, num_particles)
particles_y = np.random.uniform(0, BANNER_H, num_particles)
particles_speed = np.random.uniform(2.5, 5.0, num_particles)
particles_drift = np.random.uniform(4.0, 8.0, num_particles)

for f in range(NUM_FRAMES):
    phase = 2.0 * math.pi * (f / NUM_FRAMES)
    
    # 1. Flowing heat-wave displacement on flames
    y_coords, x_coords = np.indices((BANNER_H, BANNER_W))
    dx = (2.2 * np.sin(phase + y_coords * 0.08) * flame_weight[:, :, 0]).astype(int)
    dy = (-2.0 * np.cos(phase + y_coords * 0.06) * flame_weight[:, :, 0]).astype(int)
    
    src_y = np.clip(y_coords + dy, 0, BANNER_H - 1)
    src_x = np.clip(x_coords + dx, 0, BANNER_W - 1)
    wave_canvas = canvas_base[src_y, src_x].copy()
    
    # 2. Fire aura pulsation
    flame_pulse = 1.0 + 0.22 * math.sin(phase)
    flame_boost = np.zeros_like(wave_canvas)
    flame_boost[:, :, 0] = flame_weight[:, :, 0] * (45 * math.sin(phase) + 20)
    flame_boost[:, :, 1] = flame_weight[:, :, 0] * (15 * math.sin(phase))
    wave_canvas = np.clip(wave_canvas * (1.0 + (flame_pulse - 1.0) * flame_weight) + flame_boost, 0, 255)
    
    # 3. Smooth Black Dissolve Overlay on left and right sides (zero seams, smooth dissolve)
    for x in range(BANNER_W):
        if x < 260:
            t = (260.0 - x) / 260.0
            alpha = (t * t * (3.0 - 2.0 * t)) * 0.75 # smooth 75% dark dissolve
            wave_canvas[:, x] = wave_canvas[:, x] * (1.0 - alpha) + bg_col * alpha
        elif x > 590:
            t = (x - 590.0) / (BANNER_W - 590.0)
            alpha = (t * t * (3.0 - 2.0 * t)) * 0.75
            wave_canvas[:, x] = wave_canvas[:, x] * (1.0 - alpha) + bg_col * alpha

    # 4. Blue Ogre eye glow in top background
    blue_eye_pulse = 0.75 + 0.35 * math.sin(phase + math.pi/3)
    for ox in [ogre_eye_x1, ogre_eye_x2]:
        for dy_i in range(-4, 5):
            for dx_i in range(-7, 8):
                dist = math.sqrt((dx_i*1.0)**2 + (dy_i*1.5)**2)
                if dist < 5.5:
                    alpha_e = math.exp(-dist * 0.6) * blue_eye_pulse
                    wave_canvas[ogre_eye_y+dy_i, ox+dx_i, 0] = min(255, wave_canvas[ogre_eye_y+dy_i, ox+dx_i, 0] + 50 * alpha_e)
                    wave_canvas[ogre_eye_y+dy_i, ox+dx_i, 1] = min(255, wave_canvas[ogre_eye_y+dy_i, ox+dx_i, 1] + 160 * alpha_e)
                    wave_canvas[ogre_eye_y+dy_i, ox+dx_i, 2] = min(255, wave_canvas[ogre_eye_y+dy_i, ox+dx_i, 2] + 255 * alpha_e)

    # 5. Yujiro demonic red eye flares
    yujiro_eye_pulse = 0.85 + 0.45 * math.sin(phase * 2.0)
    for yx in [yujiro_eye_x1, yujiro_eye_x2]:
        for dy_i in range(-4, 5):
            for dx_i in range(-5, 6):
                dist = math.sqrt((dx_i*1.0)**2 + (dy_i*1.5)**2)
                if dist < 4.8:
                    alpha_e = math.exp(-dist * 0.7) * yujiro_eye_pulse
                    wave_canvas[yujiro_eye_y+dy_i, yx+dx_i, 0] = min(255, wave_canvas[yujiro_eye_y+dy_i, yx+dx_i, 0] + 255 * alpha_e)
                    wave_canvas[yujiro_eye_y+dy_i, yx+dx_i, 1] = min(255, wave_canvas[yujiro_eye_y+dy_i, yx+dx_i, 1] + 80 * alpha_e)
                    wave_canvas[yujiro_eye_y+dy_i, yx+dx_i, 2] = min(255, wave_canvas[yujiro_eye_y+dy_i, yx+dx_i, 2] + 80 * alpha_e)

    # 6. Drifting fiery embers across full banner & dissolved shadow zones
    for i in range(num_particles):
        py = (particles_y[i] - f * particles_speed[i]) % BANNER_H
        px = particles_x[i] + particles_drift[i] * math.sin(phase + i)
        px_i, py_i = int(px), int(py)
        if 0 <= px_i < BANNER_W - 2 and 0 <= py_i < BANNER_H - 2:
            wave_canvas[py_i, px_i] = [255, 120, 40]
            wave_canvas[py_i+1, px_i] = [220, 60, 20]
            wave_canvas[py_i, px_i+1] = [220, 60, 20]

    wave_canvas = np.clip(wave_canvas, 0, 255).astype(np.uint8)
    frame_pil = Image.fromarray(wave_canvas).quantize(colors=128, method=Image.Resampling.LANCZOS)
    frames.append(frame_pil)

out_path = "/home/akashbiswas/Downloads/akashbiswas7074/assets/yujiro-banner.gif"
preview_path = "/home/akashbiswas/Downloads/blu3-bird/assets/yujiro-banner.gif"

frames[0].save(
    out_path,
    save_all=True,
    append_images=frames[1:],
    duration=80, # ~12.5 fps smooth loop
    loop=0,
    optimize=True
)

import shutil
shutil.copyfile(out_path, preview_path)
print(f"Generated flawless seamless banner {out_path} ({os.path.getsize(out_path)} bytes) with {len(frames)} frames!")
