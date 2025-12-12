"""
UTILITÁRIOS COMPARTILHADOS - VERSÃO 1.0
Funções comuns para todos os scripts de atualização do README
"""
import os
from datetime import datetime

# Caminhos absolutos para evitar problemas de diretório
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
README_PATH = os.path.join(CURRENT_DIR, "..", "README.md")

def read_readme():
    """
    Lê o conteúdo atual do README.md
    Retorna: str - Conteúdo do arquivo ou string vazia se erro
    """
    try:
        with open(README_PATH, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ ERRO: Arquivo {README_PATH} não encontrado!")
        return ""
    except Exception as e:
        print(f"❌ ERRO ao ler README: {e}")
        return ""

def write_readme(content):
    """
    Escreve conteúdo no README.md
    Args:
        content (str): Conteúdo a ser escrito
    Retorna: bool - True se sucesso, False se erro
    """
    try:
        with open(README_PATH, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"❌ ERRO ao escrever README: {e}")
        return False

def update_section(content, start_marker, end_marker, new_content):
    """
    Atualiza uma seção específica entre marcadores HTML
    Args:
        content (str): Conteúdo completo do README
        start_marker (str): Marcador de início (ex: "<!-- BEGIN NASA -->")
        end_marker (str): Marcador de fim (ex: "<!-- END NASA -->")
        new_content (str): Novo conteúdo para a seção
    Retorna: str - Conteúdo atualizado
    """
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    if start_idx == -1:
        print(f"⚠️  AVISO: Marcador de início não encontrado: {start_marker}")
        return content
    
    if end_idx == -1:
        print(f"⚠️  AVISO: Marcador de fim não encontrado: {end_marker}")
        return content
    
    # Calcular posição final considerando o comprimento do marcador
    end_idx += len(end_marker)
    
    # Substituir conteúdo entre os marcadores
    before = content[:start_idx]
    after = content[end_idx:]
    
    return before + start_marker + "\n" + new_content + "\n" + end_marker + after

def get_timestamp():
    """
    Retorna timestamp formatado para logs
    Retorna: str - Timestamp no formato YYYY-MM-DD HH:MM:SS
    """
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

def log_success(section_name):
    """
    Gera mensagem de log de sucesso
    Args:
        section_name (str): Nome da seção atualizada
    """
    timestamp = get_timestamp()
    print(f"✅ SEÇÃO '{section_name}' ATUALIZADA: {timestamp}")
    return f"<!-- 🔄 {section_name} atualizado: {timestamp} -->"

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