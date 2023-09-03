from datetime import datetime
import time
import logging
import schedule
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, filters
from scraping import montar_mensagem, setup_scraping
from config import token_telegram

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)


logger = logging.getLogger(__name__)

# Função para lidar com o comando /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Opa! Sou o JaBOT Al Mossar.")
    
def enviar_cardapio(update, context):
    context.bot.send_message(chat_id = update.effective_chat, text = montar_mensagem(True))
    
start_handler = CommandHandler('start', start)
enviar_cardapio_handler = CommandHandler('cardapioStart', enviar_cardapio)

def main() -> None:
    updater = Updater(token=token, use_context=True)

    dp = updater.dispatcher

    # Registrar os manipuladores de comandos e mensagens
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler('forceCardapio', enviar_cardapio))
    dp.add_handler(MessageHandler(Filters.command, unknown))

    # Iniciar o bot
    updater.start_polling()

    # Mantenha o bot em execução até que seja interrompido manualmente (Ctrl + C)
    updater.idle()

if __name__ == '__main__':
    main()
