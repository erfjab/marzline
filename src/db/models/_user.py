import asyncio
from datetime import datetime
from typing import Optional, Union

from sqlalchemy import String, Integer, DateTime, BigInteger
from sqlalchemy.orm import mapped_column, Mapped, Session
from eiogram.types import User as EioUser, Message, CallbackQuery

from src.config import TELEGRAM_ADMIN_IDS, BOT
from src.utils import hour_difference
from ..core import Base, GetDB


class UserMessage(Base):
    __tablename__ = "user_messages"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, index=True)
    message_id: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now())


class User(Base):
    __tablename__ = "users"

    chat_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(256), nullable=False)
    username: Mapped[str] = mapped_column(String(128), nullable=True)
    join_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now())
    online_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now())

    @property
    def is_owner(self) -> bool:
        return self.chat_id in TELEGRAM_ADMIN_IDS

    def format(self) -> dict:
        return {
            "chat_id": self.chat_id,
            "full_name": self.full_name,
            "username": self.username,
        }

    @classmethod
    def get(cls, db: Session, *, chat_id: int) -> Optional["User"]:
        """Get a user with chatid"""
        return db.query(cls).filter(cls.chat_id == chat_id).first()

    @classmethod
    def get_all(cls, db: Session) -> Optional["User"]:
        """Get all users"""
        query = db.query(cls)
        return query.all()

    @classmethod
    def upsert(cls, db: Session, *, user: EioUser) -> Optional["User"]:
        """Upsert user"""
        dbuser = cls.get(db, chat_id=user.id)
        if dbuser:
            dbuser.full_name = user.full_name
            dbuser.username = user.username
            dbuser.online_at = datetime.now()
        else:
            dbuser = cls(
                chat_id=user.id,
                username=user.username,
                full_name=user.full_name,
                online_at=datetime.now(),
            )
            db.add(dbuser)

        db.commit()
        db.refresh(dbuser)
        return dbuser

    @classmethod
    def add_message(cls, db: Session, update: Union[Message, CallbackQuery]) -> None:
        """add a user message"""

        def add(db: Session, update: Union[Message, CallbackQuery]):
            message = update.message if isinstance(update, CallbackQuery) else update
            user_message = UserMessage(
                chat_id=message.chat.id, message_id=message.message_id
            )
            db.add(user_message)
            db.commit()

        if db:
            add(db, update)
        else:
            with GetDB() as db:
                add(db, update)

    @classmethod
    def clear_messages(cls, db: Session, update: Union[Message, CallbackQuery]):
        """Clear all user message"""

        def clear(db: Session, update: Union[Message, CallbackQuery]):
            message = update.message if isinstance(update, CallbackQuery) else update
            chat_id = message.chat.id
            user_messages = (
                db.query(UserMessage).filter(UserMessage.chat_id == chat_id).all()
            )
            try:
                now = datetime.now()
                asyncio.create_task(
                    BOT.delete_messages(
                        chat_id=chat_id,
                        message_ids=[
                            msg.message_id
                            for msg in user_messages
                            if hour_difference(msg.created_at, now) < 48
                        ],
                    )
                )
            except Exception:
                pass
            db.query(UserMessage).filter(UserMessage.chat_id == chat_id).delete()
            cls.add_message(db, update)

        if db:
            clear(db, update)
        else:
            with GetDB() as db:
                clear(db, update)
