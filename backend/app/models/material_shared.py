from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel


class MaterialShared(BaseModel):
    __tablename__ = 'materials_shared'

    interaction_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey('interactions.id', ondelete='CASCADE'),
        nullable=False,
    )
    material_name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    interaction = relationship('Interaction', back_populates='materials_shared')
