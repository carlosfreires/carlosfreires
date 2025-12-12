"""
NASA APIs - VERSÃO 1.0
Script exclusivo para APIs da NASA
Atualiza apenas a seção espacial do README
"""
import requests
import os
from utils import read_readme, write_readme, update_section, log_success, validate_api_response

# Configuração
NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")  # DEMO_KEY tem limites

def safe_get(url, params=None, timeout=10, api_name="API"):
    """
    Requisição HTTP segura com tratamento de erros
    """
    try:
        response = requests.get(url, params=params, timeout=timeout)
        if validate_api_response(response, api_name):
            return response.json()
    except requests.exceptions.Timeout:
        print(f"⏱️  {api_name}: Timeout após {timeout}s")
    except Exception as e:
        print(f"❌ {api_name}: Erro - {e}")
    return None

def get_nasa_apod():
    """Obtém Astronomy Picture of the Day"""
    url = f"https://api.nasa.gov/planetary/apod"
    params = {"api_key": NASA_API_KEY, "thumbs": "True"}
    return safe_get(url, params, api_name="NASA APOD")

def get_iss_location():
    """Localização da Estação Espacial"""
    url = "http://api.open-notify.org/iss-now.json"
    return safe_get(url, timeout=5, api_name="ISS Location")

def generate_nasa_html(apod_data, iss_data):
    """
    Gera HTML da seção NASA
    Args:
        apod_data (dict): Dados da APOD
        iss_data (dict): Dados da ISS
    Retorna: str - HTML da seção
    """
    # Dados padrão para fallback
    default_apod = {
        'title': 'Universo em Foco',
        'url': 'https://apod.nasa.gov/apod/image/2401/aurora_jin_960.jpg',
        'explanation': 'Explore o cosmos com imagens diárias da NASA.',
        'date': '2024-01-01'
    }
    
    apod = apod_data or default_apod
    has_iss = iss_data and 'iss_position' in iss_data
    
    html = f'''{log_success("NASA")}

<!-- ========================================================= -->
<!-- =================  EXPLORAÇÃO ESPACIAL  ================== -->
<!-- ========================================================= -->
<div style="margin: 60px auto; padding: 30px; max-width: 1200px; 
            background: linear-gradient(135deg, rgba(26,13,39,0.95), rgba(42,0,71,0.95));
            border-radius: 20px; box-shadow: 0 10px 40px rgba(148,0,211,0.4);
            border: 1px solid #8A2BE2;">

<h2 style="text-align: center; font-size: 36px; margin-bottom: 40px; 
           background: linear-gradient(45deg, #FF416C, #FF4B2B, #8A2BE2);
           -webkit-background-clip: text; -webkit-text-fill-color: transparent;
           text-shadow: 0 0 30px rgba(255,65,108,0.3);">
  🚀 EXPLORAÇÃO COSMOS &nbsp; • &nbsp; 🌌 NASA APIs
</h2>

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 30px;">
'''
    
    # Card APOD
    html += f'''
  <div style="background: rgba(0,0,0,0.7); padding: 25px; border-radius: 15px; 
              border: 2px solid #8A2BE2; box-shadow: 0 5px 20px rgba(138,43,226,0.3);">
    <h3 style="color: #FF6347; text-align: center; font-size: 22px; margin: 0 0 20px 0;">
      <span style="color: #FF6347;">📷</span> IMAGEM ASTRONÔMICA DO DIA
    </h3>
    <a href="{apod['url']}" target="_blank" style="display: block; text-decoration: none;">
      <div style="width: 100%; height: 200px; border-radius: 10px; border: 2px solid #FF6347;
                  overflow: hidden; background: #000; display: flex; align-items: center; justify-content: center;">
        <img src="{apod['url']}" alt="{apod['title']}" 
             style="max-width: 100%; max-height: 100%; object-fit: cover;">
      </div>
    </a>
    <div style="margin-top: 15px;">
      <h4 style="color: #00FFFF; font-size: 18px; margin: 10px 0;">{apod['title']}</h4>
      <p style="color: #9B59B6; font-size: 14px; line-height: 1.5; margin: 10px 0;">
        {apod['explanation'][:180]}...
      </p>
      <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px;">
        <span style="color: #FFD700; font-size: 12px;">📅 {apod.get('date', 'Data indisponível')}</span>
        <a href="https://apod.nasa.gov/apod/astropix.html" target="_blank" 
           style="color: #FF6347; text-decoration: none; font-size: 12px;">
          🌐 Ver no site da NASA
        </a>
      </div>
    </div>
  </div>
'''
    
    # Card ISS
    if has_iss:
        lat = float(iss_data['iss_position']['latitude'])
        lon = float(iss_data['iss_position']['longitude'])
        
        html += f'''
  <div style="background: rgba(0,0,0,0.7); padding: 25px; border-radius: 15px; 
              border: 2px solid #00FFFF; box-shadow: 0 5px 20px rgba(0,255,255,0.3);">
    <h3 style="color: #00FFFF; text-align: center; font-size: 22px; margin: 0 0 20px 0;">
      <span style="color: #00FFFF;">🛰️</span> ESTAÇÃO ESPACIAL INTERNACIONAL
    </h3>
    <div style="text-align: center;">
      <div style="position: relative; width: 200px; height: 200px; margin: 0 auto 20px; 
                  background: radial-gradient(circle at center, rgba(0,255,255,0.1) 0%, transparent 70%);
                  border: 2px dashed #00FFFF; border-radius: 50%;">
        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
                    width: 20px; height: 20px; background: #FF6347; border-radius: 50%;
                    box-shadow: 0 0 20px #FF6347;">
        </div>
      </div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 20px 0;">
        <div style="background: rgba(0,255,255,0.1); padding: 10px; border-radius: 8px;">
          <div style="color: #00FFFF; font-size: 12px; margin-bottom: 5px;">LATITUDE</div>
          <div style="color: #FFFFFF; font-size: 18px; font-weight: bold;">{lat:.2f}°</div>
        </div>
        <div style="background: rgba(0,255,255,0.1); padding: 10px; border-radius: 8px;">
          <div style="color: #00FFFF; font-size: 12px; margin-bottom: 5px;">LONGITUDE</div>
          <div style="color: #FFFFFF; font-size: 18px; font-weight: bold;">{lon:.2f}°</div>
        </div>
      </div>
      <div style="color: #FFD700; font-size: 12px; margin-top: 15px;">
        ⚡ Velocidade: 27.600 km/h • Altura: 408 km
      </div>
    </div>
  </div>
'''
    else:
        html += f'''
  <div style="background: rgba(0,0,0,0.7); padding: 25px; border-radius: 15px; 
              border: 2px solid #00FFFF; box-shadow: 0 5px 20px rgba(0,255,255,0.3);
              display: flex; align-items: center; justify-content: center;">
    <div style="text-align: center;">
      <div style="font-size: 48px; color: #00FFFF; margin-bottom: 15px;">🛰️</div>
      <p style="color: #9B59B6; font-size: 14px;">Dados da ISS temporariamente indisponíveis</p>
      <p style="color: #FFD700; font-size: 12px;">Tentando reconexão automática...</p>
    </div>
  </div>
'''
    
    html += '''
</div>

<div style="margin-top: 30px; padding: 15px; background: rgba(138,43,226,0.1); 
            border-radius: 10px; border-left: 4px solid #8A2BE2;">
  <p style="color: #00FFFF; text-align: center; margin: 0; font-size: 14px;">
    🔭 Dados em tempo real via NASA API • Atualização automática diária
  </p>
</div>
</div>
'''
    
    return html

