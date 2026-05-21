import random

from telegram.ext import Application
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import filters

import os, requests, json
from datetime import datetime
from dotenv import load_dotenv

import database_operations

async def start(update, context):
    options_text = ("Hi! I'm a Bot 🤖.\n\nAvailable commands: \n" +
    "/getdata - Get current temperature 🌡️\n" +
    "/history - Last 10 measurements 📋\n" +
    "/average - Average temperature 📊\n" +
    "/max - Max temperature 📈\n" +
    "/min - Min temperature 📉")

    await context.bot.send_message(chat_id=update.effective_chat.id, text=options_text)

async def getdata(update, context):
    resp = requests.get("https://api.open-meteo.com/v1/forecast?latitude=45.4064&longitude=11.8768&current_weather=true")
    data = resp.json()
    # use local machine time instead of API-provided time
    current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    temperature = data["current_weather"]["temperature"]

    database_operations.insert_measurement(current_time, temperature)

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f"🌡️ Current temperature in Padua: {temperature}°C")

async def getaverage(update, context):
    avg_temp, count = database_operations.get_average()
    if count == 0:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="No measurements available to calculate average.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"📊 Average temperature: {avg_temp:.2f}°C based on {count} measurements.")

async def getmin(update, context):
    timestamp, min_temp = database_operations.get_min()
    if timestamp is None:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="No measurements available.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"📉 Minimum temperature: {min_temp}°C at {datetime.fromisoformat(timestamp).strftime('%Y-%m-%d %H:%M:%S')}")

async def getmax(update, context):
    timestamp, max_temp = database_operations.get_max()
    if timestamp is None:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="No measurements available.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"📈 Maximum temperature: {max_temp}°C at {datetime.fromisoformat(timestamp).strftime('%Y-%m-%d %H:%M:%S')}")

async def gethistory(update, context):
    history = database_operations.get_history()
    if not history:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="No measurements available.")
    else:
        messages = [f"🕒 {datetime.fromisoformat(timestamp).strftime('%Y-%m-%d | %H:%M:%S')}: {temp}°C" for timestamp, temp in history]
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="\n".join(messages))

async def unknown(update, context):
    options_text = (
        "Sorry I don't understand this command.\n\n"
        "Please use one of the following:\n"
        "/start - See all available options.\n"
        "/getdata - Get current temperature in Padua.\n"
        "/average - Get average temperature.\n"
        "/min - Get minimum temperature.\n"
        "/max - Get maximum temperature.\n"
        "/history - Get history of measurements.\n"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=options_text)


def __main__():
    # load environment variables
    load_dotenv()
    # bot configuration
    application = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()

    # init database
    database_operations.init_db()

    ## commands handlers
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    getdata_handler = CommandHandler('getdata', getdata)
    application.add_handler(getdata_handler)

    getaverage_handler = CommandHandler('average', getaverage)
    application.add_handler(getaverage_handler)

    getmin_handler = CommandHandler('min', getmin)
    application.add_handler(getmin_handler)

    getmax_handler = CommandHandler('max', getmax)
    application.add_handler(getmax_handler)

    gethistory_handler = CommandHandler('history', gethistory)
    application.add_handler(gethistory_handler)

    unknown_handler = MessageHandler(filters.TEXT | (~filters.COMMAND), unknown)
    application.add_handler(unknown_handler)

    # starts bot
    application.run_polling()

if __name__ == "__main__":
    __main__()
