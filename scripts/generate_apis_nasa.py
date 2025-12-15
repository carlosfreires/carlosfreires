"""
NASA APIs - VERSÃO 2.1 
Gera SVG com imagens em Base64 para compatibilidade com GitHub
"""
import requests
import os
import math
import base64
from datetime import datetime, timezone
from utils import validate_api_response

NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")

def safe_get(url, params=None, timeout=10, api_name="API"):
    """Requisição HTTP segura"""
    try:
        response = requests.get(url, params=params, timeout=timeout)
        if validate_api_response(response, api_name):
            return response.json()
    except Exception as e:
        print(f"❌ {api_name}: {e}")
    return None

def get_nasa_apod():
    """Obtém Astronomy Picture of the Day"""
    url = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": NASA_API_KEY, "thumbs": "True"}
    data = safe_get(url, params, api_name="NASA APOD")
    
    # Validar que é uma imagem (não vídeo)
    if data and data.get("media_type") != "image":
        print(f"⚠️  APOD é vídeo (não imagem): {data.get('media_type')}")
        return None
    
    return data

def get_iss_location():
    """Localização da Estação Espacial"""
    url = "http://api.open-notify.org/iss-now.json"
    return safe_get(url, timeout=5, api_name="ISS Location")

def image_to_base64(url):
    """Converte imagem para Base64"""
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        # Determinar content type
        content_type = response.headers.get('content-type', 'image/jpeg')
        
        # Converter para base64
        encoded = base64.b64encode(response.content).decode('utf-8')
        return f"data:{content_type};base64,{encoded}"
    except Exception as e:
        print(f"⚠️  Falha ao converter imagem para Base64: {e}")
        return None

def get_fallback_image():
    """Imagem de fallback em Base64"""
    # Pixel transparente como fallback
    return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="

def escape_xml(text):
    """Escapa caracteres especiais para XML"""
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
    return text

