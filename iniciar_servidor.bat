@echo off
REM ============================================
REM Script para iniciar o servidor Streamlit
REM ============================================

REM Altere o caminho abaixo para a pasta do seu app
cd /d "C:\Users\saude\Desktop\Automacao\AutomacaoDeSistemas-main"

echo ============================================
echo Iniciando o servidor Streamlit...
echo ============================================

REM Executa o servidor
streamlit run app.py

echo ============================================
echo Servidor encerrado.
echo Pressione qualquer tecla para sair...
pause >nul
