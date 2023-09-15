import logging
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from scraping import montar_mensagem, setup_scraping
from config import token_telegram

# Initialize logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO, filename='logging_bot.log')
logging.getLogger().setLevel(logging.WARNING)

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
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text="Opa! Sou o JaBOT Al Mossar. Agora você receberá o cardápio para almoço e jantar!")
    switchMenu = True
    
    scheduler.add_job(sendMenuWrapper, 'cron', args=['almoco', chat_id, context], day_of_week='mon-fri', hour=19, minute=9)
    scheduler.add_job(sendMenuWrapper, 'cron', args=['jantar', chat_id, context], day_of_week='mon-fri', hour=19, minute=10) #TODO: Erro aqui? Só uma mensagem é enviada

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

# Define an asynchronous function that sends the menu
async def sendMenuAsync(tipo_refeicao: str, chat_id, context: CallbackContext):
    if switchMenu:
        montagem = montar_mensagem(tipo_refeicao)
        await context.bot.send_message(chat_id=chat_id, text=montagem)

# Define a synchronous wrapper function that runs the asynchronous function
def sendMenuWrapper(tipo_refeicao: str, chat_id, context: CallbackContext):
    if switchMenu:
        asyncio.run(sendMenuAsync(tipo_refeicao, chat_id, context))
    
def main() -> None:
    application = Application.builder().token(token_telegram).build()

    # Register command handlers
    application.add_handler(CommandHandler("start_cardapio", startMenu))
    application.add_handler(CommandHandler("stop_cardapio", stopMenu))
    application.add_handler(CommandHandler('cardapio_almoco', printLunch))
    application.add_handler(CommandHandler('cardapio_jantar', printDinner))
     
    chat_id = None
    
    scheduler.add_job(schedule_scraping, 'cron', day_of_week='mon-fri', hour=6, minute=00)
    
    # Start the scheduler
    scheduler.start()

    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
