import math
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

### HANDLERS CALCULATE ###

def calculate(update, context):
    ctx_array = context.args
    calculation = ""

    if ctx_array[1] == '+':
        calculation = f"{int(ctx_array[0])+int(ctx_array[2])}"
    elif ctx_array[1] == '-':
        calculation = f"{int(ctx_array[0])-int(ctx_array[2])}"
    elif  ctx_array[1] == '*':
        calculation = f"{int(ctx_array[0])*int(ctx_array[2])}"
    elif ctx_array[1] == '/':
        calculation = f"{int(ctx_array[0])/int(ctx_array[2])}"
    elif ctx_array[1] == 'pow':
        calculation = f"{int(ctx_array[0])**int(ctx_array[2])}"
    elif ctx_array[0] == 'sqrt':
        calculation = f"{math.sqrt(float(ctx_array[1]))}"
    else: calculation = "Error. Argumentos no válidos."

    context.bot.send_message(chat_id=update.effective_chat.id, text=calculation)