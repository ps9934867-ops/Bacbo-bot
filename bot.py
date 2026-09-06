import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensagem = (
        "🎲 *BOT BAC BO*\n\n"
        "Bem-vindo!\n\n"
        "Comandos disponíveis:\n"
        "🎯 /sinal — gerar um sinal de simulação\n"
        "ℹ️ /ajuda — ver ajuda\n\n"
        "⚠️ Os sinais são apenas simulações e não garantem resultados."
    )

    await update.message.reply_text(mensagem, parse_mode="Markdown")


async def sinal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resultados = [
        "🔵 JOGADOR",
        "🔴 BANCA",
        "🟢 EMPATE"
    ]

    resultado = random.choice(resultados)

    mensagem = (
        "🎯 *NOVO SINAL*\n\n"
        f"➡️ Resultado sugerido: *{resultado}*\n\n"
        "⚠️ Sinal gerado aleatoriamente para simulação.\n"
        "Não representa uma previsão do resultado real."
    )

    await update.message.reply_text(mensagem, parse_mode="Markdown")


async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ *AJUDA*\n\n"
        "/start — iniciar o bot\n"
        "/sinal — gerar sinal de simulação\n"
        "/ajuda — mostrar esta mensagem",
        parse_mode="Markdown"
    )


def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN não foi configurado.")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sinal", sinal))
    app.add_handler(CommandHandler("ajuda", ajuda))

    print("🤖 Bot iniciado...")
    app.run_polling()


if __name__ == "__main__":
    main()
