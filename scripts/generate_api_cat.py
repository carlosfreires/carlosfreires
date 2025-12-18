"""
✨ SPACE CATS ✨

Gera dois SVGs animados (TheCatAPI + CATAAS)
"""

import os
import random
import base64
import requests
from datetime import datetime, timezone

# ===============================
# CONFIGURAÇÕES GERAIS
# ===============================

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

CAT_API_URL = "https://api.thecatapi.com/v1/images/search?limit=1"
CATAAS_URLS = [
    "https://cataas.com/cat",
    "https://cataas.com/cat/cute",
    "https://cataas.com/cat/funny"
]
CAT_FACT_URL = "https://catfact.ninja/fact"

TIMEOUT = 10


# ===============================
# FUNÇÕES DE APOIO
# ===============================

def fetch_image_as_base64(url: str) -> str:
    """
    Baixa uma imagem e converte para base64
    para embutir diretamente no SVG.
    """
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        encoded = base64.b64encode(response.content).decode("utf-8")
        return f"data:image/jpeg;base64,{encoded}"
    except Exception:
        return ""


def get_cat_fact() -> str:
    """
    Obtém um fato sobre gatos.
    """
    try:
        response = requests.get(CAT_FACT_URL, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json().get("fact", "Cats are fascinating creatures.")
    except Exception:
        return "Cats are mysterious creatures of elegance and power."


def get_thecatapi_image() -> str:
    """
    Obtém imagem via TheCatAPI.
    """
    try:
        response = requests.get(CAT_API_URL, timeout=TIMEOUT)
        response.raise_for_status()
        image_url = response.json()[0]["url"]
        return fetch_image_as_base64(image_url)
    except Exception:
        return ""


def get_cataas_image() -> str:
    """
    Obtém imagem via CATAAS, com cache-busting.
    """
    ts = int(datetime.now(timezone.utc).timestamp())
    url = random.choice(CATAAS_URLS) + f"?_={ts}"
    return fetch_image_as_base64(url)


# ===============================
# GERADOR DO SVG
# ===============================

def build_svg(image_b64: str, fact: str, gradient_id: str, orbit_color: str) -> str:
    """
    Constrói o SVG completo com:
    - Gradiente neon animado
    - Partículas reativas
    - Estrelas procedurais
    - Órbita suave
    - Glow pulsante
    - Texto com aura luminosa
    """

    # Estrelas procedurais (simples e leves)
    stars = "".join(
        f'''
        <circle cx="{x}" cy="{y}" r="1.2" fill="#ffffff" opacity="0.35">
          <animate attributeName="opacity"
                   values="0.15;0.85;0.15"
                   dur="{d}s"
                   repeatCount="indefinite"/>
        </circle>
        '''
        for x, y, d in [
            (100, 90, 9), (280, 60, 12), (520, 120, 10),
            (860, 80, 14), (1080, 140, 11), (760, 420, 8)
        ]
    )

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="1200" height="520"
     viewBox="0 0 1200 520">

<defs>

<!-- 🌈 GRADIENTE NEON VIVO -->
<linearGradient id="{gradient_id}" x1="0%" y1="0%" x2="100%" y2="0%">
  <stop offset="0%" stop-color="#6A00FF">
    <animate attributeName="stop-color"
             values="#6A00FF;#8B5CFF;#FF2FB3;#6A00FF"
             dur="18s" repeatCount="indefinite"/>
  </stop>

  <stop offset="35%" stop-color="#FF2FB3">
    <animate attributeName="stop-color"
             values="#FF2FB3;#FF5FD2;#8B5CFF;#FF2FB3"
             dur="22s" repeatCount="indefinite"/>
    <animate attributeName="offset"
             values="30%;45%;30%"
             dur="20s" repeatCount="indefinite"/>
  </stop>

  <stop offset="70%" stop-color="#8B5CFF">
    <animate attributeName="stop-color"
             values="#8B5CFF;#6A00FF;#FF5FD2;#8B5CFF"
             dur="26s" repeatCount="indefinite"/>
    <animate attributeName="offset"
             values="65%;80%;65%"
             dur="24s" repeatCount="indefinite"/>
  </stop>

  <stop offset="100%" stop-color="#FF5FD2">
    <animate attributeName="stop-color"
             values="#FF5FD2;#FF2FB3;#6A00FF;#FF5FD2"
             dur="30s" repeatCount="indefinite"/>
  </stop>

  <animateTransform attributeName="gradientTransform"
                    type="rotate"
                    from="0 600 260"
                    to="360 600 260"
                    dur="60s"
                    repeatCount="indefinite"/>
</linearGradient>

<!-- ✨ GLOW PADRÃO -->
<filter id="glow">
  <feGaussianBlur stdDeviation="3.5" result="b"/>
  <feMerge>
    <feMergeNode in="b"/>
    <feMergeNode in="SourceGraphic"/>
  </feMerge>
</filter>

<!-- 💡 GLOW DO TEXTO -->
<filter id="textGlow">
  <feGaussianBlur stdDeviation="2.5" result="blur"/>
  <feColorMatrix type="matrix"
    values="
      1 0 0 0 0
      0 0.4 1 0 0
      1 0 1 0 0
      0 0 0 1 0"/>
  <feMerge>
    <feMergeNode in="blur"/>
    <feMergeNode in="SourceGraphic"/>
  </feMerge>
  <animate attributeName="stdDeviation"
           values="1.8;3.2;1.8"
           dur="4.8s"
           repeatCount="indefinite"/>
</filter>

<!-- ✨ GLOW DAS PARTÍCULAS -->
<filter id="particleGlow">
  <feGaussianBlur stdDeviation="2"/>
  <feMerge>
    <feMergeNode/>
    <feMergeNode in="SourceGraphic"/>
  </feMerge>
</filter>

<!-- CLIP DA IMAGEM -->
<clipPath id="clip">
  <circle cx="260" cy="260" r="200"/>
</clipPath>

</defs>

<!-- FUNDO -->
<rect width="1200" height="520" fill="url(#{gradient_id})"/>

<!-- PARTÍCULAS REATIVAS -->
<g filter="url(#particleGlow)" opacity="0.85">
  <circle cx="180" cy="160" r="2.2" fill="url(#{gradient_id})">
    <animate attributeName="opacity" values="0.25;0.9;0.25" dur="6s" repeatCount="indefinite"/>
    <animateTransform attributeName="transform" type="rotate"
                      from="0 600 260" to="360 600 260"
                      dur="48s" repeatCount="indefinite"/>
    <animate attributeName="r" values="1.6;2.8;1.6" dur="5s" repeatCount="indefinite"/>
  </circle>

  <circle cx="980" cy="120" r="1.8" fill="url(#{gradient_id})">
    <animate attributeName="opacity" values="0.2;0.75;0.2" dur="7.5s" repeatCount="indefinite"/>
    <animateTransform attributeName="transform" type="rotate"
                      from="360 600 260" to="0 600 260"
                      dur="64s" repeatCount="indefinite"/>
    <animate attributeName="r" values="1.2;2.4;1.2" dur="6.5s" repeatCount="indefinite"/>
  </circle>
</g>

<!-- ESTRELAS -->
<g>{stars}</g>

<!-- ÓRBITA -->
<circle cx="260" cy="260" r="215"
        fill="none"
        stroke="{orbit_color}"
        stroke-width="1.2"
        opacity="0.65"
        filter="url(#glow)">
  <animateTransform attributeName="transform"
                    type="rotate"
                    from="0 260 260"
                    to="360 260 260"
                    dur="34s"
                    repeatCount="indefinite"/>
</circle>

<!-- IMAGEM -->
<image x="60" y="60" width="400" height="400"
       href="{image_b64}"
       clip-path="url(#clip)"
       preserveAspectRatio="xMidYMid slice"
       filter="url(#glow)"/>

<!-- FACT COM AURA -->
<foreignObject x="520" y="150" width="620" height="220">
  <div xmlns="http://www.w3.org/1999/xhtml"
       style="
         font-family:Arial;
         font-size:22px;
         line-height:1.6;
         color:#ffffff;
         background:rgba(10,0,20,.45);
         padding:26px;
         border-radius:20px;
         filter:url(#textGlow);
         text-shadow:
           0 0 8px rgba(255,100,255,.6),
           0 0 18px rgba(160,80,255,.4);
       ">
    🐾 {fact}
  </div>
</foreignObject>

<!-- FOOTER -->
<text x="600" y="500"
      text-anchor="middle"
      font-size="12"
      fill="#ffffff"
      opacity="0.55">
  Generated • {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}
</text>

</svg>
"""


# ===============================
# MAIN
# ===============================

def main():
    print("📡 Fetching cat data...")

    fact = get_cat_fact()

    svg_api = build_svg(
        get_thecatapi_image(),
        fact,
        gradient_id="neonGradA",
        orbit_color="#FF8BFF"
    )

    svg_cataas = build_svg(
        get_cataas_image(),
        fact,
        gradient_id="neonGradB",
        orbit_color="#C77DFF"
    )

    with open(f"{OUTPUT_DIR}/space_cat_api.svg", "w", encoding="utf-8") as f:
        f.write(svg_api)

    with open(f"{OUTPUT_DIR}/space_cat_cataas.svg", "w", encoding="utf-8") as f:
        f.write(svg_cataas)

    with open(f"{OUTPUT_DIR}/cats_section.md", "w", encoding="utf-8") as f:
        f.write("![Cat](./space_cat_api.svg)\n\n![Cat](./space_cat_cataas.svg)")

    print("✨ SVGs gerados com sucesso. Versão FINAL em produção.")


if __name__ == "__main__":
    main()
