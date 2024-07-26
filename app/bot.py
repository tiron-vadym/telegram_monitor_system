import os

from sqlalchemy.future import select
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from dotenv import load_dotenv

from db import AsyncSessionLocal
from app.models import Message

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Hello! I am your bot. Use /messages to get started!"
    )


async def messages(update: Update, context: CallbackContext) -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Message)
            .order_by(Message.timestamp.desc())
            .limit(10)
        )
        msges = result.scalars().all()
        response = ""
        for message in msges:
            response += (f"ID: {message.id} - {message.timestamp} - "
                         f"{message.first_name} {message.last_name}"
                         f" (@{message.username}): {message.message_text}"
                         f" - Phone: {message.phone_number}\n")
        await update.message.reply_text(response)


def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("messages", messages))

    application.run_polling()


if __name__ == "__main__":
    main()
