from datetime import date
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_session
from app.repositories.interaction import InteractionRepository
from app.schemas.interaction import InteractionCreate, InteractionUpdate
from app.models.interaction import Interaction


class InteractionService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.repo = InteractionRepository(session)

    async def list_interactions(
        self,
        user_id: str | None = None,
        hcp_id: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        interaction_type: str | None = None,
        page: int = 1,
        limit: int = 20,
    ):
        return await self.repo.list_filtered(
            user_id=user_id,
            hcp_id=hcp_id,
            date_from=date_from,
            date_to=date_to,
            interaction_type=interaction_type,
            page=page,
            limit=limit,
        )

    async def get_interaction(self, interaction_id: str):
        return await self.repo.get(interaction_id)

    async def create_interaction(self, data: InteractionCreate, user_id: str) -> Interaction:
        interaction_data = data.model_dump(exclude={'discussion_topics', 'products_discussed', 'materials_shared', 'samples_distributed', 'follow_ups'})
        interaction_data['user_id'] = user_id

        interaction = await self.repo.create(**interaction_data)

        if data.discussion_topics:
            from app.models.discussion_topic import DiscussionTopic
            for topic in data.discussion_topics:
                self.repo.session.add(DiscussionTopic(interaction_id=interaction.id, topic=topic.topic))

        if data.products_discussed:
            from app.models.product_discussed import ProductDiscussed
            for product in data.products_discussed:
                self.repo.session.add(ProductDiscussed(interaction_id=interaction.id, product_name=product.product_name))

        if data.materials_shared:
            from app.models.material_shared import MaterialShared
            for material in data.materials_shared:
                self.repo.session.add(MaterialShared(interaction_id=interaction.id, material_name=material.material_name, quantity=material.quantity))

        if data.samples_distributed:
            from app.models.sample_distributed import SampleDistributed
            for sample in data.samples_distributed:
                self.repo.session.add(SampleDistributed(interaction_id=interaction.id, product_name=sample.product_name, quantity=sample.quantity))

        if data.follow_ups:
            from app.models.follow_up import FollowUp
            for fu in data.follow_ups:
                self.repo.session.add(FollowUp(interaction_id=interaction.id, action=fu.action, follow_up_date=fu.follow_up_date, status=fu.status))

        await self.repo.session.commit()
        await self.repo.session.refresh(interaction)
        return interaction

    async def update_interaction(self, interaction_id: str, data: InteractionUpdate):
        update_data = data.model_dump(exclude_none=True, exclude={'discussion_topics', 'products_discussed', 'materials_shared', 'samples_distributed', 'follow_ups'})
        return await self.repo.update(interaction_id, **update_data)

    async def delete_interaction(self, interaction_id: str):
        return await self.repo.delete(interaction_id)
