import os
import stripe
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("8350879750:AAHuMtnaerHNKwaqILXYRuziqTO0aIaPrDc")
STRIPE_SECRET = os.getenv("sk_test_51T4EMc2SGL0sBacP7mIJ14WrFALFgCVzifIcGo955kDpj9u86w0uo5AxknQfj9kxKC4nT9aFO0uB3ucf1NQAdUnc00BMMC2wHZ")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

stripe.api_key = STRIPE_SECRET

app = Flask(__name__)

telegram_app = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'brl',
                'product_data': {
                    'name': 'Acesso Premium',
                },
                'unit_amount': 1990,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://t.me/SEU_BOT_AQUI',
        cancel_url='https://t.me/SEU_BOT_AQUI',
    )

    await update.message.reply_text(
        f"💳 Clique para pagar:\n{checkout_session.url}"
    )

telegram_app.add_handler(CommandHandler("start", start))

@app.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, WEBHOOK_SECRET
        )
    except Exception:
        return "Erro", 400

    if event['type'] == 'checkout.session.completed':
        print("Pagamento confirmado!")

    return "OK", 200

if __name__ == "__main__":
    import threading
    threading.Thread(target=lambda: telegram_app.run_polling()).start()
    app.run(host="0.0.0.0", port=10000)
