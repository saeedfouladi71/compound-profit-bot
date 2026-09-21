import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

user_state = {}

def start(update: Update, context):
    user_state[update.effective_chat.id] = {"step": 1}
    update.message.reply_text("سلام! برای محاسبه سود مرکب، لطفاً سرمایه اولیه را وارد کن:")

def handle_message(update: Update, context):
    chat_id = update.effective_chat.id
    text = update.message.text

    if chat_id not in user_state:
        update.message.reply_text("لطفاً /start را بزن.")
        return

    step = user_state[chat_id]["step"]

    if step == 1:
        try:
            P = float(text)
            user_state[chat_id]["P"] = P
            user_state[chat_id]["step"] = 2
            update.message.reply_text("درصد سود هر معامله را وارد کن (مثلاً 0.03 برای 3 درصد):")
        except:
            update.message.reply_text("لطفاً یک عدد معتبر وارد کن.")

    elif step == 2:
        try:
            r = float(text)
            user_state[chat_id]["r"] = r
            user_state[chat_id]["step"] = 3
            update.message.reply_text("تعداد معاملات را وارد کن:")
        except:
            update.message.reply_text("درصد سود معتبر نیست.")

    elif step == 3:
        try:
            n = int(text)
            P = user_state[chat_id]["P"]
            r = user_state[chat_id]["r"]

            final = P * ((1 + r) ** n)
            profit = final - P

            msg = f"""
📊 نتیجه محاسبه سود مرکب:

💰 سرمایه اولیه: {P}
📈 درصد سود هر معامله: {r*100}%
🔢 تعداد معاملات: {n}

🏁 سرمایه نهایی: {final:.2f}
💵 سود کل: {profit:.2f}
"""

            update.message.reply_text(msg)

            user_state[chat_id]["step"] = 1
            update.message.reply_text("برای محاسبه جدید، سرمایه اولیه را وارد کن:")

        except:
            update.message.reply_text("تعداد معاملات معتبر نیست.")

def main():
    TOKEN = os.getenv("BOT_TOKEN")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    print("ربات روی Render اجرا شد...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
