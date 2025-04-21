@echo off
echo Verificando dependencias...

REM Verificar selenium
pip show selenium >nul 2>&1
if errorlevel 1 (
    echo Instalando selenium...
    pip install selenium
    if errorlevel 1 (
        echo Error al instalar selenium.
        pause
        exit /b 1
    )
) else (
    echo selenium ya está instalado.
)

REM Verificar tkinter
python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo Instalando tkinter...
    pip install tkinter
    if errorlevel 1 (
        echo Error al instalar tkinter.
        pause
        exit /b 1
    )
) else (
    echo tkinter ya está instalado.
)

echo Todas las dependencias están instaladas correctamente.
echo Iniciando WhatsApp Buster...
python buster.py
if errorlevel 1 (
    echo Error al ejecutar el programa.
    pause
) 