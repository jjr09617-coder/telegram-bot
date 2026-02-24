from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📦 Pacote Básico - R$19,90", callback_data='pacote1')],
        [InlineKeyboardButton("📦 Pacote Premium - R$39,90", callback_data='pacote2')],
        [InlineKeyboardButton("💎 VIP - R$79,90", callback_data='vip')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🔥 Bem-vindo 🔥\nEscolha um pacote:",
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    textos = {
        "pacote1": "Pacote Básico\nValor: R$19,90\n\nFaça o pagamento via Pix:\nSUA_CHAVE_AQUI",
        "pacote2": "Pacote Premium\nValor: R$39,90\n\nFaça o pagamento via Pix:\nSUA_CHAVE_AQUI",
        "vip": "VIP\nValor: R$79,90\n\nFaça o pagamento via Pix:\nSUA_CHAVE_AQUI"
    }

    await query.edit_message_text(text=textos[query.data])

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()
