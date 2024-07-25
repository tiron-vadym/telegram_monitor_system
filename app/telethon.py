import os
from datetime import datetime, timezone

from telethon import TelegramClient, events
from telethon.tl.types import User
from sqlalchemy import Column, Integer, String, Text, DateTime
import asyncio
from dotenv import load_dotenv

from db import AsyncSessionLocal, Base

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")

client = TelegramClient("session", API_ID, API_HASH)


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, unique=True, nullable=False)
    sender_id = Column(Integer)
    message_text = Column(Text)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    phone_number = Column(String)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))


@client.on(events.NewMessage)
async def handler(event: events.NewMessage.Event) -> None:
    if isinstance(event.chat, User):
        message = event.message
        sender = await message.get_sender()

        new_message = Message(
            message_id=message.id,
            sender_id=sender.id,
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


async def main() -> None:
    await client.start(PHONE_NUMBER)
    print("Client is running...")
    await client.run_until_disconnected()


asyncio.run(main())
