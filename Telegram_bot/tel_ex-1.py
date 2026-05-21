import random
import os
from dotenv import load_dotenv

from telegram.ext import Application
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import filters

import os, requests, json
from dotenv import load_dotenv

load_dotenv()

async def start(update, context):
    options_text = ("¡Hola! I'm a Bot 🤖.")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=options_text)


async def getdata(update, context):
    resp = requests.get("https://api.open-meteo.com/v1/forecast?latitude=39.47&longitude=-0.38&current_weather=true")
    data = resp.json()
    temperature = data["current_weather"]["temperature"]
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f"🌡️ Current temperature in Valencia: {temperature}°C")

async def unknown(update, context):
    options_text = (
        "Sorry I dont understand this command.\n\n"
        "Please use one of the following:\n"
        "/start - See all available options 👀.\n"
        "/getdata - Get current temperature in Valencia.\n"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=options_text)

def main():
    load_dotenv()
    # bot configuration
    application = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()

    ## commands handlers
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    getdata_handler = CommandHandler('getdata', getdata)
    application.add_handler(getdata_handler)

    unknown_handler = MessageHandler(filters.TEXT | (~filters.COMMAND), unknown)
    application.add_handler(unknown_handler)

    # starts bot
    application.run_polling()

if __name__ == "__main__":
    main()
