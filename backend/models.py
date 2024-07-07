from sqlalchemy import String, DateTime, Integer, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    threads = relationship('Thread', back_populates='user')

    messages = relationship('Message', back_populates='sender')

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}"


class Thread(Base):
    __tablename__ = 'thread'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    user = relationship("User", back_populates="threads")
    
    messages = relationship("Message", back_populates="thread")

    def __repr__(self) -> str:
        return f"Thread(id={self.id!r}, user_id={self.user_id!r}, created_at={self.created_at!r})"


class Message(Base):
    __tablename__ = 'message'

    id: Mapped[int] = mapped_column(primary_key=True)
    thread_id: Mapped[int] = mapped_column(Integer, ForeignKey("thread.id"))
    content: Mapped[str] = mapped_column(String)
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    thread = relationship("Thread", back_populates="messages")

    sender = relationship('User', back_populates='messages')

    def __repr__(self) -> str:
        return f"Message(id={self.id!r}, thread_id={self.thread_id!r}, content={self.content!r}, sender_id={self.sender_id!r}, created_at={self.created_at!r})"