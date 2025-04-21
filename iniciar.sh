#!/bin/bash

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Python3 no está instalado. Por favor, instálalo primero."
    exit 1
fi

# Verificar si pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "pip3 no está instalado. Instalando..."
    sudo apt-get update
    sudo apt-get install -y python3-pip
fi

echo "Verificando dependencias..."

# Verificar selenium
if ! pip3 show selenium &> /dev/null; then
    echo "Instalando selenium..."
    pip3 install selenium
    if [ $? -ne 0 ]; then
        echo "Error al instalar selenium."
        read -p "Presiona Enter para salir..."
        exit 1
    fi
else
    echo "selenium ya está instalado."
fi

# Verificar tkinter
if ! python3 -c "import tkinter" &> /dev/null; then
    echo "Instalando tkinter..."
    pip3 install tkinter
    if [ $? -ne 0 ]; then
        echo "Error al instalar tkinter."
        read -p "Presiona Enter para salir..."
        exit 1
    fi
else
    echo "tkinter ya está instalado."
fi

echo "Todas las dependencias están instaladas correctamente."
echo "Iniciando WhatsApp Buster..."
python3 buster.py

if [ $? -ne 0 ]; then
    echo "Error al ejecutar el programa."
    read -p "Presiona Enter para salir..."
fi 