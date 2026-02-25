#!/bin/bash
cd /root/GexBot_Trading_Library
# Generar el informe para Gemini
/root/GexBot_Trading_Library/venv/bin/python3 /root/GexBot_Trading_Library/generar_informe.py
# Subir todo a GitHub
git add .
git commit -m "Auto-reporte: $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main
