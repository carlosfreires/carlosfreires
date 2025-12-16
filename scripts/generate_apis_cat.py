"""
CAT APIs - VERSÃO FELINA PURA
2 cards horizontais: TheCatAPI + Cat Facts
"""
import requests
import random
import base64
import os
import json
from datetime import datetime, timezone
from utils import validate_api_response

def safe_get(url, params=None, timeout=10, api_name="API"):
    """Requisição HTTP segura"""
    try:
        response = requests.get(url, params=params, timeout=timeout)
        if validate_api_response(response, api_name):
            return response.json()
    except Exception as e:
        print(f"❌ {api_name}: {e}")
    return None

def get_cat_api_image():
    """Obtém imagem de gato da TheCatAPI com dados completos"""
    try:
        response = requests.get(
            "https://api.thecatapi.com/v1/images/search?has_breeds=1&limit=1",
            headers={"x-api-key": ""},  # Sem chave necessária para busca básica
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                cat = data[0]
                breeds = cat.get('breeds', [])
                breed_info = breeds[0] if breeds else {}
                
                return {
                    'url': cat['url'],
                    'width': cat.get('width', 500),
                    'height': cat.get('height', 500),
                    'breed': breed_info.get('name', 'Gato Desconhecido'),
                    'temperament': breed_info.get('temperament', 'Amigável e Curioso'),
                    'origin': breed_info.get('origin', 'Desconhecida'),
                    'life_span': breed_info.get('life_span', '12-15 anos'),
                    'weight': breed_info.get('weight', {}).get('metric', '3-6 kg'),
                    'description': breed_info.get('description', 'Gato fofo e encantador'),
                    'intelligence': breed_info.get('intelligence', 5),
                    'affection_level': breed_info.get('affection_level', 5),
                    'energy_level': breed_info.get('energy_level', 5)
                }
    except Exception as e:
        print(f"⚠️  Erro na TheCatAPI: {e}")
    
    # Fallback
    return {
        'url': 'https://cdn2.thecatapi.com/images/0XYvRd7oD.jpg',
        'breed': 'Gato Fofinho',
        'temperament': 'Brincalhão e Carinhoso',
        'origin': 'Internet',
        'life_span': '12-15 anos',
        'weight': '3-6 kg',
        'description': 'Gato adorável para alegrar seu dia',
        'intelligence': 5,
        'affection_level': 5,
        'energy_level': 5
    }

def get_cat_fact():
    """Obtém fato interessante sobre gatos"""
    try:
        response = requests.get("https://catfact.ninja/fact", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                'fact': data.get('fact', 'Gatos são animais incríveis!'),
                'length': data.get('length', 30)
            }
    except:
        pass
    
    # Fatos fallback
    facts = [
        "Gatos têm 32 músculos em cada orelha, permitindo que movam independentemente.",
        "Um gato pode saltar até 6 vezes sua altura.",
        "Gatos passam cerca de 70% de suas vidas dormindo.",
        "O ronronar de um gato tem frequência entre 25 e 150 Hz, que pode ajudar na cura óssea.",
        "Gatos têm um campo de visão de aproximadamente 200 graus.",
        "Cada gato tem um padrão único de nariz, como uma impressão digital humana.",
        "Gatos não conseguem sentir o sabor doce.",
        "Um grupo de gatos é chamado de 'clowder' em inglês.",
        "Gatos têm cerca de 100 vocalizações diferentes, enquanto cães têm apenas 10.",
        "O gato mais velho já registrado viveu 38 anos e 3 dias."
    ]
    
    fact = random.choice(facts)
    return {
        'fact': fact,
        'length': len(fact)
    }

def get_cataas_content():
    """Obtém conteúdo da CATAAS (Cat as a Service)"""
    options = [
        {"type": "image", "url": "https://cataas.com/cat", "tag": "Gato aleatório"},
        {"type": "gif", "url": "https://cataas.com/cat/gif", "tag": "GIF animado"},
        {"type": "says", "url": "https://cataas.com/cat/says/Meow%21", "tag": "Gato falante"},
        {"type": "cute", "url": "https://cataas.com/cat/cute", "tag": "Gato fofo"},
        {"type": "fat", "url": "https://cataas.com/cat/fat", "tag": "Gato gordinho"},
        {"type": "small", "url": "https://cataas.com/cat/small", "tag": "Gato pequeno"}
    ]
    
    chosen = random.choice(options)
    
    # Adicionar efeitos aleatórios
    effects = ["", "?filter=sepia", "?filter=mono", "?filter=negative", "?filter=paint", "?filter=blur"]
    effect = random.choice(effects)
    
    return {
        'url': chosen['url'] + effect,
        'type': chosen['type'],
        'tag': chosen['tag'],
        'description': f"Imagem de {chosen['tag'].lower()} via CATAAS"
    }

def get_cat_statistics():
    """Retorna estatísticas interessantes sobre gatos"""
    stats = {
        'sleep_hours': random.randint(12, 16),
        'whiskers': random.randint(12, 24),
        'heart_rate': random.randint(140, 220),
        'jump_height': random.randint(5, 8),
        'speed': random.randint(30, 48),
        'breeds_worldwide': random.randint(40, 70)
    }
    return stats

def image_to_base64(url):
    """Converte imagem para Base64"""
    try:
        response = requests.get(url, timeout=15)
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
    
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text

def generate_cat_api_card(cat_data, stats):
    """Gera SVG para TheCatAPI com dados completos"""
    
    img_base64 = image_to_base64(cat_data['url'])
    if not img_base64:
        img_base64 = get_fallback_image()
    
    breed = escape_svg(cat_data['breed'])
    temperament = escape_svg(cat_data['temperament'])
    origin = escape_svg(cat_data['origin'])
    description = escape_svg(cat_data['description'])
    life_span = cat_data['life_span']
    weight = cat_data['weight']
    
    # Calcular níveis (1-5 estrelas)
    intel_stars = "★" * cat_data['intelligence'] + "☆" * (5 - cat_data['intelligence'])
    affection_stars = "★" * cat_data['affection_level'] + "☆" * (5 - cat_data['affection_level'])
    energy_stars = "★" * cat_data['energy_level'] + "☆" * (5 - cat_data['energy_level'])
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
     width="1200" height="400" viewBox="0 0 1200 400">
  
  <defs>
    <!-- Gradiente neon roxo-laranja -->
    <linearGradient id="catCard1Bg" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#9B59B6"/>
      <stop offset="50%" stop-color="#E74C3C"/>
      <stop offset="100%" stop-color="#FF6347"/>
    </linearGradient>
    
    <!-- Gradiente para barras -->
    <linearGradient id="barGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FF6347"/>
      <stop offset="100%" stop-color="#9B59B6"/>
    </linearGradient>
    
    <!-- Filtros -->
    <filter id="catGlow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    
    <!-- Clip path -->
    <clipPath id="catImageClip1">
      <rect x="40" y="40" width="350" height="320" rx="15" ry="15"/>
    </clipPath>
    
    <!-- Padrão de patinhas -->
    <pattern id="pawPattern" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M20,10 C25,5 35,5 30,15 C25,25 15,25 10,15 C5,5 15,5 20,10" 
            fill="#FF6347" opacity="0.1"/>
    </pattern>
  </defs>
  
  <!-- Fundo -->
  <rect width="1200" height="400" fill="url(#catCard1Bg)" opacity="0.9"/>
  <rect width="1200" height="400" fill="url(#pawPattern)"/>
  
  <!-- Container principal -->
  <rect x="20" y="20" width="1160" height="360" rx="20" ry="20" 
        fill="rgba(30, 15, 30, 0.85)" stroke="#FF6347" stroke-width="3"/>
  
  <!-- Imagem do gato -->
  <g filter="url(#catGlow)" transform="translate(40, 40)">
    <rect x="0" y="0" width="350" height="320" rx="15" ry="15" 
          fill="#000000" stroke="#9B59B6" stroke-width="2"/>
    <image x="0" y="0" width="350" height="320" 
           xlink:href="{img_base64}" clip-path="url(#catImageClip1)"
           preserveAspectRatio="xMidYMid cover"/>
    
    <!-- Overlay informativo -->
    <rect x="0" y="230" width="350" height="90" rx="0" ry="0" 
          fill="rgba(0, 0, 0, 0.8)"/>
    
    <text x="175" y="260" text-anchor="middle" font-size="18" font-weight="bold"
          fill="#FFD700" font-family="Arial, Helvetica, sans-serif">
      🐱 {breed}
    </text>
    
    <text x="175" y="290" text-anchor="middle" font-size="12"
          fill="#9B59B6" font-family="Arial, Helvetica, sans-serif">
      {origin} • {life_span}
    </text>
  </g>
  
  <!-- Informações da raça -->
  <g transform="translate(420, 40)">
    <text x="0" y="40" font-size="28" font-weight="bold" 
          fill="#FFD700" font-family="Arial, Helvetica, sans-serif">
      🎯 THE CAT API
    </text>
    
    <text x="0" y="80" font-size="24" font-weight="bold" 
          fill="#FFFFFF" font-family="Arial, Helvetica, sans-serif">
      {breed}
    </text>
    
    <!-- Temperamento -->
    <g transform="translate(0, 120)">
      <text x="0" y="0" font-size="16" fill="#FF6347" font-family="Arial">
        🧠 Temperamento:
      </text>
      <foreignObject x="0" y="20" width="350" height="40">
        <div xmlns="http://www.w3.org/1999/xhtml" 
             style="color:#FFFFFF; font-size:14px; font-family:Arial,sans-serif; 
                    line-height:1.4;">
          {temperament}
        </div>
      </foreignObject>
    </g>
    
    <!-- Descrição -->
    <g transform="translate(0, 180)">
      <text x="0" y="0" font-size="16" fill="#9B59B6" font-family="Arial">
        📝 Descrição:
      </text>
      <foreignObject x="0" y="20" width="350" height="60">
        <div xmlns="http://www.w3.org/1999/xhtml" 
             style="color:#E0E0E0; font-size:13px; font-family:Arial,sans-serif; 
                    line-height:1.4;">
          {description}
        </div>
      </foreignObject>
    </g>
  </g>
  
  <!-- Estatísticas -->
  <g transform="translate(800, 40)">
    <rect x="0" y="0" width="340" height="320" rx="15" ry="15" 
          fill="rgba(255, 99, 71, 0.1)" stroke="#9B59B6" stroke-width="1"/>
    
    <text x="170" y="30" text-anchor="middle" font-size="20" font-weight="bold"
          fill="#FFD700" font-family="Arial, Helvetica, sans-serif">
      📊 ESTATÍSTICAS
    </text>
    
    <g transform="translate(30, 70)">
      <!-- Inteligência -->
      <text x="0" y="0" font-size="14" fill="#FFFFFF" font-family="Arial">
        🧠 Inteligência:
      </text>
      <text x="120" y="0" font-size="14" fill="#FFD700" font-family="Arial">
        {intel_stars}
      </text>
      
      <!-- Nível de Afeto -->
      <text x="0" y="30" font-size="14" fill="#FFFFFF" font-family="Arial">
        ❤️ Afeição:
      </text>
      <text x="120" y="30" font-size="14" fill="#FFD700" font-family="Arial">
        {affection_stars}
      </text>
      
      <!-- Nível de Energia -->
      <text x="0" y="60" font-size="14" fill="#FFFFFF" font-family="Arial">
        ⚡ Energia:
      </text>
      <text x="120" y="60" font-size="14" fill="#FFD700" font-family="Arial">
        {energy_stars}
      </text>
      
      <!-- Peso -->
      <text x="0" y="90" font-size="14" fill="#FFFFFF" font-family="Arial">
        ⚖️ Peso:
      </text>
      <text x="120" y="90" font-size="14" fill="#9B59B6" font-family="Arial">
        {weight}
      </text>
      
      <!-- Expectativa de vida -->
      <text x="0" y="120" font-size="14" fill="#FFFFFF" font-family="Arial">
        📅 Vida útil:
      </text>
      <text x="120" y="120" font-size="14" fill="#9B59B6" font-family="Arial">
        {life_span}
      </text>
    </g>
    
    <!-- Dados gerais -->
    <g transform="translate(30, 200)">
      <rect x="0" y="0" width="280" height="80" rx="10" ry="10" 
            fill="rgba(155, 89, 182, 0.2)"/>
      
      <text x="140" y="25" text-anchor="middle" font-size="12" 
            fill="#FFD700" font-family="Arial">
        🐾 DADOS GERAIS
      </text>
      
      <text x="140" y="45" text-anchor="middle" font-size="11" 
            fill="#FFFFFF" font-family="Arial">
        Sono: {stats['sleep_hours']}h/dia • Bigodes: {stats['whiskers']}
      </text>
      
      <text x="140" y="65" text-anchor="middle" font-size="11" 
            fill="#FFFFFF" font-family="Arial">
        Frequência cardíaca: {stats['heart_rate']} bpm
      </text>
    </g>
  </g>
  
  <!-- Elementos decorativos -->
  <!-- Patinhas -->
  <g transform="translate(1150, 50)">
    <circle cx="0" cy="0" r="8" fill="#FF6347" opacity="0.6">
      <animate attributeName="r" values="8;10;8" dur="2s" repeatCount="indefinite"/>
    </circle>
    <circle cx="15" cy="10" r="6" fill="#9B59B6" opacity="0.6">
      <animate attributeName="opacity" values="0.4;0.8;0.4" dur="3s" repeatCount="indefinite"/>
    </circle>
  </g>
  
  <!-- Rodapé -->
  <text x="600" y="390" text-anchor="middle" font-size="12" 
        fill="#FFD700" font-family="Arial, Helvetica, sans-serif">
    🐱 TheCatAPI • Dados reais de raças felinas • Atualizado: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}
  </text>