def generate_nasa_svg(apod_data, iss_data):
    """Gera SVG para a seção NASA"""
    
    # Dados padrão para fallback
    default_apod = {
        'title': 'Universo em Foco',
        'explanation': 'Explore o cosmos com imagens diárias da NASA.',
        'date': datetime.now(timezone.utc).strftime('%Y-%m-%d'),
        'url': 'https://apod.nasa.gov/apod/image/2401/aurora_jin_960.jpg'
    }
    
    apod = apod_data or default_apod
    has_iss = iss_data and 'iss_position' in iss_data
    
    # Obter imagem em Base64
    print("🖼️  CONVERTENDO IMAGEM PARA BASE64...")
    img_base64 = image_to_base64(apod['url'])
    if not img_base64:
        img_base64 = get_fallback_image()
        print("⚠️  Usando imagem de fallback")
    
    # Processar dados da ISS
    if has_iss:
        lat = float(iss_data['iss_position']['latitude'])
        lon = float(iss_data['iss_position']['longitude'])
        lat_rad = math.radians(lat)
        lon_rad = math.radians(lon)
        
        # Posição no círculo (projeção simplificada)
        iss_x = 225 + 90 * math.cos(lon_rad) * math.cos(lat_rad)
        iss_y = 200 + 90 * math.sin(lat_rad)
    else:
        lat = 0.0
        lon = 0.0
        iss_x = 225
        iss_y = 200
    
    # Escapar texto para XML
    title = escape_xml(apod['title'][:50])
    explanation = escape_xml(apod['explanation'][:150])
    
    # Gerar SVG com Base64
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1200" height="700" viewBox="0 0 1200 700">
  <defs>
    <!-- Gradientes -->
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1a0d27;stop-opacity:0.95"/>
      <stop offset="100%" style="stop-color:#2a0047;stop-opacity:0.95"/>
    </linearGradient>
    
    <linearGradient id="titleGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#FF416C"/>
      <stop offset="50%" style="stop-color:#FF4B2B"/>
      <stop offset="100%" style="stop-color:#8A2BE2"/>
    </linearGradient>
    
    <!-- Filtros -->
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="10" stdDeviation="20" flood-color="#9400d3" flood-opacity="0.4"/>
    </filter>
    
    <!-- Clip paths -->
    <clipPath id="imageClip">
      <rect x="0" y="0" width="400" height="200" rx="10" ry="10"/>
    </clipPath>
  </defs>
  
  <!-- Fundo principal -->
  <rect x="10" y="10" width="1180" height="680" rx="20" ry="20" 
        fill="url(#bgGradient)" filter="url(#shadow)" stroke="#8A2BE2" stroke-width="2"/>
  
  <!-- Título -->
  <text x="600" y="80" text-anchor="middle" font-size="36" font-weight="bold" 
        fill="url(#titleGradient)" font-family="Arial, Helvetica, sans-serif">
    🚀 EXPLORAÇÃO COSMOS • 🌌 NASA APIs
  </text>
  
  <!-- Grid de cards -->
  <g transform="translate(60, 120)">
    
    <!-- Card APOD -->
    <g transform="translate(0, 0)">
      <rect x="0" y="0" width="520" height="500" rx="15" ry="15" 
            fill="rgba(0,0,0,0.7)" stroke="#8A2BE2" stroke-width="2"/>
      
      <text x="260" y="40" text-anchor="middle" font-size="22" font-weight="bold" 
            fill="#FF6347" font-family="Arial, Helvetica, sans-serif">
        📷 IMAGEM ASTRONÔMICA DO DIA
      </text>
      
      <!-- Imagem APOD em Base64 -->
      <a xlink:href="{apod['url']}" target="_blank">
        <g transform="translate(60, 70)">
          <rect x="0" y="0" width="400" height="200" rx="10" ry="10" 
                fill="#000" stroke="#FF6347" stroke-width="2"/>
          <image x="0" y="0" width="400" height="200" 
                 xlink:href="{img_base64}" clip-path="url(#imageClip)"/>
        </g>
      </a>
      
      <!-- Título APOD -->
      <text x="260" y="300" text-anchor="middle" font-size="18" font-weight="bold" 
            fill="#00FFFF" font-family="Arial, Helvetica, sans-serif">
        {title}
      </text>
      
      <!-- Descrição -->
      <foreignObject x="60" y="330" width="400" height="80">
        <div xmlns="http://www.w3.org/1999/xhtml" style="color:#9B59B6;font-size:14px;font-family:Arial,sans-serif;line-height:1.4;">
          {apod['explanation'][:180]}...
        </div>
      </foreignObject>
      
      <!-- Rodapé APOD -->
      <g transform="translate(60, 430)">
        <text x="0" y="0" font-size="12" fill="#FFD700" 
              font-family="Arial, Helvetica, sans-serif">
          📅 {apod.get('date', 'Data indisponível')}
        </text>
        
        <a xlink:href="https://apod.nasa.gov/apod/astropix.html" target="_blank">
          <text x="400" y="0" text-anchor="end" font-size="12" 
                fill="#FF6347" font-family="Arial, Helvetica, sans-serif" 
                style="text-decoration: underline;">
            🌐 Ver no site da NASA
          </text>
        </a>
      </g>
    </g>
    
    <!-- Card ISS -->
    <g transform="translate(580, 0)">
      <rect x="0" y="0" width="520" height="500" rx="15" ry="15" 
            fill="rgba(0,0,0,0.7)" stroke="#00FFFF" stroke-width="2"/>
      
      <text x="260" y="40" text-anchor="middle" font-size="22" font-weight="bold" 
            fill="#00FFFF" font-family="Arial, Helvetica, sans-serif">
        🛰️ ESTAÇÃO ESPACIAL INTERNACIONAL
      </text>
      
      <!-- Círculo da Terra -->
      <g transform="translate(260, 200)">
        <circle cx="0" cy="0" r="100" fill="none" 
                stroke="#00FFFF" stroke-width="2" stroke-dasharray="5,5"/>
        
        <!-- Ponto ISS -->
        <circle cx="{iss_x - 260}" cy="{iss_y - 200}" r="8" fill="#FF6347">
          <animate attributeName="r" values="8;12;8" dur="2s" repeatCount="indefinite"/>
        </circle>
        
        <!-- Centro -->
        <circle cx="0" cy="0" r="3" fill="#00FFFF"/>
      </g>
      
      <!-- Coordenadas -->
      <g transform="translate(260, 350)">
        <g transform="translate(-100, 0)">
          <rect x="0" y="0" width="100" height="50" rx="8" ry="8" 
                fill="rgba(0,255,255,0.1)"/>
          <text x="50" y="20" text-anchor="middle" font-size="12" 
                fill="#00FFFF" font-family="Arial, Helvetica, sans-serif">
            LATITUDE
          </text>
          <text x="50" y="40" text-anchor="middle" font-size="18" font-weight="bold" 
                fill="#FFFFFF" font-family="Arial, Helvetica, sans-serif">
            {lat:.2f}°
          </text>
        </g>
        
        <g transform="translate(20, 0)">
          <rect x="0" y="0" width="100" height="50" rx="8" ry="8" 
                fill="rgba(0,255,255,0.1)"/>
          <text x="50" y="20" text-anchor="middle" font-size="12" 
                fill="#00FFFF" font-family="Arial, Helvetica, sans-serif">
            LONGITUDE
          </text>
          <text x="50" y="40" text-anchor="middle" font-size="18" font-weight="bold" 
                fill="#FFFFFF" font-family="Arial, Helvetica, sans-serif">
            {lon:.2f}°
          </text>
        </g>
      </g>
      
      <!-- Informações -->
      <text x="260" y="450" text-anchor="middle" font-size="12" 
            fill="#FFD700" font-family="Arial, Helvetica, sans-serif">
        ⚡ Velocidade: 27.600 km/h • Altura: 408 km
      </text>
    </g>
  </g>
  
  <!-- Rodapé -->
  <text x="600" y="650" text-anchor="middle" font-size="14" 
        fill="#00FFFF" font-family="Arial, Helvetica, sans-serif">
    🔭 Dados em tempo real via NASA API • Atualizado: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}
  </text>
</svg>'''
    
    return svg

def main():
    """Ponto de entrada principal"""
    print("=" * 60)
    print("🚀 GERANDO NASA STATUS SVG (VERSÃO CORRIGIDA)")
    print("=" * 60)
    
    # Obter dados
    print("📡 CONECTANDO COM APIs...")
    apod_data = get_nasa_apod()
    iss_data = get_iss_location()
    
    print(f"✅ APOD: {'Recebido' if apod_data else 'Fallback'}")
    print(f"✅ ISS: {'Recebido' if iss_data else 'Indisponível'}")
    
    # Gerar SVG
    print("🎨 CRIANDO SVG COM BASE64...")
    svg_content = generate_nasa_svg(apod_data, iss_data)
    
    # Salvar arquivo
    os.makedirs("output", exist_ok=True)
    with open("output/nasa_status.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)
    
    print("=" * 60)
    print("✅ SVG GERADO COM SUCESSO: output/nasa_status.svg")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)