def main():
    """PONTO DE ENTRADA DO SCRIPT"""
    print("=" * 60)
    print("🚀 INICIANDO ATUALIZAÇÃO NASA APIs")
    print("=" * 60)
    
    # 1. Ler README atual
    content = read_readme()
    if not content:
        print("❌ ABORTADO: Não foi possível ler README.md")
        return False
    
    # 2. Obter dados das APIs
    print("📡 CONECTANDO COM APIs ESPACIAIS...")
    apod_data = get_nasa_apod()
    iss_data = get_iss_location()
    
    print(f"✅ APOD: {'Recebido' if apod_data else 'Usando fallback'}")
    print(f"✅ ISS: {'Recebido' if iss_data else 'Indisponível'}")
    
    # 3. Gerar HTML
    print("🎨 GERANDO CONTEÚDO HTML...")
    nasa_html = generate_nasa_html(apod_data, iss_data)
    
    # 4. Atualizar seção no README
    print("📝 ATUALIZANDO SEÇÃO NASA...")
    new_content = update_section(
        content,
        "<!-- BEGIN NASA_APIS -->",
        "<!-- END NASA_APIS -->",
        nasa_html
    )
    
    # 5. Escrever novo README
    if write_readme(new_content):
        print("=" * 60)
        print("✅ NASA APIs ATUALIZADAS COM SUCESSO!")
        print("=" * 60)
        return True
    else:
        print("❌ FALHA AO ATUALIZAR README")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)