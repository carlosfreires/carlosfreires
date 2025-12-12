@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo.
echo ============================================
echo    Configuração do Ambiente CarlosFreires
echo ============================================
echo.

REM Verificar se Python está instalado
python --version > nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python não encontrado. Instale o Python 3.8+ e tente novamente.
    pause
    exit /b 1
)

echo [OK] Python está instalado.

REM Verificar/instalar dependências
echo.
echo Instalando/atualizando dependências Python...
pip install --upgrade requests > nul 2>&1
if errorlevel 1 (
    echo [AVISO] Não foi possível instalar/atualizar requests. Continuando...
)

REM Criar diretório output se não existir
if not exist "output" mkdir output

REM Verificar variáveis de ambiente
echo.
echo Verificando configurações...
if "%GITHUB_TOKEN%"=="" (
    echo [AVISO] GITHUB_TOKEN não definida. A cobra usará dados de exemplo.
    echo         Para dados reais, defina a variável:
    echo         setx GITHUB_TOKEN "seu_token_github"
)

REM Executar scripts Python
echo.
echo Executando scripts Python...

echo 1. Gerando animação da cobra...
python generate_snake.py

echo 2. Testando token do GitHub (se disponível)...
if not "%GITHUB_TOKEN%"=="" (
    python test_token.py
)

echo 3. Atualizando seção de APIs no README...
python generate_apis.py

echo.
echo ============================================
echo    CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!
echo ============================================
echo.
echo O que foi feito:
echo - Dependências Python verificadas
echo - Cobra de contribuição gerada em output/
echo - Seção de APIs atualizada no README.md
echo.
echo Próximos passos:
echo 1. Commit e push das alterações:
echo    git add .
echo    git commit -m "Atualização automática: cobra e APIs"
echo    git push origin main
echo.
echo 2. Para atualizações automáticas, configure GitHub Actions.
echo.
pause