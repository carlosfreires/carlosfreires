"""
NASA APIs - VERSÃO HORIZONTAL 
3 SVGs grandes horizontais com gradiente neon #9B59B6 - #FF6347
"""
import requests
import os
import math
import base64
import random
from datetime import datetime, timezone, timedelta
from utils import validate_api_response

NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")

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

def get_mars_rover_photo():
    """Foto aleatória do Mars Rover"""
    rovers = ["curiosity", "opportunity", "spirit"]
    rover = random.choice(rovers)
    
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos"
    
    sol = random.randint(1, 2000) if rover == "curiosity" else random.randint(1, 5000)
    params = {"api_key": NASA_API_KEY, "sol": sol, "page": 1}
    
    data = safe_get(url, params, api_name="Mars Rover Photos")
    
    if data and data.get("photos"):
        photo = random.choice(data["photos"])
        return {
            "img_src": photo["img_src"],
            "earth_date": photo["earth_date"],
            "rover": photo["rover"]["name"],
            "camera": photo["camera"]["full_name"],
            "rover_type": rover.capitalize(),
            "sol": photo["sol"]
        }
    return None

def get_epic_image():
    """Imagem mais recente da EPIC (Terra)"""
    url = "https://api.nasa.gov/EPIC/api/natural"
    params = {"api_key": NASA_API_KEY}
    
    data = safe_get(url, params, api_name="EPIC")
    
    if data and len(data) > 0:
        latest = data[0]
        date_obj = datetime.strptime(latest["date"], "%Y-%m-%d %H:%M:%S")
        date_str = date_obj.strftime("%Y/%m/%d")
        
        return {
            "image": latest["image"],
            "date": date_obj.strftime("%Y-%m-%d"),
            "time": date_obj.strftime("%H:%M UTC"),
            "image_url": f"https://epic.gsfc.nasa.gov/archive/natural/{date_str}/png/{latest['image']}.png",
            "caption": latest.get("caption", "Terra vista do espaço"),
            "distance": "1.5 milhão de km"
        }
    return None

def image_to_base64(url, max_size=(800, 400)):
    """Converte imagem para Base64 com otimização"""
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        
        content_type = response.headers.get('content-type', 'image/jpeg')
        encoded = base64.b64encode(response.content).decode('utf-8')
        return f"data:{content_type};base64,{encoded}"
    except Exception as e:
        print(f"⚠️  Falha ao converter imagem: {e}")
        return None

def get_fallback_image():
    """Imagem de fallback em Base64"""
    return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="

def escape_svg(text, max_length=100):
    """Escapa caracteres especiais para SVG"""
    if not text:
        return ""
    replacements = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&apos;'
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    
    return text[:max_length] + "..." if len(text) > max_length else text

