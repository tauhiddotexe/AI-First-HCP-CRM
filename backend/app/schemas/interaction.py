from datetime import date, datetime, time
from pydantic import BaseModel


class DiscussionTopicSchema(BaseModel):
    topic: str


class ProductDiscussedSchema(BaseModel):
    product_name: str


class MaterialSharedSchema(BaseModel):
    material_name: str
    quantity: int = 1


class SampleDistributedSchema(BaseModel):
    product_name: str
    quantity: int = 1


class FollowUpSchema(BaseModel):
    follow_up_date: date | None = None
    action: str
    status: str = 'pending'


class InteractionCreate(BaseModel):
    hcp_id: str
    interaction_type: str
    interaction_date: date
    interaction_time: time | None = None
    location: str | None = None
    summary: str | None = None
    sentiment: str | None = None
    outcome: str | None = None
    discussion_topics: list[DiscussionTopicSchema] | None = None
    products_discussed: list[ProductDiscussedSchema] | None = None
    materials_shared: list[MaterialSharedSchema] | None = None
    samples_distributed: list[SampleDistributedSchema] | None = None
    follow_ups: list[FollowUpSchema] | None = None


class InteractionUpdate(BaseModel):
    interaction_type: str | None = None
    interaction_date: date | None = None
    interaction_time: time | None = None
    location: str | None = None
    summary: str | None = None
    sentiment: str | None = None
    outcome: str | None = None
    status: str | None = None
    discussion_topics: list[DiscussionTopicSchema] | None = None
    products_discussed: list[ProductDiscussedSchema] | None = None
    materials_shared: list[MaterialSharedSchema] | None = None
    samples_distributed: list[SampleDistributedSchema] | None = None
    follow_ups: list[FollowUpSchema] | None = None
