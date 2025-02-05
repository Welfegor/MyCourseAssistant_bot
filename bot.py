from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

TOKEN = "7251612310:AAEyNnRxqVRFnL8X4aBL_eK_3y3aNel8XH8"

async def start(update: Update, context: CallbackContext):
    keyboard = [["📚 Поиск курсов", "🗓 Расписание"], ["🔔 Напоминания", "❓ Помощь"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Здравствуйте! Я ваш помощник по курсам. Выберите действие:", reply_markup=reply_markup
    )

async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text.lower()
    if "поиск курсов" in user_message:
        await update.message.reply_text("Введите название курса или категорию:")
    elif "расписание" in user_message:
      schedule = (
          "📅 *Расписание курсов на эту неделю:*\n\n"
          "🔹 *Python для начинающих* — Пн, Ср, Пт в 18:00\n"
          "🔹 *Веб-разработка (HTML, CSS, JS)* — Вт, Чт в 19:00\n"
          "🔹 *Разработка игр на Unity* — Сб в 16:00\n"
          "🔹 *Основы машинного обучения* — Ср, Вс в 17:00\n"
          "🔹 *Алгоритмы и структуры данных* — Пн, Чт в 20:00\n\n"
          "📌 Не забудьте записаться на курсы!"
      )
      await update.message.reply_text(schedule, parse_mode="Markdown")
    elif "напоминания" in user_message:
        await update.message.reply_text("Я буду напоминать вам о предстоящих занятиях!")
    elif "помощь" in user_message:
      help_text = (
          "❓ *Часто задаваемые вопросы:*\n\n"
          "🔹 *Как записаться на курс?* — Выберите нужный курс в разделе «📚 Поиск курсов» и следуйте инструкциям.\n"
          "🔹 *Что делать, если я пропустил занятие?* — Вы можете посмотреть запись урока в личном кабинете платформы.\n"
          "🔹 *Как получить скидку на обучение?* — Следите за акциями в разделе «🗓 Расписание» или подпишитесь на уведомления.\n"
          "🔹 *Как задать вопрос преподавателю?* — В каждом курсе есть чат для общения с преподавателем и студентами.\n"
          "🔹 *Где найти дополнительные материалы?* — После записи на курс вам откроется доступ к учебным материалам.\n\n"
          "📧 *Контакты поддержки:* welfegorofficial@gmail.com"
      )
      await update.message.reply_text(help_text, parse_mode="Markdown")
    else:
        await update.message.reply_text("Извините, я вас не понял. Пожалуйста, выберите действие из меню.")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
