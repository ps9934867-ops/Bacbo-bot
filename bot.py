import os
import telebot
from collections import Counter

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

# Guarda os resultados durante a execução do bot
historico = []


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "🤖 Olá! O Bot Bac Bo está online!\n\n"
        "Comandos disponíveis:\n"
        "📊 /historico - ver resultados registrados\n"
        "📈 /estatisticas - ver estatísticas\n"
        "➕ /resultado X - registrar um resultado\n"
        "🗑️ /limpar - apagar o histórico"
    )


@bot.message_handler(commands=["resultado"])
def resultado(message):
    partes = message.text.split()

    if len(partes) != 2:
        bot.reply_to(
            message,
            "Use assim:\n\n"
            "/resultado Player\n"
            "/resultado Banker\n"
            "/resultado Tie"
        )
        return

    resultado = partes[1].lower()

    nomes = {
        "player": "Player",
        "banker": "Banker",
        "tie": "Tie"
    }

    if resultado not in nomes:
        bot.reply_to(
            message,
            "Resultado inválido.\n"
            "Use: Player, Banker ou Tie."
        )
        return

    historico.append(nomes[resultado])

    bot.reply_to(
        message,
        f"✅ Resultado registrado: {nomes[resultado]}\n"
        f"Total registrado: {len(historico)}"
    )


@bot.message_handler(commands=["historico"])
def ver_historico(message):
    if not historico:
        bot.reply_to(message, "📭 Ainda não existem resultados registrados.")
        return

    ultimos = historico[-20:]

    texto = "📊 Últimos resultados:\n\n"

    for i, resultado in enumerate(ultimos, 1):
        texto += f"{i}. {resultado}\n"

    texto += f"\nTotal no histórico: {len(historico)}"

    bot.reply_to(message, texto)


@bot.message_handler(commands=["estatisticas"])
def estatisticas(message):
    if not historico:
        bot.reply_to(message, "📭 Ainda não existem resultados.")
        return

    contagem = Counter(historico)
    total = len(historico)

    player = contagem["Player"]
    banker = contagem["Banker"]
    tie = contagem["Tie"]

    texto = (
        "📈 ESTATÍSTICAS\n\n"
        f"Total: {total}\n\n"
        f"🔵 Player: {player} ({player / total * 100:.1f}%)\n"
        f"🔴 Banker: {banker} ({banker / total * 100:.1f}%)\n"
        f"🟢 Tie: {tie} ({tie / total * 100:.1f}%)\n\n"
        "⚠️ Estas estatísticas descrevem apenas o histórico "
        "registrado e não garantem o próximo resultado."
    )

    bot.reply_to(message, texto)


@bot.message_handler(commands=["limpar"])
def limpar(message):
    historico.clear()

    bot.reply_to(
        message,
        "🗑️ Histórico apagado com sucesso."
    )


print("🤖 Bot Bac Bo iniciado...")

bot.infinity_polling()
