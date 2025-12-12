@echo off
echo ================================================
echo 🧪 TESTE LOCAL DE TODAS AS APIs (EXCETO COBRINHA)
echo ================================================

echo.
echo ⚠️  NOTA: A cobrinha agora é gerada pelo GitHub Actions
echo usando Platane/snk. Teste local não disponível.
echo.

echo 🚀 TESTANDO NASA APIs...
cd scripts
set NASA_API_KEY=DEMO_KEY
python generate_apis_nasa.py
if %errorlevel% neq 0 echo ⚠️  NASA falhou (usando fallback)!

echo.
echo 📰 TESTANDO NEWS APIs...
python generate_apis_news.py
if %errorlevel% neq 0 echo ⚠️  News falhou (usando fallback)!

echo.
echo 😺 TESTANDO CAT APIs...
python generate_apis_cat.py
if %errorlevel% neq 0 echo ⚠️  Cat falhou (usando fallback)!

echo.
echo ================================================
echo ✅ TESTES COMPLETOS!
echo.
echo 🐍 Para testar a cobrinha:
echo 1. Faça push para o GitHub
echo 2. Vá em Actions > Generate Snake Animation
echo 3. Clique em "Run workflow"
echo ================================================
pause