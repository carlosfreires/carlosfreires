"""
TECH NEWS APIs - VERSÃO 1.0
Script exclusivo para notícias de tecnologia
Atualiza apenas a seção de notícias do README
"""
import requests
import os
import random
from utils import read_readme, write_readme, update_section, log_success, validate_api_response

def safe_get(url, headers=None, timeout=10, api_name="API"):
    """Requisição HTTP segura"""
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        if validate_api_response(response, api_name):
            return response.json()
    except Exception as e:
        print(f"⚠️  {api_name}: {e}")
    return None

def get_tech_news():
    """Obtém notícias de tecnologia"""
    # Fallback: notícias curadas
    fallback_news = [
        {
            "title": "Inteligência Artificial Revoluciona Desenvolvimento",
            "description": "Ferramentas de IA estão transformando como escrevemos e debugamos código.",
            "category": "🤖 IA",
            "read_time": "3 min"
        },
        {
            "title": "Open Source Atinge Novo Recorde em 2024",
            "description": "Comunidade open source cresce com colaboração global sem precedentes.",
            "category": "🔓 OPEN SOURCE",
            "read_time": "4 min"
        },
        {
            "title": "JavaScript Domina Desenvolvimento Web Moderno",
            "description": "Ecossistema JavaScript expande com novas frameworks e ferramentas.",
            "category": "⚡ JAVASCRIPT",
            "read_time": "5 min"
        },
        {
            "title": "Python Lidera em Data Science & Machine Learning",
            "description": "Python se consolida como linguagem preferida para IA e análise de dados.",
            "category": "🐍 PYTHON",
            "read_time": "4 min"
        },
        {
            "title": "DevOps e Containers Transformam Infraestrutura",
            "description": "Docker e Kubernetes revolucionam deployment de aplicações em escala.",
            "category": "🐳 DEVOPS",
            "read_time": "6 min"
        }
    ]
    
    # Tentar API externa (NewsAPI)
    news_api_key = os.getenv("NEWS_API_KEY")
    if news_api_key:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "category": "technology",
            "language": "en",
            "pageSize": 5,
            "apiKey": news_api_key
        }
        data = safe_get(url, params=params, api_name="NewsAPI")
        
        if data and "articles" in data:
            articles = data["articles"]
            if articles:
                return [
                    {
                        "title": a.get("title", "Notícia Tech").replace(" - Reuters", "").replace(" - BBC News", "")[:80],
                        "description": a.get("description", "Leia mais sobre tecnologia.")[:120],
                        "category": random.choice(["🤖 IA", "⚡ TECH", "🔬 CIÊNCIA", "💻 DEV"]),
                        "read_time": f"{random.randint(2, 8)} min"
                    }
                    for a in articles[:5]
                ]
    
    return fallback_news

