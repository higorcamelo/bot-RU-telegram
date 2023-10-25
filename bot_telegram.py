import logging
import pytz 
import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, JobQueue, MessageHandler, filters
from scraping import montar_mensagem, setup_scraping
import config
import os.path
from pathlib import Path
import json

# Initialize logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=config.logging_level, filename= config.logging_file)
logging.getLogger("httpx").setLevel(config.logging_level)

ids = []

def save_ids():
    with open('salvo/inscritos.json', 'w+') as arquivo:
        json.dump(ids, arquivo, indent=4, ensure_ascii=False)

def recover_ids():
    if Path('salvo/inscritos.json').exists():
        with open('salvo/inscritos.json', 'r+') as arquivo:
            global ids
            ids = json.load(arquivo)

# Function to execute scraping
async def execute_scraping(context):
    setup_scraping('almoco')
    setup_scraping('jantar')

async def start(update: Update, context: CallbackContext) -> None:
    message = """
Olá! Sou o JaBOT Al Mossar, seu bot para o cardápio do RU.

Aqui estão os comandos disponíveis:
/start_cardapio - comece a receber automaticamente o cardápio, programado para as 10:40 para o almoço e 16:30 para o jantar.
/stop_cardapio - pare de receber o cardápio programado.
/almoco - receba imediatamente o cardápio do almoço.
/jantar - receba imediatamente o cardápio do jantar.
/comentario <seu comentário> - envie um comentário anônimo para o desenvolvedor. Faça sugestões, críticas, elogios, etc.
    """
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# Command handler to start menu
async def startMenu(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    if chat_id not in ids:
        ids.append(chat_id)
        save_ids()
        await context.bot.send_message(chat_id=chat_id, text="✅ Feito! Agora você irá receber o cardápio às 10:40 para o almoço e 16:30 para o jantar.")
    else:
        await context.bot.send_message(chat_id=chat_id, text="👍 Você já está inscrito para receber o cardápio. Aguarde as próximas atualizações! 📅")

# Command handler to stop menu
async def stopMenu(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    if chat_id in ids:
        ids.remove(chat_id)
        save_ids()
        await context.bot.send_message(chat_id=chat_id, text="Tudo bem, agora você deixará de receber o cardápio. Caso mude de ideia, basta usar /start_cardapio novamente.")
    else:
        await context.bot.send_message(chat_id=chat_id, text="🤷‍♂️ Você não está inscrito para receber o cardápio. Caso deseje se inscrever, use /start_cardapio. 😉")


# Command handler to print lunch menu
async def printLunch(update: Update, context: CallbackContext) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text=montar_mensagem('almoco'))

# Command handler to print dinner menu
async def printDinner(update: Update, context: CallbackContext) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text=montar_mensagem('jantar'))
    
async def enviar_comentario(update: Update, context: CallbackContext):
    comentario = update.message.text.split(' ', 1)[1]
    feedback_chat_id = config.id_feedback_chat
    await context.bot.send_message(chat_id=feedback_chat_id, text=f"Comentário de um usuário:\n\n{comentario}")

# Function to send menu based on conditional scheduling
async def sendMenu(context: CallbackContext):
    if len(ids) > 0:
        mensagem = montar_mensagem(context.job.name)
        for chat_id in ids:
            await context.bot.send_message(chat_id=chat_id, text=mensagem)

def main() -> None:
    os.makedirs(os.path.join('salvo'), exist_ok=True)
    recover_ids()

    application = Application.builder().token(config.token_telegram).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("start_cardapio", startMenu))
    application.add_handler(CommandHandler("stop_cardapio", stopMenu))
    application.add_handler(CommandHandler('almoco', printLunch))
    application.add_handler(CommandHandler('jantar', printDinner))
    application.add_handler(CommandHandler("comentario", enviar_comentario))
    
    # Get the JobQueue instance for scraping
    scraping_job_queue: JobQueue = application.job_queue

    # Execute one time to avoid errors
    scraping_job_queue.run_once(execute_scraping, 2)

    # Schedule the execute_scraping function from Monday to Friday at 6 AM
    scraping_job_queue.run_daily(
        execute_scraping,
        days=(0, 1, 2, 3, 4),  # Monday to Friday
        time=datetime.time(hour=config.scraping_hour, minute=0, second=0, tzinfo=pytz.timezone('America/Fortaleza')),  # 6:00 AM
    )

    # Get separate JobQueue instances for lunch and dinner
    lunch_job_queue: JobQueue = application.job_queue
    dinner_job_queue: JobQueue = application.job_queue
    

    # Schedule lunch menu sending at a specific time
    lunch_job_queue.run_daily(
        sendMenu,
        days = (0, 1, 2, 3, 4),  # Monday to Friday
        time = datetime.time(hour=10, minute=40, second=0, tzinfo=pytz.timezone('America/Fortaleza')),
        name = 'almoco',
    )

    # Schedule dinner menu sending at a specific time
    dinner_job_queue.run_daily(
        sendMenu,
        days = (0, 1, 2, 3, 4),  # Monday to Friday
        time = datetime.time(hour=16, minute=30, second=0, tzinfo=pytz.timezone('America/Fortaleza')),
        name = 'jantar',
    )

    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    
if __name__ == '__main__':
    main()