def generate_horizontal_apod_svg(apod_data):
    """Gera SVG horizontal grande para APOD"""
    
    default_apod = {
        'title': 'Universo em Foco: Imagem Astronômica do Dia',
        'explanation': 'A NASA seleciona diariamente uma imagem ou fotografia diferente do nosso fascinante universo, acompanhada por uma breve explicação escrita por um astrônomo profissional.',
        'date': datetime.now(timezone.utc).strftime('%Y-%m-%d'),
        'url': 'https://apod.nasa.gov/apod/image/2401/aurora_jin_960.jpg',
        'media_type': 'image',
        'copyright': 'NASA Astronomy Picture of the Day'
    }
    
    apod = apod_data or default_apod
    
    img_base64 = image_to_base64(apod['url'])
    if not img_base64:
        img_base64 = get_fallback_image()
    
    title = escape_svg(apod['title'][:60])
    explanation = escape_svg(apod['explanation'][:250])
    date_str = apod.get('date', datetime.now(timezone.utc).strftime('%Y-%m-%d'))
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
     width="1200" height="400" viewBox="0 0 1200 400">
  
  <defs>
    <!-- Gradiente neon principal -->
    <linearGradient id="apodNeonBg" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#9B59B6"/>
      <stop offset="50%" stop-color="#E74C3C"/>
      <stop offset="100%" stop-color="#FF6347"/>
    </linearGradient>
    
    <!-- Gradiente para imagem -->
    <linearGradient id="imageOverlay" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#9B59B6" stop-opacity="0.7"/>
      <stop offset="100%" stop-color="#FF6347" stop-opacity="0.7"/>
    </linearGradient>
    
    <!-- Efeitos de brilho -->
    <filter id="neonGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
    
    <filter id="imageShadow">
      <feDropShadow dx="5" dy="5" stdDeviation="10" flood-color="#FF6347" flood-opacity="0.3"/>
    </filter>
    
    <clipPath id="roundedImage">
      <rect x="40" y="40" width="500" height="320" rx="15" ry="15"/>
    </clipPath>
  </defs>
  
  <!-- Fundo com gradiente neon -->
  <rect width="1200" height="400" fill="url(#apodNeonBg)"/>
  
  <!-- Sobreposição escura para contraste -->
  <rect width="1200" height="400" fill="#000000" opacity="0.7"/>
  
  <!-- Container do card -->
  <rect x="20" y="20" width="1160" height="360" rx="20" ry="20" 
        fill="rgba(0, 0, 0, 0.6)" stroke="#FF6347" stroke-width="3"/>
  
  <!-- Imagem principal -->
  <g filter="url(#imageShadow)">
    <rect x="40" y="40" width="500" height="320" rx="15" ry="15" 
          fill="#000000" stroke="#9B59B6" stroke-width="2"/>
    <image x="40" y="40" width="500" height="320" 
           xlink:href="{img_base64}" clip-path="url(#roundedImage)"
           preserveAspectRatio="xMidYMid cover"/>
    
    <!-- Overlay gradiente na imagem -->
    <rect x="40" y="40" width="500" height="320" rx="15" ry="15" 
          fill="url(#imageOverlay)" opacity="0.3"/>
  </g>
  
  <!-- Conteúdo textual -->
  <g transform="translate(570, 40)">
    
    <!-- Título -->
    <text x="0" y="40" font-size="28" font-weight="bold" 
          fill="#FFFFFF" font-family="Arial, Helvetica, sans-serif">
      🌟 ASTRONOMY PICTURE OF THE DAY
    </text>
    
    <text x="0" y="80" font-size="32" font-weight="bold" 
          fill="#FF6347" font-family="Arial, Helvetica, sans-serif">
      {title}
    </text>
    
    <!-- Descrição -->
    <foreignObject x="0" y="120" width="570" height="120">
      <div xmlns="http://www.w3.org/1999/xhtml" 
           style="color:#E0E0E0; font-size:16px; font-family:Arial,sans-serif; 
                  line-height:1.5; text-align:justify;">
        {explanation}
      </div>
    </foreignObject>
    
    <!-- Metadados -->
    <g transform="translate(0, 260)">
      <rect x="0" y="0" width="570" height="100" rx="10" ry="10" 
            fill="rgba(155, 89, 182, 0.2)"/>
      
      <g transform="translate(20, 20)">
        <text x="0" y="0" font-size="14" fill="#FFD700" font-family="Arial">
          📅 <tspan fill="#FFFFFF" font-weight="bold">Data:</tspan> 
          <tspan fill="#9B59B6"> {date_str}</tspan>
        </text>
        
        <text x="0" y="25" font-size="14" fill="#FFD700" font-family="Arial">
          🖼️ <tspan fill="#FFFFFF" font-weight="bold">Tipo:</tspan> 
          <tspan fill="#9B59B6"> Imagem Astronômica</tspan>
        </text>
        
        <text x="0" y="50" font-size="14" fill="#FFD700" font-family="Arial">
          🔭 <tspan fill="#FFFFFF" font-weight="bold">Fonte:</tspan> 
          <tspan fill="#9B59B6"> NASA APOD</tspan>
        </text>
      </g>
      
      <!-- Botão de ação -->
      <a xlink:href="https://apod.nasa.gov/apod/astropix.html" target="_blank">
        <rect x="400" y="20" width="150" height="60" rx="10" ry="10" 
              fill="#FF6347" opacity="0.9"/>
        <text x="475" y="55" text-anchor="middle" font-size="16" 
              fill="#FFFFFF" font-weight="bold" font-family="Arial">
          🌐 VER COMPLETO
        </text>
      </a>
    </g>
  </g>
  
  <!-- Elementos decorativos -->
  <circle cx="1150" cy="50" r="10" fill="#FF6347" opacity="0.6">
    <animate attributeName="r" values="10;15;10" dur="2s" repeatCount="indefinite"/>
  </circle>
  
  <circle cx="50" cy="350" r="8" fill="#9B59B6" opacity="0.6">
    <animate attributeName="r" values="8;12;8" dur="3s" repeatCount="indefinite"/>
  </circle>
  
  <!-- Rodapé -->
  <text x="600" y="390" text-anchor="middle" font-size="12" 
        fill="#FFD700" font-family="Arial, Helvetica, sans-serif">
    🚀 NASA APOD • Atualizado em tempo real • {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}
  </text>
