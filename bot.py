from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

def start(update: Update, context: CallbackContext):
    keyboard = [["📚 Поиск курсов", "🗓 Расписание"], ["🔔 Напоминания", "❓ Помощь"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(
        "Здравствуйте! Я ваш помощник по курсам. Выберите действие:", reply_markup=reply_markup
    )

def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text.lower()
    if "поиск курсов" in user_message:
        update.message.reply_text("Введите название курса или категорию:")
    elif "расписание" in user_message:
        update.message.reply_text("Расписание курсов на эту неделю: ...")
    elif "напоминания" in user_message:
        update.message.reply_text("Я буду напоминать вам о предстоящих занятиях!")
    elif "помощь" in user_message:
        update.message.reply_text("Вот список часто задаваемых вопросов: ...")
    else:
        update.message.reply_text("Извините, я вас не понял. Пожалуйста, выберите действие из меню.")

def main():
    updater = Updater("7251612310:AAEyNnRxqVRFnL8X4aBL_eK_3y3aNel8XH8")

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
