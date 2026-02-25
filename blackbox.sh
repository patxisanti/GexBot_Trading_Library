#!/bin/bash
echo "🚀 Sincronizando búnker con la base central..."
cd /root/GexBot_Trading_Library
git add .
git commit -m "Auto-reporte: $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main
echo "✅ Informe enviado. Gemini ya puede ver los cambios."
