import os
import telebot

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "🤖 Olá! O Bot Bacbo está online.\n\n"
        "Estou pronto para receber os resultados e trabalhar com sinais."
    )

@bot.message_handler(commands=["status"])
def status(message):
    bot.reply_to(message, "✅ Bot online e funcionando!")

bot.infinity_polling()