</svg>'''
    
    return svg

def generate_horizontal_mars_svg(mars_data):
    """Gera SVG horizontal grande para Mars Rover"""
    
    default_mars = {
        'img_src': 'https://mars.nasa.gov/system/resources/detail_files/26895_1-PIA24546-1280.jpg',
        'earth_date': datetime.now(timezone.utc).strftime('%Y-%m-%d'),
        'rover': 'Curiosity',
        'camera': 'Mast Camera (Mastcam)',
        'rover_type': 'Curiosity',
        'sol': '3000'
    }
    
    mars = mars_data or default_mars
    
    img_base64 = image_to_base64(mars['img_src'])
    if not img_base64:
        img_base64 = get_fallback_image()
    
    rover = escape_svg(mars['rover'])
    camera = escape_svg(mars['camera'])
    date_str = mars['earth_date']
    sol = mars.get('sol', 'N/A')
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
     width="1200" height="400" viewBox="0 0 1200 400">
  
  <defs>
    <!-- Gradiente neon invertido -->
    <linearGradient id="marsNeonBg" x1="100%" y1="0%" x2="0%" y2="0%">
      <stop offset="0%" stop-color="#FF6347"/>
      <stop offset="50%" stop-color="#E74C3C"/>
      <stop offset="100%" stop-color="#9B59B6"/>
    </linearGradient>
    
    <!-- Gradiente para texto -->
    <linearGradient id="textGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FF6347"/>
      <stop offset="100%" stop-color="#FFD700"/>
    </linearGradient>
    
    <!-- Padrão marciano -->
    <pattern id="marsPattern" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
      <circle cx="10" cy="10" r="2" fill="#FF6347" opacity="0.3"/>
    </pattern>
    
    <filter id="marsGlow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    
    <clipPath id="marsImageClip">
      <rect x="650" y="40" width="500" height="320" rx="15" ry="15"/>
    </clipPath>
  </defs>
  
  <!-- Fundo com padrão marciano -->
  <rect width="1200" height="400" fill="url(#marsNeonBg)"/>
  <rect width="1200" height="400" fill="url(#marsPattern)" opacity="0.2"/>
  
  <!-- Container principal -->
  <rect x="20" y="20" width="1160" height="360" rx="20" ry="20" 
        fill="rgba(20, 10, 5, 0.8)" stroke="#FF6347" stroke-width="3"/>
  
  <!-- Conteúdo textual (esquerda) -->
  <g transform="translate(50, 40)">
    
    <!-- Cabeçalho -->
    <text x="0" y="40" font-size="32" font-weight="bold" 
          fill="url(#textGradient)" font-family="Arial, Helvetica, sans-serif">
      🚀 MISSÃO MARS ROVER
    </text>
    
    <text x="0" y="85" font-size="36" font-weight="bold" 
          fill="#FFFFFF" font-family="Arial, Helvetica, sans-serif">
      Explorando o{" "}
      <tspan fill="#FF6347">Planeta Vermelho</tspan>
    </text>
    
    <!-- Descrição -->
    <foreignObject x="0" y="130" width="550" height="100">
      <div xmlns="http://www.w3.org/1999/xhtml" 
           style="color:#E0E0E0; font-size:16px; font-family:Arial,sans-serif; 
                  line-height:1.5; text-align:justify;">
        Os rovers da NASA estão explorando Marte desde 2004, coletando dados científicos
        e imagens inéditas da superfície marciana. Cada rover é um laboratório móvel
        equipado com instrumentos científicos avançados.
      </div>
    </foreignObject>
    
    <!-- Estatísticas -->
    <g transform="translate(0, 250)">
      <rect x="0" y="0" width="550" height="110" rx="10" ry="10" 
            fill="rgba(255, 99, 71, 0.15)"/>
      
      <g transform="translate(20, 15)">
        <!-- Linha 1 -->
        <text x="0" y="0" font-size="14" fill="#FFD700" font-family="Arial">
          🤖 <tspan fill="#FFFFFF">Rover Ativo:</tspan>
          <tspan fill="#9B59B6" font-weight="bold"> {rover}</tspan>
        </text>
        
        <text x="280" y="0" font-size="14" fill="#FFD700" font-family="Arial">
          📷 <tspan fill="#FFFFFF">Câmera:</tspan>
          <tspan fill="#9B59B6"> {camera[:25]}...</tspan>
        </text>
        
        <!-- Linha 2 -->
        <text x="0" y="30" font-size="14" fill="#FFD700" font-family="Arial">
          📅 <tspan fill="#FFFFFF">Data Terrestre:</tspan>
          <tspan fill="#FF6347"> {date_str}</tspan>
        </text>
        
        <text x="280" y="30" font-size="14" fill="#FFD700" font-family="Arial">
          🔴 <tspan fill="#FFFFFF">Sol Marciano:</tspan>
          <tspan fill="#FF6347"> {sol}</tspan>
        </text>
        
        <!-- Linha 3 -->
        <text x="0" y="60" font-size="14" fill="#FFD700" font-family="Arial">
          🛰️ <tspan fill="#FFFFFF">Rovers Ativos:</tspan>
          <tspan fill="#9B59B6"> Curiosity, Perseverance</tspan>
        </text>
        
        <text x="280" y="60" font-size="14" fill="#FFD700" font-family="Arial">
          ⏱️ <tspan fill="#FFFFFF">Desde:</tspan>
          <tspan fill="#FF6347"> 2004</tspan>
        </text>
      </g>
    </g>
  </g>
  
  <!-- Imagem de Marte (direita) -->
  <g filter="url(#marsGlow)" transform="translate(650, 40)">
    <rect x="0" y="0" width="500" height="320" rx="15" ry="15" 
          fill="#000000" stroke="#9B59B6" stroke-width="3"/>
    <image x="0" y="0" width="500" height="320" 
           xlink:href="{img_base64}" clip-path="url(#marsImageClip)"
           preserveAspectRatio="xMidYMid cover"/>
    
    <!-- Overlay informativo -->
    <rect x="0" y="220" width="500" height="100" rx="0" ry="0" 
          fill="rgba(0, 0, 0, 0.7)"/>
    
    <text x="250" y="255" text-anchor="middle" font-size="18" 
          fill="#FFD700" font-family="Arial, Helvetica, sans-serif">
      SUPERFÍCIE MARCIANA
    </text>
    
    <text x="250" y="285" text-anchor="middle" font-size="14" 
          fill="#9B59B6" font-family="Arial, Helvetica, sans-serif">
      Foto real do rover {rover}
    </text>
  </g>
  
  <!-- Botão de ação -->
  <a xlink:href="https://mars.nasa.gov/mars2020/multimedia/raw-images/" target="_blank">
    <g transform="translate(950, 310)">
      <rect x="0" y="0" width="200" height="50" rx="10" ry="10" 
            fill="#FF6347" opacity="0.9"/>
      <text x="100" y="30" text-anchor="middle" font-size="16" 
            fill="#FFFFFF" font-weight="bold" font-family="Arial">
        🪐 EXPLORAR MARTE
      </text>
    </g>
  </a>
  
  <!-- Elementos decorativos -->
  <circle cx="1100" cy="80" r="12" fill="#FF6347" opacity="0.7">
    <animate attributeName="opacity" values="0.7;1;0.7" dur="2s" repeatCount="indefinite"/>
  </circle>
  
  <circle cx="100" cy="350" r="10" fill="#9B59B6" opacity="0.7">
    <animate attributeName="opacity" values="0.7;1;0.7" dur="3s" repeatCount="indefinite"/>
  </circle>
  
  <!-- Rodapé -->
  <text x="600" y="390" text-anchor="middle" font-size="12" 
        fill="#FFD700" font-family="Arial, Helvetica, sans-serif">
    🔴 NASA Mars Exploration Program • Imagens reais do Planeta Vermelho • {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}
  </text>
</svg>'''
    
    return svg

