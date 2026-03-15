import logging
import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - [MONITOR DELTA] - %(message)s', level=logging.INFO)

def cargar_token():
    if os.path.exists('config.txt'):
        with open('config.txt', 'r') as f:
            return f.read().strip()
    return None

async def start(update, context):
    await update.message.reply_text('SISTEMA DELTA ONLINE')

async def handle_photo(update, context):
    logging.info('IMAGEN RECIBIDA - Analizando capas...')
    await update.message.reply_text('Analizando segmentacion local...')

if __name__ == '__main__':
    token = cargar_token()
    if token:
        app = Application.builder().token(token).build()
        app.add_handler(CommandHandler('start', start))
        app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
        print('--- CONSOLA DELTA CONECTADA ---')
        app.run_polling()
