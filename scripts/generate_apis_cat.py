"""
CAT APIs - VERSÃO 1.0
Script exclusivo para API de gatos e citações
Atualiza apenas a seção felina do README
"""
import requests
import random
from utils import read_readme, write_readme, update_section, log_success

def get_cat_image():
    """Obtém imagem aleatória de gato com fallback"""
    try:
        response = requests.get("https://api.thecatapi.com/v1/images/search", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                return data[0]['url']
    except:
        pass
    
    # Fallback para imagens estáticas
    fallback_images = [
        "https://cataas.com/cat",
        "https://cataas.com/cat/gif",
        "https://cataas.com/cat/says/hello"
    ]
    return random.choice(fallback_images)

def get_developer_quote():
    """Retorna citação inspiradora para devs"""
    quotes = [
        {
            "text": "Primeiro, resolva o problema. Então, escreva o código.",
            "author": "John Johnson",
            "category": "💡 SABEDORIA DEV"
        },
        {
            "text": "Qualquer código seu que você não revisou em 6 meses pode muito bem ter sido escrito por outra pessoa.",
            "author": "Lei de Eagleson",
            "category": "🔄 REFATORAÇÃO"
        },
        {
            "text": "Programar não é sobre digitar, é sobre pensar.",
            "author": "Rich Hickey",
            "category": "🧠 PENSAMENTO"
        },
        {
            "text": "O código é poesia que os computadores entendem.",
            "author": "Dev Anônimo",
            "category": "🎨 ARTE DO CÓDIGO"
        },
        {
            "text": "Um gato sempre sabe o que quer. Um desenvolvedor também deveria.",
            "author": "Cat Lover Dev",
            "category": "😺 INSPIRAÇÃO FELINA"
        },
        {
            "text": "O sucesso é a soma de pequenos esforços repetidos dia após dia.",
            "author": "Robert Collier",
            "category": "🚀 PERSEVERANÇA"
        },
        {
            "text": "O melhor código é código escrito para humanos, não para máquinas.",
            "author": "Dev Sábio",
            "category": "👥 COLABORAÇÃO"
        }
    ]
    return random.choice(quotes)

def generate_cat_html(cat_image, quote):
    """Gera HTML da seção felina"""
    html = f'''{log_success("GATO DO DIA")}

<!-- ========================================================= -->
<!-- ==================  MOMENTO FELINO  ====================== -->
<!-- ========================================================= -->
<div style="margin: 60px auto; padding: 40px; max-width: 1200px;
            background: linear-gradient(135deg, rgba(39,26,13,0.95), rgba(71,42,0,0.95));
            border-radius: 20px; box-shadow: 0 10px 40px rgba(255,165,0,0.4);
            border: 1px solid #FFD700; position: relative; overflow: hidden;">
  
  <!-- Elementos decorativos -->
  <div style="position: absolute; top: -100px; right: -100px; width: 300px; height: 300px;
              background: radial-gradient(circle, rgba(255,215,0,0.15) 0%, transparent 70%);
              border-radius: 50%;"></div>
  <div style="position: absolute; bottom: -100px; left: -100px; width: 250px; height: 250px;
              background: radial-gradient(circle, rgba(255,99,71,0.15) 0%, transparent 70%);
              border-radius: 50%;"></div>

  <h2 style="text-align: center; font-size: 36px; margin-bottom: 40px;
             background: linear-gradient(45deg, #FFD700, #FF6347, #FFA500);
             -webkit-background-clip: text; -webkit-text-fill-color: transparent;
             text-shadow: 0 0 30px rgba(255,215,0,0.3);">
    😻 MOMENTO FELINO &nbsp; • &nbsp; ✨ PAUSA INSPIRADORA
  </h2>

  <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 40px;">
    
    <!-- Card da Imagem -->
    <div style="flex: 1; min-width: 300px; max-width: 450px;">
      <div style="background: rgba(255,255,255,0.08); padding: 20px; border-radius: 20px;
                  border: 3px solid #FF6347; box-shadow: 0 10px 30px rgba(255,99,71,0.2);">
        
        <div style="position: relative; width: 100%; padding-bottom: 75%; border-radius: 15px;
                    overflow: hidden; background: #000;">
          <img src="{cat_image}" alt="Gato Inspirador" 
               style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;
                      object-fit: cover; transition: transform 0.5s ease;"
               onmouseover="this.style.transform='scale(1.05)'"
               onmouseout="this.style.transform='scale(1)'">
        </div>
        
        <div style="display: flex; justify-content: center; gap: 20px; margin: 20px 0;">
          <span style="color: #FFD700; font-size: 14px; display: flex; align-items: center; gap: 5px;">
            🐾 <span style="color: #FFFFFF;">Fofura Garantida</span>
          </span>
          <span style="color: #FF6347; font-size: 14px; display: flex; align-items: center; gap: 5px;">
            😸 <span style="color: #FFFFFF;">Anti-stress</span>
          </span>
          <span style="color: #9B59B6; font-size: 14px; display: flex; align-items: center; gap: 5px;">
            💡 <span style="color: #FFFFFF;">Inspiração</span>
          </span>
        </div>
        
        <div style="text-align: center; padding: 15px; background: rgba(255,215,0,0.1);
                    border-radius: 10px; margin-top: 10px;">
          <p style="color: #FFD700; margin: 0; font-size: 14px; font-style: italic;">
            "Um gato olhando fixamente para a tela pode ser um desenvolvedor em outra vida."
          </p>
        </div>
      </div>
    </div>
    
    <!-- Card da Citação -->
    <div style="flex: 1; min-width: 300px; max-width: 500px;">
      <div style="background: rgba(0,0,0,0.7); padding: 30px; border-radius: 20px;
                  border: 3px solid #FFD700; box-shadow: 0 10px 30px rgba(255,215,0,0.2);
                  height: 100%; position: relative;">
        
        <div style="position: absolute; top: 15px; left: 20px;">
          <span style="background: {random.choice(['#FF6347', '#00FFFF', '#9B59B6'])}; 
                 color: white; padding: 5px 15px; border-radius: 20px; font-size: 12px;">
            {quote['category']}
          </span>
        </div>
        
        <div style="margin-top: 40px;">
          <div style="font-size: 60px; color: #FFD700; opacity: 0.2; position: absolute; top: 40px; right: 30px;">
            "
          </div>
          
          <p style="color: #FFFFFF; font-size: 22px; line-height: 1.6; font-style: italic;
                    margin: 20px 0 30px 0; text-shadow: 0 2px 10px rgba(0,0,0,0.5);">
            {quote['text']}
          </p>
          
          <div style="border-top: 2px solid #FF6347; padding-top: 20px; margin-top: 30px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <div>
                <p style="color: #FFD700; margin: 0; font-size: 18px; font-weight: bold;">
                  — {quote['author']}
                </p>
                <p style="color: #9B59B6; margin: 5px 0 0 0; font-size: 12px;">
                  📚 Sabedoria para desenvolvedores
                </p>
              </div>
              <span style="color: #00FFFF; font-size: 12px;">
                ⏱️ {random.randint(1, 3)} min de reflexão
              </span>
            </div>
          </div>
        </div>
      </div>
      
      <div style="margin-top: 25px; padding: 20px; background: rgba(255,215,0,0.1); 
                  border-radius: 15px; border-left: 4px solid #FF6347;">
        <div style="display: flex; align-items: center; gap: 15px;">
          <div style="font-size: 24px; color: #FF6347;">💡</div>
          <div>
            <p style="color: #FFD700; margin: 0; font-size: 16px; font-weight: bold;">
              DICA PARA DEVS:
            </p>
            <p style="color: #9B59B6; margin: 5px 0 0 0; font-size: 14px;">
              Assim como gatos precisam de pausas, desenvolvedores precisam de momentos de criatividade.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div style="margin-top: 40px; padding: 20px; background: rgba(0,0,0,0.4); 
              border-radius: 15px; border: 1px solid #9B59B6;">
    <p style="color: #9B59B6; text-align: center; margin: 0; font-size: 14px; font-style: italic;">
      😺 <em>"Os gatos têm tudo: admiração, sono sem fim, e companhia apenas quando querem."</em> 
      — Rudyard Kipling • Última atualização automática
    </p>
  </div>

</div>

<style>
  @keyframes gentleFloat {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-8px); }}
  }}
  img:hover {{
    animation: gentleFloat 2s ease-in-out infinite;
  }}
</style>
'''
    
    return html

def main():
    """PONTO DE ENTRADA DO SCRIPT"""
    print("=" * 60)
    print("😺 INICIANDO ATUALIZAÇÃO CAT APIs")
    print("=" * 60)
    
    # 1. Ler README
    content = read_readme()
    if not content:
        print("❌ ABORTADO: Não foi possível ler README.md")
        return False
    
    # 2. Obter dados
    print("🐱 BUSCANDO GATO INSPIRADOR...")
    cat_image = get_cat_image()
    quote = get_developer_quote()
    
    print(f"✅ IMAGEM: {'Recebida da API' if 'cataas' not in cat_image else 'Fallback'}")
    print(f"✅ CITAÇÃO: '{quote['author']}'")
    
    # 3. Gerar HTML
    print("🎨 CRIANDO SEÇÃO FELINA...")
    cat_html = generate_cat_html(cat_image, quote)
    
    # 4. Atualizar seção
    print("📝 ATUALIZANDO SEÇÃO GATO...")
    new_content = update_section(
        content,
        "<!-- BEGIN CAT_APIS -->",
        "<!-- END CAT_APIS -->",
        cat_html
    )
    
    # 5. Salvar README
    if write_readme(new_content):
        print("=" * 60)
        print("✅ CAT APIs ATUALIZADAS COM SUCESSO!")
        print("=" * 60)
        return True
    else:
        print("❌ FALHA AO ATUALIZAR README")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)