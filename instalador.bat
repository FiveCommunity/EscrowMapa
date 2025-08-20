@echo off
echo Verificando se o Python esta instalado...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python nao encontrado! Por favor, instale o Python antes de continuar.
    pause
    exit /b
)

echo Instalando dependencias...
pip install --upgrade pip
pip install requests colorama pycryptodome

echo Dependencias instaladas com sucesso!
pause
