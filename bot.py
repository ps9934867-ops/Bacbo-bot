import os
import telebot
from collections import Counter

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

# Guarda os últimos resultados recebidos
historico = []


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "🤖 Olá! O Bot Bacbo está online!\n\n"
        "Comandos disponíveis:\n"
        "🎯 /sinal - gerar sinal\n"
        "📊 /status - verificar o bot\n"
        "➕ /resultado 1 2 3 - adicionar resultado"
    )


@bot.message_handler(commands=["status"])
def status(message):
    bot.reply_to(
        message,
        f"✅ Bot online!\n"
        f"📊 Resultados armazenados: {len(historico)}"
    )


@bot.message_handler(commands=["resultado"])
def adicionar_resultado(message):
    try:
        partes = message.text.split()[1:]

        if len(partes) != 3:
            bot.reply_to(
                message,
                "❌ Formato incorreto.\n\n"
                "Exemplo:\n"
                "/resultado 4 2 5"
            )
            return

        dados = [int(x) for x in partes]

        if not all(1 <= x <= 6 for x in dados):
            raise ValueError

        historico.append(dados)

        # Mantém apenas os últimos 50 resultados
        if len(historico) > 50:
            historico.pop(0)

        bot.reply_to(
            message,
            f"✅ Resultado registrado: {dados[0]} - {dados[1]} - {dados[2]}\n"
            f"📊 Total armazenado: {len(historico)}"
        )

    except:
        bot.reply_to(
            message,
            "❌ Resultado inválido.\n\n"
            "Use, por exemplo:\n"
            "/resultado 3 5 2"
        )


@bot.message_handler(commands=["sinal"])
def sinal(message):

    if len(historico) < 5:
        bot.reply_to(
            message,
            "⚠️ Ainda não tenho dados suficientes.\n\n"
            "Adicione pelo menos 5 resultados usando:\n"
            "/resultado 3 5 2"
        )
        return

    # Analisa os últimos resultados
    ultimos = historico[-10:]

    soma_jogador = sum(r[0] for r in ultimos)
    soma_banqueiro = sum(r[1] for r in ultimos)

    if soma_jogador > soma_banqueiro:
        sinal = "🎯 JOGADOR"
    elif soma_banqueiro > soma_jogador:
        sinal = "🎯 BANQUEIRO"
    else:
        sinal = "🎯 EMPATE"

    bot.reply_to(
        message,
        "📡 SINAL BAC BO\n\n"
        f"{sinal}\n\n"
        f"📊 Análise dos últimos {len(ultimos)} resultados.\n"
        "⚠️ Este sinal é apenas experimental e não garante o próximo resultado."
    )


print("🤖 Bot Bacbo iniciado...")

bot.infinity_polling()
