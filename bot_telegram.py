import logging
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from scraping import montar_mensagem, setup_scraping
from config import token_telegram

# Initialize logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO, filename='logging_bot.log')
logging.getLogger('httpx').setLevel(logging.WARNING)

# Global variable for menu switch
switchMenu = False

scheduler = BackgroundScheduler(timezone="America/Sao_Paulo")

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
    logging.info(switchMenu)
    
    # Schedule the menu sending jobs
    scheduler.add_job(sendMenuAsync, CronTrigger(day_of_week='mon-sat', hour=11, minute=12), args=['almoco', chat_id, context])
    scheduler.add_job(sendMenuAsync, CronTrigger(day_of_week='mon-sat', hour=11, minute=13), args=['jantar', chat_id, context])

# Command handler to stop menu
async def stopMenu(update: Update, context: CallbackContext) -> None:
    global switchMenu
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Tudo bem, agora você deixará de receber o cardápio...")

# Command handler to print lunch menu
async def printLunch(update: Update, context: CallbackContext) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text=montar_mensagem('almoco'))

# Command handler to print dinner menu
async def printDinner(update: Update, context: CallbackContext) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text=montar_mensagem('jantar'))

# Define an asynchronous function that sends the menu
async def sendMenuAsync(tipo_refeicao: str, chat_id, context: CallbackContext):
    try:
        if switchMenu:
            logging.info(f"Chamando sendMenuAsync para {tipo_refeicao}")
            montagem = montar_mensagem(tipo_refeicao)
            await context.bot.send_message(chat_id=chat_id, text=montagem) #TODO NAO SEI MAIS O QUE FAZER
    except Exception as e:
        logging.error(f"Error in sendMenuAsync: {str(e)}")

def main() -> None:
    application = Application.builder().token(token_telegram).build()
    
    # Register command handlers
    application.add_handler(CommandHandler("start_cardapio", startMenu))
    application.add_handler(CommandHandler("stop_cardapio", stopMenu))
    application.add_handler(CommandHandler('cardapio_almoco', printLunch))
    application.add_handler(CommandHandler('cardapio_jantar', printDinner))
    
    scheduler.add_job(schedule_scraping, CronTrigger(day_of_week='mon-fri', hour=6, minute=0))
    
    # Start the scheduler
    scheduler.start()

    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
