from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.types import JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseModel


class AIExtractionLog(BaseModel):
    __tablename__ = 'ai_extraction_logs'

    interaction_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey('interactions.id', ondelete='SET NULL'),
        nullable=True,
    )
    extracted_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    processing_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