def generate_horizontal_epic_svg(epic_data):
    """Gera SVG horizontal grande para EPIC (Terra)"""
    
    default_epic = {
        'image_url': 'https://epic.gsfc.nasa.gov/archive/natural/2024/01/01/png/epic_1b_20240101003608.png',
        'date': datetime.now(timezone.utc).strftime('%Y-%m-%d'),
        'time': datetime.now(timezone.utc).strftime('%H:%M UTC'),
        'caption': 'Terra vista do espaço - Pálido Ponto Azul',
        'distance': '1.5 milhão de km'
    }
    
    epic = epic_data or default_epic
    
    img_base64 = image_to_base64(epic['image_url'])
    if not img_base64:
        img_base64 = get_fallback_image()
    
    date_str = epic['date']
    time_str = epic['time']
    distance = epic.get('distance', '1.5 milhão de km')
    caption = escape_svg(epic['caption'])
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
     width="1200" height="400" viewBox="0 0 1200 400">
  
  <defs>
    <!-- Gradiente neon diagonal -->
    <linearGradient id="epicNeonBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#9B59B6"/>
      <stop offset="50%" stop-color="#E74C3C"/>
      <stop offset="100%" stop-color="#FF6347"/>
    </linearGradient>
    
    <!-- Gradiente circular para a Terra -->
    <radialGradient id="earthGlow" cx="30%" cy="40%" r="70%">
      <stop offset="0%" stop-color="#00BFFF" stop-opacity="0.8"/>
      <stop offset="70%" stop-color="#1E90FF" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#00008B" stop-opacity="0.1"/>
    </radialGradient>
    
    <!-- Efeitos de estrelas -->
    <filter id="starTwinkle">
      <feGaussianBlur in="SourceAlpha" stdDeviation="2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    
    <!-- Padrão de estrelas -->
    <pattern id="starPattern" x="0" y="0" width="50" height="50" patternUnits="userSpaceOnUse">
      <circle cx="25" cy="25" r="0.5" fill="#FFFFFF" opacity="0.3">
        <animate attributeName="r" values="0.5;1;0.5" dur="4s" repeatCount="indefinite"/>
      </circle>
    </pattern>
    
    <clipPath id="earthClip">
      <circle cx="300" cy="200" r="130"/>
    </clipPath>
  </defs>
  
  <!-- Fundo espacial -->
  <rect width="1200" height="400" fill="#000000"/>
  <rect width="1200" height="400" fill="url(#starPattern)" opacity="0.5"/>
  <rect width="1200" height="400" fill="url(#epicNeonBg)" opacity="0.3"/>
  
  <!-- Container principal -->
  <rect x="20" y="20" width="1160" height="360" rx="20" ry="20" 
        fill="rgba(10, 20, 40, 0.85)" stroke="#00BFFF" stroke-width="3"/>
  
  <!-- Globo Terra (esquerda) -->
  <g transform="translate(50, 40)">
    <circle cx="250" cy="160" r="150" fill="url(#earthGlow)"/>
    
    <!-- Imagem da Terra -->
    <a xlink:href="{epic['image_url']}" target="_blank">
      <circle cx="250" cy="160" r="130" fill="#000000" stroke="#00BFFF" stroke-width="3"/>
      <image x="120" y="30" width="260" height="260" 
             xlink:href="{img_base64}" clip-path="url(#earthClip)"
             preserveAspectRatio="xMidYMid meet"/>
    </a>
    
    <!-- Anéis orbitais -->
    <circle cx="250" cy="160" r="145" fill="none" stroke="#00FFFF" 
            stroke-width="1" stroke-dasharray="5,5" opacity="0.6"/>
    <circle cx="250" cy="160" r="160" fill="none" stroke="#9B59B6" 
            stroke-width="1" stroke-dasharray="3,7" opacity="0.4"/>
    
    <!-- Informações sobre a Terra -->
    <g transform="translate(400, 0)">
      <text x="0" y="40" font-size="36" font-weight="bold" 
            fill="#00FFFF" font-family="Arial, Helvetica, sans-serif">
        🌍 NOSSO PLANETA
      </text>
      
      <text x="0" y="85" font-size="28" font-weight="bold" 
            fill="#FFFFFF" font-family="Arial, Helvetica, sans-serif">
        Pálido <tspan fill="#9B59B6">Ponto</tspan>{" "}
        <tspan fill="#FF6347">Azul</tspan>
      </text>
      
      <foreignObject x="0" y="120" width="500" height="120">
        <div xmlns="http://www.w3.org/1999/xhtml" 
             style="color:#E0E0E0; font-size:16px; font-family:Arial,sans-serif; 
                    line-height:1.5; text-align:justify;">
          A câmera EPIC (Earth Polychromatic Imaging Camera) a bordo do satélite DSCOVR 
          tira fotos coloridas da Terra de uma distância de {distance}, 
          mostrando o lado iluminado do nosso planeta como ele realmente é.
        </div>
      </foreignObject>
    </g>
  </g>
  
  <!-- Estatísticas e dados -->
  <g transform="translate(500, 260)">
    <rect x="0" y="0" width="650" height="100" rx="15" ry="15" 
          fill="rgba(0, 191, 255, 0.1)"/>
    
    <g transform="translate(20, 20)">
      <!-- Linha 1 -->
      <text x="0" y="0" font-size="14" fill="#FFD700" font-family="Arial">
        📅 <tspan fill="#FFFFFF">Data da Imagem:</tspan>
        <tspan fill="#00FFFF" font-weight="bold"> {date_str}</tspan>
      </text>
      
      <text x="250" y="0" font-size="14" fill="#FFD700" font-family="Arial">
        ⏰ <tspan fill="#FFFFFF">Hora UTC:</tspan>
        <tspan fill="#00FFFF"> {time_str}</tspan>
      </text>
      
      <text x="450" y="0" font-size="14" fill="#FFD700" font-family="Arial">
        📡 <tspan fill="#FFFFFF">Distância:</tspan>
        <tspan fill="#9B59B6"> {distance}</tspan>
      </text>
      
      <!-- Linha 2 -->
      <text x="0" y="30" font-size="14" fill="#FFD700" font-family="Arial">
        🛰️ <tspan fill="#FFFFFF">Satélite:</tspan>
        <tspan fill="#FF6347"> DSCOVR</tspan>
      </text>
      
      <text x="250" y="30" font-size="14" fill="#FFD700" font-family="Arial">
        📷 <tspan fill="#FFFFFF">Câmera:</tspan>
        <tspan fill="#FF6347"> EPIC</tspan>
      </text>
      
      <text x="450" y="30" font-size="14" fill="#FFD700" font-family="Arial">
        🌐 <tspan fill="#FFFFFF">Órbita:</tspan>
        <tspan fill="#9B59B6"> L1 Lagrange</tspan>
      </text>
      
      <!-- Linha 3 -->
      <text x="0" y="60" font-size="14" fill="#FFD700" font-family="Arial">
        🎯 <tspan fill="#FFFFFF">Objetivo:</tspan>
        <tspan fill="#00BFFF"> Monitoramento terrestre</tspan>
      </text>
    </g>
  </g>
  
  <!-- Citação de Carl Sagan -->
  <g transform="translate(750, 180)">
    <rect x="0" y="0" width="400" height="70" rx="10" ry="10" 
          fill="rgba(155, 89, 182, 0.3)"/>
    
    <text x="200" y="25" text-anchor="middle" font-size="12" 
          fill="#FFD700" font-family="Arial" font-style="italic">
      "Olhe de novo para esse ponto. É aqui. É a nossa casa. Somos nós."
    </text>
    
    <text x="200" y="45" text-anchor="middle" font-size="11" 
          fill="#9B59B6" font-family="Arial">
      — Carl Sagan, Pálido Ponto Azul
    </text>
  </g>
  
  <!-- Botão de ação -->
  <a xlink:href="https://epic.gsfc.nasa.gov" target="_blank">
    <g transform="translate(950, 320)">
      <rect x="0" y="0" width="200" height="50" rx="10" ry="10" 
            fill="linear-gradient(90deg, #00BFFF, #9B59B6)" opacity="0.9"/>
      <text x="100" y="30" text-anchor="middle" font-size="16" 
            fill="#FFFFFF" font-weight="bold" font-family="Arial">
        🌐 VER TERRA AO VIVO
      </text>
    </g>
  </a>
  
  <!-- Elementos decorativos -->
  <circle cx="1150" cy="100" r="8" fill="#00FFFF" opacity="0.7" filter="url(#starTwinkle)">
    <animate attributeName="opacity" values="0.3;0.8;0.3" dur="3s" repeatCount="indefinite"/>
  </circle>
  
  <circle cx="80" cy="320" r="6" fill="#FF6347" opacity="0.7" filter="url(#starTwinkle)">
    <animate attributeName="opacity" values="0.3;0.8;0.3" dur="2.5s" repeatCount="indefinite"/>
  </circle>
  
  <!-- Rodapé -->
  <text x="600" y="390" text-anchor="middle" font-size="12" 
        fill="#FFD700" font-family="Arial, Helvetica, sans-serif">
    🌍 NASA EPIC • Terra vista do espaço • Distância: {distance} • {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}
  </text>
