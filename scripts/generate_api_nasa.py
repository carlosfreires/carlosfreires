"""
NASA API

Gera um SVG animado
"""
import requests
import os
import base64
from datetime import datetime, timezone, timedelta



NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")


def validate_api_response(response, api_name):
    """
    Valida resposta de API
    Args:
        response: Objeto Response do requests
        api_name (str): Nome da API para logs
    Retorna: bool - True se resposta válida
    """
    if response.status_code != 200:
        print(f"⚠️  {api_name}: Status code {response.status_code}")
        return False
    
    try:
        response.json()
        return True
    except:
        print(f"⚠️  {api_name}: Resposta JSON inválida")
        return False
    

def safe_get(url, params=None, timeout=15, api_name="API"):
    """Requisição HTTP segura"""
    try:
        response = requests.get(url, params=params, timeout=timeout)
        if validate_api_response(response, api_name):
            return response.json()
    except Exception as e:
        print(f"❌ {api_name}: {e}")
    return None


def get_nasa_apod():
    """Astronomy Picture of the Day"""
    url = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": NASA_API_KEY, "thumbs": "True"}
    data = safe_get(url, params, api_name="NASA APOD")
    
    if data and data.get("media_type") != "image":
        print(f"⚠️  APOD é vídeo: {data.get('media_type')}")
        return None
    
    return data


def image_to_base64(url):
    """Converte imagem para Base64 com tratamento robusto"""
    if not url:
        return None
    
    # URLs alternativas para fallback
    fallback_urls = [
        "https://images.unsplash.com/photo-1446776653964-20c1d3a81b06?w=800&h=400&fit=crop",  # Espaço
        "https://images.unsplash.com/photo-1502134249126-9f3755a50d78?w=800&h=400&fit=crop",  # Estrelas
        "https://images.unsplash.com/photo-1465101162946-4377e57745c3?w=800&h=400&fit=crop",  # Galáxia
    ]
    
    # Tenta a URL principal
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            content_type = response.headers.get('content-type', 'image/jpeg')
            encoded = base64.b64encode(response.content).decode('utf-8')
            return f"data:{content_type};base64,{encoded}"
    except:
        pass
    
    # Tenta URLs de fallback
    for fallback_url in fallback_urls:
        try:
            response = requests.get(fallback_url, timeout=10)
            if response.status_code == 200:
                content_type = response.headers.get('content-type', 'image/jpeg')
                encoded = base64.b64encode(response.content).decode('utf-8')
                return f"data:{content_type};base64,{encoded}"
        except:
            continue
    
    # Se tudo falhar, retorna imagem base64 mínima
    return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="


def get_fallback_image():
    """Imagem de fallback em Base64"""
    return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="

def escape_svg(text, max_length=None):
    """Escapa caracteres especiais para uso dentro de SVG/HTML.
    - max_length: se None -> não trunca; se int -> trunca e adiciona '...' somente quando necessário.
    - preserva quebras de linha transformando em <br/> para o foreignObject.
    """
    if not text:
        return ""
    replacements = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&apos;'
    }
    # Escapa
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    # Preservar quebras de linha
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    # Não inserir <br/> se o caller preferir usar white-space: pre-wrap. 
    # Ainda assim transformamos novas linhas em <br/> para compatibilidade máxima.
    text = text.replace('\n', '<br/>')
    # Truncamento opcional
    if isinstance(max_length, int) and max_length > 0 and len(text) > max_length:
        return text[:max_length] + "..."
    return text

