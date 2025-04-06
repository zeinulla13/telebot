import logging
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Твой токен
TOKEN = "7322085126:AAEfdS284EIDNE1zchyFIrTcXcCyAhNFIqg"

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Словарь для отслеживания состояния пользователя
user_states = {}

# Стартовая команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Мы рады, что ты хочешь попасть на Бал.\n\n"
        "Пожалуйста, напиши своё Фамилия, Имя и Класс (пример: Байдуллаев Зейнулла 10Д)"
    )

# Приём ФИО
async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    full_text = update.message.text.strip()

    user_states[user_id] = "waiting_for_pdf"

    await update.message.reply_text(
        f"«{full_text}» стоимость билета 2500тг на одного человека.\n\n"
        "Для приобретения, отправь деньги на номер KASPI:\n"
        "*87752027187* Байдуллаев Зейнулла\n\n"
        "И пришли, пожалуйста, чек в формате **PDF** сюда в этот чат."
    )

# Обработка PDF чека
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_states.get(user_id) != "waiting_for_pdf":
        await update.message.reply_text("Сначала напиши Фамилию, Имя и Класс.")
        return

    document = update.message.document
    if document.mime_type != "application/pdf":
        await update.message.reply_text("Пожалуйста, отправь чек **в формате PDF**.")
        return

    await update.message.reply_text("Спасибо! Чек получен.")

    # Отправка готового QR-кода
    with open("qr_code_image.jpg", "rb") as qr:
        await update.message.reply_photo(
            photo=InputFile(qr),
            caption="Вот ваш личный Qr код, который проверят у входа на Бал"
        )

    # Сброс состояния
    user_states.pop(user_id, None)

# Запуск бота
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()