</svg>'''
    
    return svg

def main():
    """Ponto de entrada principal"""
    print("=" * 60)
    print("🌌 NASA APIS - SVGs HORIZONTAIS GRANDES")
    print("=" * 60)
    
    # Criar pasta de output
    os.makedirs("output", exist_ok=True)
    
    # 1. APOD
    print("\n📡 BUSCANDO APOD...")
    apod_data = get_nasa_apod()
    print(f"✅ APOD: {'Recebido' if apod_data else 'Usando fallback'}")
    
    apod_svg = generate_horizontal_apod_svg(apod_data)
    with open("output/nasa_apod_horizontal.svg", "w", encoding="utf-8") as f:
        f.write(apod_svg)
    print("🖼️  SVG APOD horizontal gerado")
    
    # 2. Mars Rover
    print("\n📡 BUSCANDO MARS ROVER...")
    mars_data = get_mars_rover_photo()
    print(f"✅ Mars Rover: {'Recebido' if mars_data else 'Usando fallback'}")
    
    mars_svg = generate_horizontal_mars_svg(mars_data)
    with open("output/nasa_mars_horizontal.svg", "w", encoding="utf-8") as f:
        f.write(mars_svg)
    print("🖼️  SVG Mars horizontal gerado")
    
    # 3. EPIC (Terra)
    print("\n📡 BUSCANDO EPIC (TERRA)...")
    epic_data = get_epic_image()
    print(f"✅ EPIC Terra: {'Recebido' if epic_data else 'Usando fallback'}")
    
    epic_svg = generate_horizontal_epic_svg(epic_data)
    with open("output/nasa_epic_horizontal.svg", "w", encoding="utf-8") as f:
        f.write(epic_svg)
    print("🖼️  SVG EPIC horizontal gerado")
    
    # Gerar markdown para README
    print("\n📄 GERANDO MARKDOWN PARA README...")
    md_content = f"""<!-- NASA_HORIZONTAL_SECTION -->
<!-- Atualizado: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} -->

## 🚀 NASA APIs em Tempo Real - Visão Expandida

<div align="center">

### 🌟 Astronomy Picture of the Day (APOD)
[![NASA APOD](output/nasa_apod_horizontal.svg)](https://apod.nasa.gov)
*Imagem astronômica diária com explicação científica*

---

### 🚀 Mars Rover Photos
[![Mars Rover](output/nasa_mars_horizontal.svg)](https://mars.nasa.gov)
*Fotos reais da superfície de Marte pelos rovers da NASA*

---

### 🌍 Earth from Space (EPIC)
[![Earth from Space](output/nasa_epic_horizontal.svg)](https://epic.gsfc.nasa.gov)
*Terra vista do satélite DSCOVR a 1.5 milhão de km*

<br>

<sub>🛰️ Dados em tempo real via NASA APIs • 🔄 Atualizado automaticamente a cada 4 horas</sub>
<sub>🎨 Design com gradiente neon #9B59B6 → #FF6347</sub>

</div>

<!-- END_NASA_HORIZONTAL_SECTION -->
"""
    
    with open("output/nasa_horizontal_section.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    
    print("=" * 60)
    print("✅ TODOS OS 3 SVGs HORIZONTAIS GERADOS COM SUCESSO!")
    print("📁 output/nasa_apod_horizontal.svg")
    print("📁 output/nasa_mars_horizontal.svg")
    print("📁 output/nasa_epic_horizontal.svg")
    print("📁 output/nasa_horizontal_section.md")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)