from datetime import date
from sqlalchemy import Date, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel


class FollowUp(BaseModel):
    __tablename__ = 'follow_ups'

    interaction_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey('interactions.id', ondelete='CASCADE'),
        nullable=False,
    )
    follow_up_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    action: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default='pending')

    interaction = relationship('Interaction', back_populates='follow_ups')
