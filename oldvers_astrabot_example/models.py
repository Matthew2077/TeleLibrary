from datetime import datetime
from sqlalchemy import String, DateTime, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Item(Base):
    """
    Un semplice "task/nota" associato all'utente Telegram che l'ha creato.
    Ogni utente vede e gestisce solo i propri elementi.
    """
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)  # id Telegram dell'utente
    title: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return f"<Item id={self.id} title={self.title!r}>"
