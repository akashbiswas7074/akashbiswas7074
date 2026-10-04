import base64

FACE_PATH = "/home/akashbiswas/Downloads/akashbiswas7074/assets/yujiro-face.png"
CARD_PATH_1 = "/home/akashbiswas/Downloads/akashbiswas7074/assets/hanma-card.svg"
CARD_PATH_2 = "/home/akashbiswas/Downloads/blu3-bird/assets/hanma-card.svg"

with open(FACE_PATH, "rb") as f:
    b64 = base64.b64encode(f.read()).decode("utf-8")

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="280" viewBox="0 0 800 280" font-family="ui-monospace, 'SF Mono', 'Cascadia Mono', Menlo, monospace">
  <defs>
    <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FF2A55"/>
      <stop offset="50%" stop-color="#5277C3"/>
      <stop offset="100%" stop-color="#4AF626"/>
    </linearGradient>
    <radialGradient id="auraGlow" cx="15%" cy="50%" r="40%">
      <stop offset="0%" stop-color="#FF2A55" stop-opacity="0.32"/>
      <stop offset="100%" stop-color="#0D1117" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="tbar"><rect x="1.5" y="1.5" width="797" height="36" rx="8.5"/></clipPath>
    <clipPath id="avatarClip"><circle cx="110" cy="148" r="68"/></clipPath>
  </defs>

  <!-- Background Card with Glow Border -->
  <rect x="1.5" y="1.5" width="797" height="277" rx="10" fill="#0D1117" stroke="url(#borderGrad)" stroke-width="1.5"/>
  <rect x="1.5" y="1.5" width="797" height="277" rx="10" fill="url(#auraGlow)"/>

  <!-- Terminal Top Bar -->
  <rect x="1.5" y="1.5" width="797" height="36" fill="#161B22" clip-path="url(#tbar)"/>
  <line x1="1.5" y1="37.5" x2="798.5" y2="37.5" stroke="#30363D" stroke-width="1"/>
  <circle cx="24" cy="19" r="5.5" fill="#FF5F56"/>
  <circle cx="43" cy="19" r="5.5" fill="#FFBD2E"/>
  <circle cx="62" cy="19" r="5.5" fill="#27C93F"/>
  <text x="400" y="23" text-anchor="middle" font-size="12" fill="#8B949E">akash@nixos: ~/hanma-creed</text>

  <!-- Left Side: Yujiro Hanma Actual Face Avatar with Glowing Demonic Frame -->
  <g>
    <!-- Outer Glowing Aura Ring -->
    <circle cx="110" cy="148" r="74" fill="none" stroke="#FF2A55" stroke-width="2.5" opacity="0.8">
      <animate attributeName="stroke-width" values="2;4;2" dur="2s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.6;1;0.6" dur="2s" repeatCount="indefinite"/>
    </circle>
    <circle cx="110" cy="148" r="70" fill="none" stroke="#800F2F" stroke-width="1"/>

    <!-- Actual Cropped Face Image of Yujiro -->
    <image href="data:image/png;base64,{b64}" x="42" y="80" width="136" height="136" clip-path="url(#avatarClip)" preserveAspectRatio="xMidYMid slice"/>
    
    <!-- Title under avatar -->
    <text x="110" y="238" text-anchor="middle" font-size="11" font-weight="800" fill="#FF4D6D" letter-spacing="2">YUJIRO HANMA</text>
    <text x="110" y="254" text-anchor="middle" font-size="9.5" font-weight="700" fill="#8B949E" letter-spacing="2">THE OGRE</text>
  </g>

  <!-- Right Side: The Hanma Developer Creed & Quote (Cleanly Formatted, No Cropping) -->
  <g transform="translate(215, 52)">
    <text x="0" y="18" font-size="12" font-weight="700" fill="#FF2A55" letter-spacing="1.5">⚡ THE STRONGEST ENGINEER // HANMA DOCTRINE</text>
    
    <text x="0" y="46" font-size="14.5" font-weight="700" fill="#E6EDF3">"True strength isn't given — it is forged</text>
    <text x="0" y="68" font-size="14.5" font-weight="700" fill="#E6EDF3"> through relentless practice &amp; deep mastery."</text>
    
    <text x="0" y="96" font-size="12.5" fill="#8B949E">Training deep neural nets &amp; AI models, architecting 3D worlds,</text>
    <text x="0" y="116" font-size="12.5" fill="#8B949E">and shipping high-speed MERN &amp; mobile apps — conquer every bug.</text>
    
    <text x="0" y="144" font-size="12" fill="#5277C3" font-weight="700">― Yujiro Hanma × Akash Biswas</text>

    <!-- Status Bar -->
    <rect x="0" y="160" width="555" height="38" rx="6" fill="#161B22" stroke="#30363D" stroke-width="1"/>
    <circle cx="18" cy="179" r="4.5" fill="#4AF626">
      <animate attributeName="opacity" values="1;0.35;1" dur="1.3s" repeatCount="indefinite"/>
    </circle>
    <text x="32" y="183" font-size="11.5" fill="#E6EDF3" font-weight="700">STATUS: <tspan fill="#4AF626">READY TO TRAIN MODELS &amp; SHIP CODE</tspan> <tspan fill="#8B949E">| AI/ML · MERN · 3D</tspan></text>
  </g>
</svg>"""

with open(CARD_PATH_1, "w") as f:
    f.write(svg)
with open(CARD_PATH_2, "w") as f:
    f.write(svg)

print(f"Generated {CARD_PATH_1} and {CARD_PATH_2} successfully ({len(svg)} bytes)!")
