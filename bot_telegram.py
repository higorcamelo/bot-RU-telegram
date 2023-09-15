import logging
from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from scraping import montar_mensagem, setup_scraping
from config import token_telegram

# Initialize logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

# Global variable for menu switch
switchMenu = False

scheduler = BackgroundScheduler()

# Function to execute scraping
def execute_scraping():
    setup_scraping('almoco')
    setup_scraping('jantar')

def schedule_scraping():
    execute_scraping()

# Command handler to start menu
async def startMenu(update: Update, context: CallbackContext) -> None:
    global switchMenu
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Opa! Sou o JaBOT Al Mossar. Agora você receberá o cardápio para almoço e jantar!")
    switchMenu = True

# Command handler to stop menu
async def stopMenu(update: Update, context: CallbackContext) -> None:
    global switchMenu
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Tudo bem, agora você deixará de receber o cardápio...")
    switchMenu = False

# Command handler to print lunch menu
async def printLunch(update: Update, context: CallbackContext) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text=montar_mensagem('almoco'))

# Command handler to print dinner menu
async def printDinner(update: Update, context: CallbackContext) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text=montar_mensagem('jantar'))

# Function to send menu based on conditional scheduling
def sendMenu(tipo_refeicao: str, context: CallbackContext):
    if switchMenu:
        montagem = montar_mensagem(tipo_refeicao)
        context.bot.send_message(chat_id=update.effective_chat.id, text=montagem)

def main() -> None:
    application = Application.builder().token(token_telegram).build()

    # Register command handlers
    application.add_handler(CommandHandler("start_cardapio", startMenu))
    application.add_handler(CommandHandler("stop_cardapio", stopMenu))
    application.add_handler(CommandHandler('cardapio_almoco', printLunch))
    application.add_handler(CommandHandler('cardapio_jantar', printDinner))

    scheduler.add_job(schedule_scraping, 'cron', day_of_week='mon-fri', hour=6, minute=00)
    #scheduler.add_job(sendMenu, 'cron', args=['almoco'], day_of_week='mon-fri', hour=8, minute=52, context=application)
    #cheduler.add_job(sendMenu, 'cron', args=['jantar'], day_of_week='mon-fri', hour=18, minute=0, context=application)

    # Start the scheduler
    scheduler.start()

    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
