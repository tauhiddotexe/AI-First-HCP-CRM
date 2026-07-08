from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel


class ProductDiscussed(BaseModel):
    __tablename__ = 'products_discussed'

    interaction_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey('interactions.id', ondelete='CASCADE'),
        nullable=False,
    )
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)

    interaction = relationship('Interaction', back_populates='products_discussed')