</svg>'''
    
    return svg

def generate_cataas_card(cataas_data, cat_fact, stats):
    """Gera SVG para CATAAS + Cat Facts"""
    
    img_base64 = image_to_base64(cataas_data['url'])
    if not img_base64:
        img_base64 = get_fallback_image()
    
    fact = escape_svg(cat_fact['fact'])
    fact_length = cat_fact['length']
    cataas_type = cataas_data['type']
    cataas_tag = cataas_data['tag']
    
    # Gerar fatos adicionais
    additional_facts = [
        f"🏃 Velocidade máxima: {stats['speed']} km/h",
        f"🦘 Salto vertical: {stats['jump_height']}x sua altura",
        f"🌍 Raças no mundo: {stats['breeds_worldwide']}+",
        f"💤 Dorme {stats['sleep_hours']} horas por dia",
        f"📏 {stats['whiskers']} bigodes ultra-sensíveis",
        f"💗 {stats['heart_rate']} batimentos por minuto"
    ]
    
    # Selecionar 3 fatos aleatórios
    selected_facts = random.sample(additional_facts, 3)
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
     width="1200" height="400" viewBox="0 0 1200 400">
  
  <defs>
    <!-- Gradiente neon invertido -->
    <linearGradient id="catCard2Bg" x1="100%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FF6347"/>
      <stop offset="50%" stop-color="#E74C3C"/>
      <stop offset="100%" stop-color="#9B59B6"/>
    </linearGradient>
    
    <!-- Gradiente para texto -->
    <linearGradient id="textGlow" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFD700"/>
      <stop offset="100%" stop-color="#FF6347"/>
    </linearGradient>
    
    <!-- Padrão felino -->
    <pattern id="whiskerPattern" x="0" y="0" width="50" height="50" patternUnits="userSpaceOnUse">
      <line x1="25" y1="0" x2="25" y2="50" stroke="#FF6347" stroke-width="1" opacity="0.2"/>
      <line x1="0" y1="25" x2="50" y2="25" stroke="#9B59B6" stroke-width="1" opacity="0.2"/>
    </pattern>
    
    <!-- Filtro de brilho -->
    <filter id="brightGlow">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    
    <!-- Clip path -->
    <clipPath id="catImageClip2">
      <rect x="40" y="40" width="350" height="320" rx="15" ry="15"/>
    </clipPath>
  </defs>
  
  <!-- Fundo -->
  <rect width="1200" height="400" fill="url(#catCard2Bg)" opacity="0.9"/>
  <rect width="1200" height="400" fill="url(#whiskerPattern)"/>
  
  <!-- Container principal -->
  <rect x="20" y="20" width="1160" height="360" rx="20" ry="20" 
        fill="rgba(40, 20, 40, 0.85)" stroke="#9B59B6" stroke-width="3"/>
  
  <!-- Imagem CATAAS -->
  <g filter="url(#brightGlow)" transform="translate(40, 40)">
    <rect x="0" y="0" width="350" height="320" rx="15" ry="15" 
          fill="#000000" stroke="#FF6347" stroke-width="2"/>
    <image x="0" y="0" width="350" height="320" 
           xlink:href="{img_base64}" clip-path="url(#catImageClip2)"
           preserveAspectRatio="xMidYMid cover"/>
    
    <!-- Badge do tipo -->
    <rect x="280" y="20" width="60" height="30" rx="8" ry="8" 
          fill="#FF6347" opacity="0.9"/>
    <text x="310" y="40" text-anchor="middle" font-size="12" 
          fill="#FFFFFF" font-weight="bold" font-family="Arial">
      {cataas_type.upper()}
    </text>
    
    <!-- Tag -->
    <rect x="10" y="270" width="130" height="40" rx="8" ry="8" 
          fill="rgba(0, 0, 0, 0.7)"/>
    <text x="75" y="295" text-anchor="middle" font-size="14" 
          fill="#FFD700" font-family="Arial">
      {cataas_tag}
    </text>
  </g>
  
  <!-- Seção de fatos -->
  <g transform="translate(420, 40)">
    <text x="0" y="40" font-size="28" font-weight="bold" 
          fill="url(#textGlow)" font-family="Arial, Helvetica, sans-serif">
      🐾 CATAAS + CAT FACTS
    </text>
    
    <text x="0" y="85" font-size="24" font-weight="bold" 
          fill="#FFFFFF" font-family="Arial, Helvetica, sans-serif">
      Fatos Incríveis Sobre Gatos
    </text>
    
    <!-- Fato principal -->
    <g transform="translate(0, 130)">
      <rect x="0" y="0" width="360" height="120" rx="15" ry="15" 
            fill="rgba(255, 215, 0, 0.1)" stroke="#FF6347" stroke-width="2"/>
      
      <text x="180" y="30" text-anchor="middle" font-size="18" font-weight="bold"
            fill="#FFD700" font-family="Arial, Helvetica, sans-serif">
        🧠 FATO FELINO #{random.randint(100, 999)}
      </text>
      
      <foreignObject x="20" y="50" width="320" height="60">
        <div xmlns="http://www.w3.org/1999/xhtml" 
             style="color:#FFFFFF; font-size:16px; font-family:Arial,sans-serif; 
                    line-height:1.4; text-align:center; font-style:italic;">
          "{fact}"
        </div>
      </foreignObject>
      
      <text x="180" y="115" text-anchor="middle" font-size="12"
            fill="#9B59B6" font-family="Arial, Helvetica, sans-serif">
        📏 {fact_length} caracteres • Fonte: Cat Fact Ninja
      </text>
    </g>
  </g>
  
  <!-- Fatos rápidos -->
  <g transform="translate(800, 40)">
    <rect x="0" y="0" width="340" height="320" rx="15" ry="15" 
          fill="rgba(155, 89, 182, 0.15)" stroke="#FF6347" stroke-width="1"/>
    
    <text x="170" y="30" text-anchor="middle" font-size="22" font-weight="bold"
          fill="#FFD700" font-family="Arial, Helvetica, sans-serif">
      ⚡ FATOS RÁPIDOS
    </text>
    
    <g transform="translate(30, 70)">
      <!-- Fato 1 -->
      <rect x="0" y="0" width="280" height="40" rx="8" ry="8" 
            fill="rgba(255, 99, 71, 0.2)"/>
      <text x="20" y="25" font-size="14" fill="#FFFFFF" font-family="Arial">
        {selected_facts[0]}
      </text>
      
      <!-- Fato 2 -->
      <rect x="0" y="60" width="280" height="40" rx="8" ry="8" 
            fill="rgba(155, 89, 182, 0.2)"/>
      <text x="20" y="85" font-size="14" fill="#FFFFFF" font-family="Arial">
        {selected_facts[1]}
      </text>
      
      <!-- Fato 3 -->
      <rect x="0" y="120" width="280" height="40" rx="8" ry="8" 
            fill="rgba(255, 215, 0, 0.2)"/>
      <text x="20" y="145" font-size="14" fill="#FFFFFF" font-family="Arial">
        {selected_facts[2]}
      </text>
    </g>
    
    <!-- API Info -->
    <g transform="translate(30, 220)">
      <rect x="0" y="0" width="280" height="80" rx="10" ry="10" 
            fill="rgba(30, 30, 30, 0.6)"/>
      
      <text x="140" y="25" text-anchor="middle" font-size="14" font-weight="bold"
            fill="#FF6347" font-family="Arial, Helvetica, sans-serif">
        🌐 APIS UTILIZADAS
      </text>
      
      <text x="140" y="50" text-anchor="middle" font-size="12"
            fill="#FFFFFF" font-family="Arial, Helvetica, sans-serif">
        CATAAS • Cat Fact Ninja
      </text>
    </g>
  </g>
  
  <!-- Elementos decorativos -->
  <!-- Bigodes -->
  <g transform="translate(1150, 200)">
    <line x1="-20" y1="0" x2="20" y2="0" stroke="#FFD700" stroke-width="2" opacity="0.5">
      <animate attributeName="x2" values="20;25;20" dur="3s" repeatCount="indefinite"/>
    </line>
    <line x1="-20" y1="-10" x2="20" y2="-10" stroke="#FF6347" stroke-width="2" opacity="0.5">
      <animate attributeName="x2" values="20;22;20" dur="2.5s" repeatCount="indefinite"/>
    </line>
    <line x1="-20" y1="10" x2="20" y2="10" stroke="#9B59B6" stroke-width="2" opacity="0.5">
      <animate attributeName="x2" values="20;23;20" dur="2.8s" repeatCount="indefinite"/>
    </line>
  </g>
  
  <!-- Rodapé -->
  <text x="600" y="390" text-anchor="middle" font-size="12" 
        fill="#FFD700" font-family="Arial, Helvetica, sans-serif">
    🐾 CATAAS + Cat Facts • Conteúdo felino em tempo real • Atualizado: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}
  </text>
</svg>'''
    
    return svg

