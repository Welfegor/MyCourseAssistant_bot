import asyncio
from datetime import time
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

TOKEN = "ВАШ_ТОКЕН"

# Флаг для включения/выключения напоминаний
user_reminders = {}

# Список занятий (курс, время)
schedule = [
    ("Python для начинающих", time(10, 0)),   # 10:00
    ("Основы машинного обучения", time(14, 30)),  # 14:30
    ("Веб-разработка на Django", time(18, 0)),  # 18:00
]

# Функция отправки напоминаний
async def send_reminders(context: CallbackContext):
    """Отправляет напоминания о курсах в установленное время."""
    job = context.job
    chat_id = job.chat_id

    if chat_id in user_reminders and user_reminders[chat_id]:
        message = "🔔 *Напоминание о курсах на сегодня:*\n\n"
        for course, course_time in schedule:
            message += f"📅 *{course}* в {course_time.strftime('%H:%M')}\n"

        await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")

# Команда /напоминания
async def reminders(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    if chat_id in user_reminders and user_reminders[chat_id]:
        user_reminders[chat_id] = False
        await update.message.reply_text("❌ Напоминания отключены.")
    else:
        user_reminders[chat_id] = True
        context.job_queue.run_daily(send_reminders, time=time(9, 0), chat_id=chat_id)  # Уведомления в 9:00
        await update.message.reply_text("✅ Напоминания включены! Вы получите расписание на день в 9:00.")

# Обработчик команды /start
async def start(update: Update, context: CallbackContext):
    keyboard = [["📚 Поиск курсов", "🗓 Расписание"], ["🔔 Напоминания", "❓ Помощь"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Здравствуйте! Я ваш помощник по курсам. Выберите действие:", reply_markup=reply_markup
    )

# Обработчик сообщений
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text.lower()

    if "поиск курсов" in user_message:
        await update.message.reply_text("Введите название курса или категорию:")
    elif "расписание" in user_message:
        schedule_text = "📅 *Расписание курсов на эту неделю:*\n\n"
        for course, course_time in schedule:
            schedule_text += f"🔹 *{course}* в {course_time.strftime('%H:%M')}\n"
        await update.message.reply_text(schedule_text, parse_mode="Markdown")
    elif "напоминания" in user_message:
        await reminders(update, context)
    elif "помощь" in user_message:
        help_text = (
            "❓ *Часто задаваемые вопросы:*\n\n"
            "🔹 *Как записаться на курс?* — Выберите курс в разделе «📚 Поиск курсов».\n"
            "🔹 *Как получить скидку?* — Следите за акциями.\n"
            "🔹 *Как задать вопрос преподавателю?* — В каждом курсе есть чат.\n\n"
            "📧 *Контакты:* welfegorofficial@gmail.com"
        )
        await update.message.reply_text(help_text, parse_mode="Markdown")
    else:
        await update.message.reply_text("Извините, я вас не понял. Пожалуйста, выберите действие из меню.")

# Запуск бота
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("напоминания", reminders))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
