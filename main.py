import os
import logging
import aiohttp

from typing import Final
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

TOKEN: Final = os.getenv('API_KEY')
BOT_USERNAME: Final = '@AS_OpoBot'

# Configuración de los logs
logging.basicConfig(datefmt='%d/%m/%Y %I:%M:%S %p',
                    encoding='utf-8',
                    filemode='w',
                    filename='logs.log',
                    format='%(levelname)s %(asctime)s: %(message)s',
                    level=logging.INFO
                    )

logging.debug('Prueba')

# Commands

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello!')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Ayuda por favor!')


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: Añadir un fetch que llame a la API que creamos
    await update.message.reply_text('Custom')


# Responses

async def handle_response(text: str) -> str:
    processed: str = text.lower()
    query = text.replace(' ', '%20')
    # Preparar la URL
    base_url = "http://localhost:8000/buscar/"  # Ajusta el puerto si es diferente
    url = f"{base_url}?q={query}"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()

                    if not data:
                        return "No encontré resultados que coincidan 😔"

                    # Formatear los resultados
                    formatted_results = []
                    for item in data[:3]:  # Los 3 más relevantes
                        formatted = (
                            f"📚 *{item['title']}*\n"
                            f"🏢 Fuente: {item['source']}\n"
                            f"📅 Inicio: {item['start_date'][:10]}\n"
                            f"📅 Fin: {item['end_date'][:10] if item['end_date'] else 'Sin fecha de fin'}\n"
                            f"📌 Estado: {item['status']}\n"
                            f"🔗 [Ver convocatoria]({item['url']})\n"
                            f"⭐ Coincidencias: {item.get('coincidencias', 0)}\n"
                            "-------------------------\n"
                        )
                        formatted_results.append(formatted)

                    return "\n".join(formatted_results)

                else:
                    return f"Error consultando las convocatorias 😵 ({response.status})"
        except Exception as e:
            return f"Error: {str(e)}"

    if 'hello' in processed:
        return 'Hey there'

    if 'how' in processed:
        return 'good'

    return 'No se'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    logging.info(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip
            response: str = await handle_response(new_text)
        else:
            return
    else:
        response: str = await handle_response(text)

    logging.info(f"Bot: {response}")
    await update.message.reply_text(response, parse_mode='Markdown')


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error('Update {update} caused error {context.error}')


if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)
