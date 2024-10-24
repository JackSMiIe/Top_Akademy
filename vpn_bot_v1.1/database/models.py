from sqlalchemy import String, Boolean, DateTime, Text, func, Integer, DECIMAL,LargeBinary
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Базовый класс с полями для отслеживания времени создания и обновления
class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


# Класс продукта
class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(15), nullable=False)
    price: Mapped[float] = mapped_column(DECIMAL(10,2), nullable=False)


# Класс пользователя
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String(255), nullable=True)
    status: Mapped[bool] = mapped_column(Boolean, default=False)  # Исправлено: явное указание типа данных
    subscription_start: Mapped[DateTime] = mapped_column(DateTime, nullable=True)  # Дата начала подписки
    subscription_end: Mapped[DateTime] = mapped_column(DateTime, nullable=True)  # Дата окончания подписки

    config_file: Mapped[str] = mapped_column(Text, nullable=True)  # Содержимое config.conf
    qr_code: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)  # Поле для хранения QR-кода в бинарном виде
