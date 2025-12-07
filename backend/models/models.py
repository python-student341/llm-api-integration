from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from backend.database.database import Base


class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    password: Mapped[str]

    chat = relationship('ChatRequest', back_populates='user', cascade='all, delete-orphan')

class ChatRequest(Base):
    __tablename__ = 'chat_requests'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    prompt: Mapped[str]
    answer: Mapped[str]

    user = relationship('UserModel', back_populates='chat')