import os
import re
import io
from collections import Counter

import pytesseract
from PIL import Image
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎲 BOT DE ANÁLISE DE BAC BO\n\n"
        "Envie uma captura do gráfico/resultados.\n"
        "Vou tentar ler os dados visíveis e apresentar uma análise estatística.\n\n"
        "⚠️ A análise não garante o próximo resultado."
    )


def analisar_texto(texto):
    texto = texto.upper()

    jogador = len(re.findall(r"\b(JOGADOR|PLAYER|P)\b", texto))
    banca = len(re.findall(r"\b(BANCA|BANKER|BANKER|B)\b", texto))
    empate = len(re.findall(r"\b(EMPATE|TIE|T)\b", texto))

    total = jogador + banca + empate

    if total == 0:
        return None

    contagem = {
        "🔵 JOGADOR": jogador,
        "🔴 BANCA": banca,
        "🟢 EMPATE": empate,
    }

    maior = max(contagem, key=contagem.get)

    return contagem, total, maior


async def analisar_imagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensagem = await update.message.reply_text(
        "📷 Imagem recebida!\n"
        "🔎 A analisar o gráfico..."
    )

    try:
        foto = update.message.photo[-1]
        arquivo = await context.bot.get_file(foto.file_id)

        dados = await arquivo.download_as_bytearray()
        imagem = Image.open(io.BytesIO(dados))

        # Aumenta a imagem para melhorar a leitura do texto
        largura, altura = imagem.size
        imagem = imagem.resize((largura * 2, altura * 2))

        texto = pytesseract.image_to_string(imagem)

        resultado = analisar_texto(texto)

        if resultado is None:
            await mensagem.edit_text(
                "❌ Não consegui identificar resultados suficientes "
                "na imagem.\n\n"
                "Tente enviar uma captura mais nítida, mostrando "
                "claramente a área dos resultados."
            )
            return

        contagem, total, maior = resultado

        percentagem = contagem[maior] / total * 100

        resposta = (
            "📊 *ANÁLISE DA IMAGEM*\n\n"
            f"🔵 Jogador: {contagem['🔵 JOGADOR']}\n"
            f"🔴 Banca: {contagem['🔴 BANCA']}\n"
            f"🟢 Empate: {contagem['🟢 EMPATE']}\n\n"
            f"📈 Mais identificado: *{maior}*\n"
            f"📊 Frequência observada: *{percentagem:.1f}%*\n\n"
            "⚠️ Isto é uma análise dos dados encontrados "
            "na imagem, não uma previsão garantida do próximo resultado."
        )

        await mensagem.edit_text(
            resposta,
            parse_mode="Markdown"
        )

    except Exception as erro:
        await mensagem.edit_text(
            "❌ Não foi possível analisar esta imagem.\n\n"
            "Verifique se a captura está nítida e tente novamente."
        )

        print(f"Erro ao analisar imagem: {erro}")


async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ COMO USAR\n\n"
        "1️⃣ Envie /start\n"
        "2️⃣ Envie uma captura do gráfico\n"
        "3️⃣ Aguarde a análise\n\n"
        "⚠️ Os resultados são estatísticos e não garantem o próximo resultado."
    )


def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN não foi configurado.")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ajuda", ajuda))
    app.add_handler(
        MessageHandler(filters.PHOTO, analisar_imagem)
    )

    print("🤖 Bot iniciado...")
    app.run_polling()


if __name__ == "__main__":
    main()
