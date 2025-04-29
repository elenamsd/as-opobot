import os
import logging
from datetime import time as dt_time
from zoneinfo import ZoneInfo

from typing import Final
from dotenv import load_dotenv
from telegram import BotCommand, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from pymongo import MongoClient, errors

load_dotenv()

TOKEN: Final = os.getenv("API_KEY")
BOT_USERNAME: Final = os.getenv("BOT_USERNAME", "@AS_OpoBot")
MONGO_DB_URI: Final  = os.getenv("MONGO_DB_URI")
DB_NAME: Final = os.getenv("DB_NAME", "uipathFuente")

try:
    client = MongoClient(MONGO_DB_URI, serverSelectionTimeoutMS=5000, connectTimeoutMS=5000)
    client.server_info()   # fuerza la conexión
    print("✅ Conexión exitosa a MongoDB")
except errors.ServerSelectionTimeoutError as err:
    print("❌ No puede conectar a MongoDB:", err)
except Exception as e:
    print("❌ Error inesperado:", e)

# Configuración de los logs
logging.basicConfig(datefmt='%d/%m/%Y %I:%M:%S %p',
                    encoding='utf-8',
                    filemode='w',
                    filename='logs.log',
                    format='%(levelname)s %(asctime)s: %(message)s',
                    level=logging.INFO
                    )

logging.debug('Bot arrancando…')

# Helper para MongoDB
def get_mongo_db():
    """
    Conecta a Mongo y devuelve (db, client).
    La base se elige con la variable DB_NAME.
    """
    client = MongoClient(MONGO_DB_URI)
    db = client[DB_NAME]
    return db, client

# --- Comandos del bot
# Mensaje de bienvenida
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "¡Hola! Soy OpoBot 🤖 "
        "Conmigo puedes buscar convocatorias de oposiciones en base a tus intereses.\n\n"
        "Usa /help para ver las funciones disponibles."
    )
    await update.message.reply_text(welcome_text)

# Ayuda. Muestra los comandos posibles.
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🤖 *Funciones del bot de Oposiciones*\n\n"
        "*/start* - Mostrar mensaje de bienvenida\n"
        "*/help* - Mostrar esta ayuda\n\n"
        "*/interes <palabra>* - Añadir un tema de interés. Ej: `/interes informática`\n"
        "*/quitar_interes <palabra>* - Eliminar un interés. Ej: `/quitar_interes informática`\n"
        "*/mis_intereses* - Listar tus intereses actuales\n\n"
        "*/buscar* - Buscar convocatorias según tus intereses\n\n"
        "Además:\n"
        "• Responde a cualquier texto buscando convocatorias (usa palabras clave).\n"
        "• Notifica cada día a las 06:00 AM las nuevas convocatorias que coincidan con tus intereses.\n\n"
        "¡Prueba por ejemplo:\n"
        "`/interes educación`\n"
        "`/mis_intereses`\n"
        "y luego envía /buscar para ver las convocatorias! 😊"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

# Añadir interés
async def add_interest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    if not context.args:
        return await update.message.reply_text("❌ Usa: /interes <palabra>")

    keyword = " ".join(context.args).strip().lower()
    db, client = get_mongo_db()

    try:
        col = db.usuarios
        if col.find_one({"user_id": user_id, "keyword": keyword}):
            await update.message.reply_text(f"🟡 Ya tenías el interés “{keyword}”.")
        else:
            col.insert_one({"user_id": user_id, "keyword": keyword})
            await update.message.reply_text(
                f"✅ Añadido interés: *{keyword}*", parse_mode="Markdown"
            )
    except Exception as e:
        logging.error(f"Error guardando interés en MongoDB: {e}")
        await update.message.reply_text(
            "❌ Hubo un error guardando tu interés. Prueba otra vez más tarde."
        )
    finally:
        client.close()

