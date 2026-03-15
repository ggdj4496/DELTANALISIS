# --- Lanzador de Entorno DELTA ---
Write-Host "🚀 Iniciando Protocolo de Activación DELTA..." -ForegroundColor Cyan

# 1. Comprobar e Instalar librerías críticas
Write-Host "📦 Verificando dependencias (OpenCV, Python-Telegram-Bot)..." -ForegroundColor Yellow
pip install opencv-python numpy python-telegram-bot --quiet

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error instalando librerías. Revisa tu conexión a internet." -ForegroundColor Red
    exit
}

# 2. Crear el archivo del Bot (si no existe) con el Monitor incluido
$botCode = @"
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# CONFIGURACIÓN DE MONITORIZACIÓN
logging.basicConfig(format='%(asctime)s - [MONITOR DELTA] - %(message)s', level=logging.INFO)
TOKEN = 'TU_TOKEN_AQUÍ' # <--- PEGA TU TOKEN AQUÍ

async def start(update, context):
    logging.info(f"Usuario {update.effective_user.id} ha iniciado el bot.")
    await update.message.reply_text('🛰️ Sistema DELTA Activo. Monitorizando órdenes...')

async def handle_photo(update, context):
    logging.info("📥 Imagen interceptada. Iniciando análisis de capas...")
    await update.message.reply_text('🔍 Imagen recibida. Analizando segmentación local...')
    # Aquí iría tu lógica de procesamiento local

if __name__ == '__main__':
    print("--- 🛰️ CONSOLA DELTA EN LINEA ---")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling()
"@

Set-Content -Path "delta_bot_local.py" -Value $botCode

# 3. Ejecutar el Bot
Write-Host "✅ Entorno listo. Arrancando Bot..." -ForegroundColor Green
python delta_bot_local.py