def main():
    """Ponto de entrada principal"""
    print("=" * 60)
    print("😺 CAT APIS - 2 CARDS HORIZONTAIS FELINOS")
    print("=" * 60)
    
    # Criar pasta de output
    os.makedirs("output", exist_ok=True)
    
    # 1. Buscar dados para Card 1 (TheCatAPI)
    print("\n📡 BUSCANDO DADOS DO CAT API...")
    cat_data = get_cat_api_image()
    print(f"✅ Raça: {cat_data['breed']} ({cat_data['origin']})")
    
    # 2. Buscar dados para Card 2 (CATAAS + Cat Facts)
    print("📡 BUSCANDO DADOS CATAAS E FATOS...")
    cataas_data = get_cataas_content()
    cat_fact = get_cat_fact()
    print(f"✅ CATAAS: {cataas_data['tag']}")
    print(f"✅ Fato: {cat_fact['fact'][:50]}...")
    
    # 3. Estatísticas gerais
    stats = get_cat_statistics()
    
    # 4. Gerar SVGs
    print("\n🎨 CRIANDO SVGs HORIZONTAIS...")
    
    # Card 1: TheCatAPI
    card1_svg = generate_cat_api_card(cat_data, stats)
    with open("output/cat_api_card.svg", "w", encoding="utf-8") as f:
        f.write(card1_svg)
    print("🖼️  SVG Card 1 (TheCatAPI) gerado")
    
    # Card 2: CATAAS + Cat Facts
    card2_svg = generate_cataas_card(cataas_data, cat_fact, stats)
    with open("output/cataas_card.svg", "w", encoding="utf-8") as f:
        f.write(card2_svg)
    print("🖼️  SVG Card 2 (CATAAS + Cat Facts) gerado")
    
    # 5. Gerar markdown para README
    print("\n📄 GERANDO MARKDOWN PARA README...")
    md_content = f"""<!-- CATS_HORIZONTAL_SECTION -->
<!-- Atualizado: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} -->

## 😻 MOMENTO FELINO - APIs Reais

<div align="center">

### 🐱 TheCatAPI - Raças Felinas
[![TheCatAPI](output/cat_api_card.svg)](https://thecatapi.com)
*Imagem aleatória com dados completos da raça*

---

### 🐾 CATAAS + Cat Facts
[![CATAAS](output/cataas_card.svg)](https://cataas.com)
*Imagens + fatos interessantes sobre gatos*

<br>

<sub>🎨 Design com gradiente neon #9B59B6 → #FF6347</sub>
<sub>🔄 Atualizado automaticamente a cada 6 horas</sub>
<sub>📡 Dados em tempo real via APIs felinas</sub>

</div>

<!-- END_CATS_HORIZONTAL_SECTION -->
"""
    
    with open("output/cats_section.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    
    print("=" * 60)
    print("✅ 2 CARDS FELINOS GERADOS COM SUCESSO!")
    print("📁 output/cat_api_card.svg")
    print("📁 output/cataas_card.svg")
    print("📁 output/cats_section.md")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)