# Eliminar interés
async def remove_interest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    if not context.args:
        return await update.message.reply_text("❌ Usa: /quitar_interes <palabra>")

    keyword = " ".join(context.args).strip().lower()
    db, client = get_mongo_db()
    col = db.usuarios
    res = col.delete_one({"user_id": user_id, "keyword": keyword})

    if res.deleted_count:
        await update.message.reply_text(
            f"🗑️ Eliminado interés: *{keyword}*", parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(f"❌ No tenías el interés “{keyword}”.")
    client.close()

# Listar intereses
async def list_interests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    db, client = get_mongo_db()
    col = db.usuarios
    docs = list(col.find({"user_id": user_id}))
    client.close()

    if not docs:
        return await update.message.reply_text(
            "ℹ️ No tienes intereses. Añade uno con /interes <palabra>."
        )

    texto = "\n".join(f"• {d['keyword']}" for d in docs)
    await update.message.reply_text(f"📚 Tus intereses:\n\n{texto}")

# Filtrar las convocatorias según los intereses
async def buscar_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id

    # 1) Se conecta a Mongo
    try:
        db, client = get_mongo_db()
    except Exception as e:
        return await update.message.reply_text(f"❌ Error de BD: {e}")

    try:
        # 2) Lee los intereses
        intereses = list(db.usuarios.find({"user_id": user_id}))
        if not intereses:
            return await update.message.reply_text("ℹ️ No tienes intereses. Usa /interes primero.")

        # 3) Busca en convocatoriasOriginal
        convocatorias = list(db.convocatoriasOriginal.find())
        resultados = []
        for doc in convocatorias:
            nombre = (doc.get("nombre") or "").lower()
            for i in intereses:
                kw = i["keyword"].lower()
                if kw in nombre:
                    resultados.append(doc)
                    break

        # 4) Formatea la respuesta
        if not resultados:
            await update.message.reply_text("😔 No hay convocatorias que coincidan con tus intereses.")
        else:
            lines = []
            for doc in resultados[:10]:
                lines.append("\n".join([
                    f"📚 *{doc['nombre']}*",
                    f"🏢 Fuente: {doc.get('fuente','')}",
                    f"📅 Inicio: {doc.get('fecha_inicio','')[:10]}",
                    f"📅 Fin: {doc.get('fecha_fin')[:10] if doc.get('fecha_fin') else 'Sin fecha de fin'}",
                    f"🔗 [Ver convocatoria]({doc.get('url','')})",
                    "-------------------------",
                ]))
            await update.message.reply_text("\n\n".join(lines), parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Error en buscar_command: {e}")
        await update.message.reply_text("❌ Error buscando convocatorias.")
    finally:
        client.close()

# Comandos desconocidos por el bot
async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ No existe el comando especificado. Usa /help para ver los disponibles.")

# Texto libre no reconocido por el bot (p. ej.: "fuhsjdkfgjh", "hola", ...)
async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 No he entendido ese mensaje. Usa /help para ver los comandos disponibles.")

# Manejo de errores
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Update {update} caused error {context.error}")

# Tarea programada: leer de Mongo y notificar según intereses
async def check_and_notify(context: ContextTypes.DEFAULT_TYPE):
    logging.info("🔍 Revisando convocatorias…")
    try:
        db, client = get_mongo_db()
        # 1) Traemos todas las convocatorias abiertas
        abiertas = list(db.convocatoriasOriginal.find())
        historico  = db.convocatoriasHistorico

        # 2) Obtenemos la lista de usuarios que tienen intereses
        user_ids = db.usuarios.distinct("user_id")

        # 3) Para cada usuario, filtramos por sus intereses
        for uid in user_ids:
            intereses = list(db.usuarios.find({"user_id": uid}))
            for doc in abiertas:
                nombre = (doc.get("nombre") or "").lower()
                for i in intereses:
                    kw = i["keyword"].lower()
                    if kw in nombre:
                        text = "\n".join([
                            f"📢 Convocatoria sobre *{kw}*:",
                            f"📚 *{doc['nombre']}*",
                            f"🏢 Fuente: {doc.get('fuente','')}",
                            f"📅 Inicio: {doc.get('fecha_inicio','')[:10]}",
                            f"📅 Fin: {doc.get('fecha_fin','')[:10] if doc.get('fecha_fin') else 'Sin fecha de fin'}",
                            f"🔗 [Ver convocatoria]({doc.get('url','')})"
                        ])
                        await context.bot.send_message(
                            chat_id=uid,
                            text=text,
                            parse_mode="Markdown"
                        )
                        # 4) Si aún no está en histórico, lo movemos
                        if not historico.find_one({"_id": doc["_id"]}):
                            historico.insert_one(doc)
                        break  # no procesar más keywords para este doc y usuario
    except Exception as e:
        logging.error(f"Error en check_and_notify: {e}")
    finally:
        client.close()

# Arrancar el bot y el scheduler
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler("interes", add_interest))
    app.add_handler(CommandHandler("quitar_interes", remove_interest))
    app.add_handler(CommandHandler("mis_intereses", list_interests))
    app.add_handler(CommandHandler("buscar", buscar_command))
    app.add_handler(MessageHandler(filters.COMMAND, unknown_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_message))

    # Errors
    app.add_error_handler(error)

    # Scheduler: todos los días a las 06:00
    app.job_queue.run_daily(
        callback=check_and_notify,
        time=dt_time(hour=6, minute=0, second=0, tzinfo=ZoneInfo("Atlantic/Canary")),
        name="daily_opp_notifications"
    )


    # Lista de comandos del bot (los que quieres que salgan al escribir "/")
    COMMANDS = [
        BotCommand("start", "Mostrar mensaje de bienvenida"),
        BotCommand("help", "Mostrar la ayuda del bot"),
        BotCommand("interes", "Añadir un tema de interés"),
        BotCommand("quitar_interes", "Eliminar un tema de interés"),
        BotCommand("mis_intereses", "Ver tus intereses"),
        BotCommand("buscar", "Buscar convocatorias según tus intereses"),
    ]

    # Establecer los comandos visibles en el menú de Telegram
    async def set_commands():
        await app.bot.set_my_commands(COMMANDS)

    app.post_init(set_commands)

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)
