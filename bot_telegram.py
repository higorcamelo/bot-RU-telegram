import logging
import threading
import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, JobQueue
from scraping import montar_mensagem, setup_scraping
from config import token_telegram

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

switchCardapio = False  # Defina a variável globalmente

def executar_scraping():
    setup_scraping('almoco')
    setup_scraping('jantar')

# Função para lidar com o comando /start
async def startCardapio(update: Update, context: CallbackContext) -> None:
    global switchCardapio  # Declare a variável global
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Opa! Sou o JaBOT Al Mossar. Agora você receberá o cardápio para almoço e jantar!")
    switchCardapio = True
    
async def stopCardapio(update:Update, context: CallbackContext) -> None:
    global switchCardapio  # Declare a variável global
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Tudo bem, agora você deixará de receber o cardápio...")
    switchCardapio = False

# Função para lidar com o comando /cardapioStart
async def printAlmoco(update: Update, context: CallbackContext) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text=montar_mensagem('almoco'))
    
async def printJantar(update: Update, context: CallbackContext) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text=montar_mensagem('jantar'))

# Função para enviar mensagens de almoço com base no agendamento
def enviar_mensagem_almoco(context: CallbackContext):
    if switchCardapio:
        context.bot.send_message(chat_id=context.job.context, text=montar_mensagem('almoco'))

def main() -> None:
    application = Application.builder().token(token_telegram).build()

    # Registrar os manipuladores de comandos
    application.add_handler(CommandHandler("qxdStart", startCardapio))
    application.add_handler(CommandHandler("qxdStop", stopCardapio))
    application.add_handler(CommandHandler('cardapioAlmoco', printAlmoco))
    application.add_handler(CommandHandler('cardapioJantar', printJantar))
    
    # Obter o objeto JobQueue
    job_queue: JobQueue = application.job_queue

    # Agendar a função executar_scraping de segunda a sexta-feira às 6h da manhã
    job_queue.run_daily(
        executar_scraping,
        days=(0, 1, 2, 3, 4),  # Segunda a sexta
        time=datetime.time(hour=23, minute=22, second=0),  # 6:00 AM
    )

    # Agendar o envio de mensagens de almoço com base no agendamento condicional
    #job_queue.run_daily(
    #    enviar_mensagem_almoco,
    #    days=(0, 1, 2, 3, 4),  # Segunda a sexta
    #    time=datetime.time(hour=23, minute=14, second=0),  # 10:30 AM
    #    context=application.bot.get_updates().effective_chat.id  # Obtém o chat_id
    #)

    # Executar o bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    
    #TODO: DESCOBRIR COMO PROGRAMAR O CRONOGRAMA DO SCRAPING E DAS MENSAGENS

if __name__ == '__main__':
    main()
