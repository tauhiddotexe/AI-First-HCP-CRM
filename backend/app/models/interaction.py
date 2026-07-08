from datetime import date, time
from sqlalchemy import Date, ForeignKey, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel


class Interaction(BaseModel):
    __tablename__ = 'interactions'

    hcp_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey('hcps.id', ondelete='CASCADE'),
        nullable=False,
    )
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )
    interaction_type: Mapped[str] = mapped_column(String(100), nullable=False)
    interaction_date: Mapped[date] = mapped_column(Date, nullable=False)
    interaction_time: Mapped[time | None] = mapped_column(Time, nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    sentiment: Mapped[str | None] = mapped_column(String(50), nullable=True)
    outcome: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default='completed')

    hcp = relationship('HCP', backref='interactions')
    discussion_topics = relationship('DiscussionTopic', back_populates='interaction', cascade='all, delete-orphan')
    products_discussed = relationship('ProductDiscussed', back_populates='interaction', cascade='all, delete-orphan')
    materials_shared = relationship('MaterialShared', back_populates='interaction', cascade='all, delete-orphan')
    samples_distributed = relationship('SampleDistributed', back_populates='interaction', cascade='all, delete-orphan')
    follow_ups = relationship('FollowUp', back_populates='interaction', cascade='all, delete-orphan')
    chat_messages = relationship('ChatMessage', back_populates='interaction', cascade='all, delete-orphan')
