from sqlalchemy import Column, Integer, String, Text, DateTime
from db import Base


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, unique=True, nullable=False)
    message_text = Column(Text)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    phone_number = Column(String)
    timestamp = Column(DateTime(timezone=True))
