from datetime import datetime
import logging
import schedule
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from scraping import montar_mensagem, setup_scraping
from config import token_telegram

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Função para lidar com o comando /start
async def start(update: Update, context: CallbackContext) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Opa! Sou o JaBOT Al Mossar.")

# Função para lidar com o comando /cardapioStart
async def force_almoco(update: Update, context: CallbackContext) -> None:
    setup_scraping('almoco')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=montar_mensagem('almoco'))
    
async def force_jantar(update: Update, context: CallbackContext) -> None:
    setup_scraping('jantar')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=montar_mensagem('jantar'))
    
    
#TODO: PROGRAMAR HORARIOS E DATAS. FAZER SCRAPING DE SEGUNDA A SEXTA 6H E POSTAR ALMOÇO ÀS 10:30 E JANTAR ÀS 16:30
#TODO: CRIAR COMANDO PARA INICIALIZAR O MODO AUTOMÁTICO COM AS MÉTRICAS ACIMA

def main() -> None:
    application = Application.builder().token(token_telegram).build()

    # Registrar os manipuladores de comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler('cardapioAlmoco', force_almoco))
    application.add_handler(CommandHandler('cardapioAlmoco', force_jantar))

    # Executar o bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
