from datetime import (
    datetime,
)

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.sql.functions import (
    current_timestamp,
)


class Base(DeclarativeBase):
    pass


class ModelBaseMixin:
    id: Mapped[str] = mapped_column(
        Integer,
        primary_key=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=current_timestamp(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=current_timestamp(),
    )


class Quiz(ModelBaseMixin, Base):
    __tablename__ = 'quiz'

    answer: Mapped[str] = mapped_column(
        String,
    )
    question: Mapped[str] = mapped_column(
        Text,
    )
    value: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
    )
    airdate: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey('category.id'),
    )
    game_id: Mapped[int] = mapped_column(
        Integer,
    )
    category: Mapped['Category'] = relationship(
        back_populates='quiz',
    )


class Category(ModelBaseMixin, Base):
    __tablename__ = 'category'

    title: Mapped[str] = mapped_column(
        String,
    )
    clues_count: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
    )
    quiz: Mapped['Quiz'] = relationship(
        back_populates='category',
    )
