import os

from telethon import TelegramClient, events
from telethon.tl.types import User
from dotenv import load_dotenv
from db import AsyncSessionLocal
from app.models import Message

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")

client = TelegramClient("session", API_ID, API_HASH)


@client.on(events.NewMessage)
async def handler(event: events.NewMessage.Event) -> None:
    if isinstance(event.chat, User):
        message = event.message
        sender = await message.get_sender()

        new_message = Message(
            message_id=message.id,
            message_text=message.text,
            first_name=sender.first_name,
            last_name=sender.last_name,
            username=sender.username,
            phone_number=sender.phone,
            timestamp=message.date
        )
        async with AsyncSessionLocal() as session:
            async with session.begin():
                session.add(new_message)
                await session.commit()


def main() -> None:
    client.start(PHONE_NUMBER)
    print("Client is running...")
    client.run_until_disconnected()


if __name__ == "__main__":
    main()
