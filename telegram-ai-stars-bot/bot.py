"""
Telegram AI Utility Bot with Stars Monetization
Freemium: limited free AI queries, paid unlimited via Telegram Stars.
"""
import os
from telebot import TeleBot, types
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = TeleBot(TOKEN)

# In-memory store (use SQLite/Redis in production)
user_credits = {}  # user_id -> remaining free queries
FREE_LIMIT = 5

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_credits.setdefault(user_id, FREE_LIMIT)
    bot.reply_to(
        message,
        f"Welcome! You have {user_credits[user_id]} free AI queries.\n"
        "/ask <question> — Ask AI\n"
        "/buy — Get more with Telegram Stars"
    )

@bot.message_handler(commands=['ask'])
def ask(message):
    user_id = message.from_user.id
    if user_credits.get(user_id, 0) <= 0:
        bot.reply_to(message, "Free limit reached. Use /buy to continue.")
        return
    query = message.text.replace('/ask', '').strip()
    if not query:
        return bot.reply_to(message, "Usage: /ask your question")
    # TODO: Call OpenAI / Grok / Anthropic here
    reply = f"[AI Placeholder] Answer to: {query}"
    user_credits[user_id] -= 1
    bot.reply_to(message, reply + f"\n\nRemaining free: {user_credits[user_id]}")

@bot.message_handler(commands=['buy'])
def buy(message):
    prices = [types.LabeledPrice(label="50 AI Queries", amount=50)]  # 50 Stars
    bot.send_invoice(
        message.chat.id,
        title="AI Query Pack",
        description="50 additional AI queries",
        invoice_payload="queries_50",
        provider_token="",  # Empty for Stars
        currency="XTR",
        prices=prices
    )

@bot.pre_checkout_query_handler(func=lambda q: True)
def pre_checkout(query):
    bot.answer_pre_checkout_query(query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def successful_payment(message):
    user_id = message.from_user.id
    user_credits[user_id] = user_credits.get(user_id, 0) + 50
    bot.reply_to(message, "Payment successful! +50 queries added.")

if __name__ == "__main__":
    bot.infinity_polling()