def generate_news_html(news_items):
    """Gera HTML da seção de notícias"""
    colors = ["#FF6347", "#00FFFF", "#FFD700", "#9B59B6", "#4169E1"]
    icons = ["🚀", "💡", "⚡", "🔬", "🌐"]
    
    html = f'''{log_success("NOTÍCIAS TECH")}

<!-- ========================================================= -->
<!-- ================  NOTÍCIAS DE TECNOLOGIA  ================ -->
<!-- ========================================================= -->
<div style="margin: 60px auto; padding: 30px; max-width: 1200px;
            background: linear-gradient(135deg, rgba(13,26,39,0.95), rgba(0,42,71,0.95));
            border-radius: 20px; box-shadow: 0 10px 40px rgba(0,148,211,0.4);
            border: 1px solid #00FFFF;">

<h2 style="text-align: center; font-size: 36px; margin-bottom: 40px;
           background: linear-gradient(45deg, #00FFFF, #4169E1, #8A2BE2);
           -webkit-background-clip: text; -webkit-text-fill-color: transparent;
           text-shadow: 0 0 30px rgba(0,255,255,0.3);">
  💻 TECH NEWS &nbsp; • &nbsp; 🔬 INOVAÇÃO DIGITAL
</h2>

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 25px;">
'''
    
    for i, news in enumerate(news_items):
        color = colors[i % len(colors)]
        icon = icons[i % len(icons)]
        
        html += f'''
  <div style="background: rgba(255,255,255,0.05); padding: 25px; border-radius: 15px;
              border: 1px solid {color}; transition: all 0.3s ease;
              position: relative; overflow: hidden;">
    
    <div style="position: absolute; top: 0; right: 0; width: 60px; height: 60px;
                background: {color}20; border-bottom-left-radius: 15px;
                display: flex; align-items: center; justify-content: center;">
      <span style="font-size: 24px;">{icon}</span>
    </div>
    
    <div style="margin-bottom: 15px;">
      <span style="background: {color}; color: white; padding: 4px 12px;
             border-radius: 20px; font-size: 12px; font-weight: bold;">
        {news['category']}
      </span>
      <span style="color: #FFD700; font-size: 12px; margin-left: 10px;">
        ⏱️ {news['read_time']}
      </span>
    </div>
    
    <h3 style="color: {color}; font-size: 18px; margin: 10px 0; line-height: 1.4;">
      {news['title']}
    </h3>
    
    <p style="color: #9B59B6; font-size: 14px; line-height: 1.5; margin: 15px 0;">
      {news['description']}
    </p>
    
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 20px;">
      <span style="color: #00FFFF; font-size: 12px;">
        📅 Hoje • 🔥 Trending
      </span>
      <button style="background: {color}; color: white; border: none; padding: 8px 16px;
              border-radius: 8px; font-size: 12px; cursor: pointer; transition: opacity 0.3s;"
              onmouseover="this.style.opacity='0.8'" onmouseout="this.style.opacity='1'">
        📖 Ler Artigo
      </button>
    </div>
    
    <div style="position: absolute; bottom: 0; left: 0; width: 100%; height: 3px;
                background: linear-gradient(90deg, {color}, transparent);">
    </div>
  </div>
'''
    
    html += '''
</div>

<div style="margin-top: 40px; padding: 20px; background: rgba(0,255,255,0.1); 
            border-radius: 12px; border-left: 4px solid #00FFFF;">
  <div style="display: flex; align-items: center; justify-content: center; gap: 15px;">
    <div style="font-size: 24px;">📡</div>
    <div>
      <p style="color: #00FFFF; margin: 0; font-size: 16px; font-weight: bold;">
        MANTENHA-SE ATUALIZADO
      </p>
      <p style="color: #9B59B6; margin: 5px 0 0 0; font-size: 14px;">
        O mundo da tecnologia evolui rápido. Estas são as tendências do momento.
      </p>
    </div>
  </div>
</div>

</div>
'''
    
    return html

def main():
    """PONTO DE ENTRADA DO SCRIPT"""
    print("=" * 60)
    print("📰 INICIANDO ATUALIZAÇÃO TECH NEWS")
    print("=" * 60)
    
    # 1. Ler README
    content = read_readme()
    if not content:
        print("❌ ABORTADO: Não foi possível ler README.md")
        return False
    
    # 2. Obter notícias
    print("📡 BUSCANDO NOTÍCIAS RECENTES...")
    news_items = get_tech_news()
    print(f"✅ {len(news_items)} NOTÍCIAS ENCONTRADAS")
    
    # 3. Gerar HTML
    print("🎨 CRIANDO LAYOUT DE NOTÍCIAS...")
    news_html = generate_news_html(news_items)
    
    # 4. Atualizar seção
    print("📝 ATUALIZANDO SEÇÃO NEWS...")
    new_content = update_section(
        content,
        "<!-- BEGIN NEWS_APIS -->",
        "<!-- END NEWS_APIS -->",
        news_html
    )
    
    # 5. Salvar README
    if write_readme(new_content):
        print("=" * 60)
        print("✅ TECH NEWS ATUALIZADAS COM SUCESSO!")
        print("=" * 60)
        return True
    else:
        print("❌ FALHA AO ATUALIZAR README")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)