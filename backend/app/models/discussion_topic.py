from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel


class DiscussionTopic(BaseModel):
    __tablename__ = 'discussion_topics'

    interaction_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey('interactions.id', ondelete='CASCADE'),
        nullable=False,
    )
    topic: Mapped[str] = mapped_column(Text, nullable=False)

    interaction = relationship('Interaction', back_populates='discussion_topics')
