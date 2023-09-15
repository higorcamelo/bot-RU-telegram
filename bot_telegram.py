import logging
import threading
import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, JobQueue
from scraping import montar_mensagem, setup_scraping
from config import token_telegram

# Initialize logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

# Global variable for menu switch
switchMenu = False

# Function to execute scraping
def execute_scraping():
    setup_scraping('almoco')
    setup_scraping('jantar')

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
def sendMenu(context: CallbackContext):
    if switchMenu:
        context.bot.send_message(chat_id=context.job.context, text=montar_mensagem(context.job.name))

def main() -> None:
    application = Application.builder().token(token_telegram).build()

    # Register command handlers
    application.add_handler(CommandHandler("startMenu", startMenu))
    application.add_handler(CommandHandler("stopMenu", stopMenu))
    application.add_handler(CommandHandler('printLunch', printLunch))
    application.add_handler(CommandHandler('printDinner', printDinner))

    # Get the JobQueue instance for scraping
    scraping_job_queue: JobQueue = application.job_queue

    # Schedule the execute_scraping function from Monday to Friday at 6 AM
    scraping_job_queue.run_daily(
        execute_scraping,
        days=(0, 1, 2, 3, 4),  # Monday to Friday
        time=datetime.time(hour=19, minute=33, second=0),  # 6:00 AM
    )

    # Get separate JobQueue instances for lunch and dinner
    lunch_job_queue: JobQueue = application.job_queue
    dinner_job_queue: JobQueue = application.job_queue

    # Schedule lunch menu sending at a specific time
    lunch_job_queue.run_daily(
        sendMenu,
        days=(0, 1, 2, 3, 4),  # Monday to Friday
        time=datetime.time(hour=12, minute=0, second=0),  # 12:00 PM
        data='almoco',
    )

    # Schedule dinner menu sending at a specific time
    dinner_job_queue.run_daily(
        sendMenu,
        days=(0, 1, 2, 3, 4),  # Monday to Friday
        time=datetime.time(hour=18, minute=0, second=0),  # 6:00 PM
        data='jantar',
    )

    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    
if __name__ == '__main__':
    main()