def generate_apod_svg(apod_data):
    """Gera SVG para APOD """
    default_apod = {
        'title': 'First Horizon-Scale Image of a Black Hole',
        'explanation': "What does a black hole look like? To find out, radio telescopes from around the Earth coordinated observations of black holes with the largest known event horizons on the sky. Alone, black holes are just black, but these monster attractors are known to be surrounded by glowing gas. The first image was released yesterday and resolved the area around the black hole at the center of galaxy M87 on a scale below that expected for its event horizon. Pictured, the dark central region is not the event horizon, but rather the black hole's shadow -- the central region of emitting gas darkened by the central black hole's gravity. The size and shape of the shadow is determined by bright gas near the event horizon, by strong gravitational lensing deflections, and by the black hole's spin. In resolving this black hole's shadow, the Event Horizon Telescope (EHT) bolstered evidence that Einstein's gravity works even in extreme regions, and gave clear evidence that M87 has a central spinning black hole of about 6 billion solar masses. The EHT is not done -- future observations will be geared toward even higher resolution, better tracking of variability, and exploring the immediate vicinity of the black hole in the center of our Milky Way Galaxy.",
        'date': datetime.now(timezone.utc).strftime('%Y-%m-%d'),
        'url': 'https://apod.nasa.gov/apod/image/1904/M87bh_EHT_2629.jpg',
        'media_type': 'image',
        'copyright': 'NASA Astronomy Picture of the Day'
    }

    apod = apod_data or default_apod
    img_base64 = image_to_base64(apod['url']) or get_fallback_image()

    title = escape_svg(apod['title'])
    explanation = escape_svg(apod['explanation'])
    date_str = apod.get('date', datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC'))

    # ----- GEOMETRIA MESTRE -----
    img_x = 30.0
    img_y = 180.0
    img_w = 480.0
    img_h = 500.0
    rx = 28.0

    # bordas / strokes (usamos offsets centrados para manter alinhamento visual)
    border_stroke = 3.0        # borda externa gradiente com glow
    inner_stroke = 1.5         # borda interna sutil
    brillo_padding = 10.0      # brilho extra (pode ficar um pouco maior que a imagem)

    # calculos para compensar stroke centrado (stroke desenha metade para dentro/fora)
    border_x = img_x - (border_stroke / 2.0)
    border_y = img_y - (border_stroke / 2.0)
    border_w = img_w + border_stroke
    border_h = img_h + border_stroke

    inner_x = img_x  # inner stroke desenhado exatamente no retângulo mestre
    inner_y = img_y
    inner_w = img_w
    inner_h = img_h

    # brilho externo (um retângulo maior para efeito de brilho)
    brillo_x = img_x - brillo_padding
    brillo_y = img_y - brillo_padding
    brillo_w = img_w + (brillo_padding * 2)
    brillo_h = img_h + (brillo_padding * 2)

    # máscara/clipPath — usa exatamente o retângulo mestre para recortar a imagem
    mask_rect_x = img_x
    mask_rect_y = img_y
    mask_rect_w = img_w
    mask_rect_h = img_h

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     width="1500" height="900" viewBox="0 0 1500 900">
  <defs>
    <!-- (mantive seus gradientes/filters originais) -->
    <linearGradient id="hyper" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%"><animate attributeName="stop-color" values="#00F5FF;#8A2BE2;#FF00FF;#FF6347;#00F5FF" dur="6s" repeatCount="indefinite"/></stop>
      <stop offset="50%"><animate attributeName="stop-color" values="#FF00FF;#00F5FF;#FF6347;#8A2BE2;#FF00FF" dur="6s" repeatCount="indefinite"/></stop>
      <stop offset="100%"><animate attributeName="stop-color" values="#FF6347;#FF00FF;#8A2BE2;#00F5FF;#FF6347" dur="6s" repeatCount="indefinite"/></stop>
    </linearGradient>

    <linearGradient id="spaceBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%">
        <animate attributeName="stop-color"
          values="#001F3F;#002A5C;#3A0CA3;#001F3F"
          dur="18s" repeatCount="indefinite"/>
      </stop>

      <stop offset="50%">
        <animate attributeName="stop-color"
          values="#0A1128;#7209B7;#4CC9F0;#0A1128"
          dur="22s" repeatCount="indefinite"/>
      </stop>

      <stop offset="100%">
        <animate attributeName="stop-color"
          values="#02040A;#8A2BE2;#001F3F;#02040A"
          dur="26s" repeatCount="indefinite"/>
      </stop>
    </linearGradient>

    <linearGradient id="fadeGradient" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#001F3F" stop-opacity="0"/>
      <stop offset="35%" stop-color="#1A2A6C" stop-opacity="0.1"/>
      <stop offset="55%" stop-color="#3A0CA3" stop-opacity="0.3"/>
      <stop offset="75%" stop-color="#0A1128" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="#02040A" stop-opacity="0.8"/>   
    </linearGradient>

    <linearGradient id="imageBorder" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#8A2BE2" stop-opacity="0.6"/>
      <stop offset="50%" stop-color="#00F5FF" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#FF00FF" stop-opacity="0.6"/>
    </linearGradient>

    <radialGradient id="star">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow">
      <feDropShadow dx="0" dy="18" stdDeviation="25" flood-color="#000" flood-opacity="0.7"/>
    </filter>

    <filter id="imageGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="6" result="blur"/>
      <feFlood flood-color="#00F5FF" flood-opacity="0.5" result="glowColor"/>
      <feComposite in="glowColor" in2="blur" operator="in" result="softGlow"/>
      <feMerge>
        <feMergeNode in="softGlow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- MÁSCARA E CLIP PATH: usam exatamente o retângulo mestre -->
    <mask id="roundedMask">
      <rect x="{mask_rect_x}" y="{mask_rect_y}" width="{mask_rect_w}" height="{mask_rect_h}" rx="{rx}" ry="{rx}" fill="white"/>
    </mask>

    <clipPath id="imgClip">
      <rect x="{mask_rect_x}" y="{mask_rect_y}" rx="{rx}" ry="{rx}" width="{mask_rect_w}" height="{mask_rect_h}"/>
    </clipPath>
  </defs>

  <!-- BASE -->
  <rect width="1500" height="900" rx="42" ry="42" fill="url(#spaceBg)" filter="url(#softShadow)"/>

  <!-- ENERGY FRAME -->
  <rect x="10" y="10" width="1480" height="880" rx="36" ry="36"
        fill="none" stroke="url(#hyper)" stroke-width="3"/>

  <!-- STARFIELD (mantive como estava) -->
  <g fill="url(#star)">
    <circle cx="420" cy="80" r="1.4"/>
    <circle cx="560" cy="140" r="1.8"/>
    <circle cx="780" cy="60" r="1.6"/>
    <circle cx="1020" cy="120" r="2"/>
    <circle cx="1280" cy="90" r="1.5"/>
    <circle cx="1300" cy="200" r="2.1"/>
    <circle cx="860" cy="300" r="1.7"/>
    <circle cx="940" cy="360" r="2.2"/>
    <circle cx="720" cy="480" r="1.6"/>
    <circle cx="480" cy="520" r="2"/>
    <circle cx="900" cy="500" r="2.4"><animate attributeName="opacity" values="0.2;1;0.2" dur="6s" repeatCount="indefinite"/></circle>
    <circle cx="1050" cy="360" r="1.8"><animate attributeName="opacity" values="0.1;1;0.1" dur="5s" repeatCount="indefinite"/></circle>
  </g>

  <!-- IMAGE WINDOW COM EFEITOS -->
  <g>
    <!-- FUNDO ESCURO PARA CONTRASTE: expandi 6px em torno para garantir margem suave -->
    <rect x="{img_x - 6}" y="{img_y - 6}" rx="{rx + 6}" ry="{rx + 6}"
          width="{img_w + 12}" height="{img_h + 12}"
          fill="rgba(0,0,0,0.75)"/>

    <!-- BORDA GRADIENTE EXTERNA (posicionada com compensação de stroke) -->
    <rect x="{border_x}" y="{border_y}" rx="{rx}" ry="{rx}"
          width="{border_w}" height="{border_h}"
          fill="none" stroke="url(#imageBorder)" stroke-width="{border_stroke}"
          filter="url(#imageGlow)"/>

    <!-- IMAGEM (clip/mask usando o retângulo mestre) -->
    <image
      x="{img_x}"
      y="{img_y}"
      width="{img_w}"
      height="{img_h}"
      xlink:href="{img_base64}"
      preserveAspectRatio="xMidYMid slice"
      clip-path="url(#imgClip)"
      mask="url(#roundedMask)"
    />

    <!-- OVERLAY COM GRADIENTE DE TRANSPARÊNCIA (exatamente o mesmo retângulo) -->
    <rect x="{img_x}" y="{img_y}" width="{img_w}" height="{img_h}" rx="{rx}" ry="{rx}"
          fill="url(#fadeGradient)" mask="url(#roundedMask)"/>

    <!-- BORDA INTERNA SUTIL (mesma geometria) -->
    <rect x="{inner_x}" y="{inner_y}" rx="{rx}" ry="{rx}"
          width="{inner_w}" height="{inner_h}"
          fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="{inner_stroke}"/>

    <!-- BRILHO EXTRA NAS BORDAS EXTERNAS (retângulo maior para glow) -->
    <rect x="{brillo_x}" y="{brillo_y}" rx="{rx + 8}" ry="{rx + 8}"
          width="{brillo_w}" height="{brillo_h}"
          fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
  </g>

  <!-- TEXT TITLE -->
  <g transform="translate(40,50)">
    <text font-size="18" fill="#AFAAFF" font-family="Arial" letter-spacing="2">
      NASA · ASTRONOMY PICTURE OF THE DAY
    </text>
  </g>
  

  <!-- TEXT PANEL -->
  <g transform="translate(570,100)">
    <foreignObject y="0" width="840" height="80" fill="url(#hyper)">
      <div xmlns="http://www.w3.org/1999/xhtml" 
      style="
        font-family: Arial, sans-serif;
        font-size: 36px;
        line-height: 1.2;
        font-weight: 800;
        text-align: left;
        word-wrap: break-word;
        overflow-wrap: break-word;
        white-space: normal;
  
        background: linear-gradient(
          90deg,
          #00F5FF,
          #8A2BE2,
          #FF00FF,
          #FF6347,
          #00F5FF
        );
        background-size: 300% 300%;
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
  
        animation: gradientMove 6s ease infinite;
      ">

        {title}
      </div>
    </foreignObject>

    <rect y="85" width="840" height="2" fill="rgba(255,255,255,0.1)"/>

    <foreignObject y="95" width="840" height="600">
      <div xmlns="http://www.w3.org/1999/xhtml" 
      style="color: #FFFFFF; font-family: Arial, sans-serif; font-size: 
      20px; line-height: 1.6; text-align: justify; font-weight: 400; 
      white-space: pre-wrap; max-height: 590px; overflow-y: auto; 
      padding-right: 10px; text-shadow: 0 0 3px #EDEDF4, 0 0 6px #EDEDF4, 0 0 12px #5271FF, 
      0 0 24px #5271FF;">
        {explanation}
      </div>
    </foreignObject>
  </g>

  <!-- FOOTER -->
  <g transform="translate(80,710)">
    <text x="80" font-size="16" fill="#9FA0FF" font-family="Arial">
      🛰️ Data provided by NASA APOD
    </text>
  </g>

  <text x="750" y="880" text-anchor="middle" font-size="14" fill="#9FA0FF" font-family="Arial, Helvetica, sans-serif">
    🚀 Updated on {date_str}
  </text>
</svg>'''
    return svg


def main():
    """Ponto de entrada principal"""
    print("=" * 60)
    print("🌌 NASA API - SVG")
    print("=" * 60)
    
    # Criar pasta de output
    os.makedirs("output", exist_ok=True)
    
    # APOD
    print("\n📡 BUSCANDO APOD...")
    apod_data = get_nasa_apod()
    print(f"✅ APOD: {'Recebido' if apod_data else 'Usando fallback'}")
    
    # Gerar SVG APOD
    try:
        apod_svg = generate_apod_svg(apod_data)
        with open("output/nasa_apod.svg", "w", encoding="utf-8") as f:
            f.write(apod_svg)
        print("🖼️  SVG APOD gerado")
    except Exception as e:
        print(f"❌ Erro ao gerar SVG APOD: {e}")
    
   
    # Gerar markdown para README
    print("\n📄 GERANDO MARKDOWN PARA README...")
    md_content = f"""<!-- NASA_SECTION -->
<!-- Atualizado: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} -->

## 🚀 NASA APIs em Tempo Real - Visão Expandida

<div align="center">

### 🌟 Astronomy Picture of the Day (APOD)
[![NASA APOD](output/nasa_apod.svg)](https://apod.nasa.gov)
*Imagem astronômica diária com explicação científica*

<br>

<sub>🛰️ Dados em tempo real via NASA APIs • 🔄 Atualizado automaticamente a cada 4 horas</sub>
<sub>🎨 Design com gradiente neon #9B59B6 → #FF6347</sub>

</div>

<!-- END_NASA_SECTION -->
"""
    
    try:
        with open("output/nasa_section.md", "w", encoding="utf-8") as f:
            f.write(md_content)
        print("📄 Markdown gerado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao gerar markdown: {e}")
    
    print("=" * 60)
    print("✅ SVG GERADO COM SUCESSO!")
    print("📁 output/nasa_apod.svg")
    print("📁 output/nasa_section.md")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)