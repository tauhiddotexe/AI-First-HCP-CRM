import uuid
from datetime import date, datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.interaction import InteractionRepository
from app.repositories.hcp import HCPRepository
from app.models.interaction import Interaction
from app.models.discussion_topic import DiscussionTopic
from app.models.product_discussed import ProductDiscussed
from app.models.material_shared import MaterialShared
from app.models.sample_distributed import SampleDistributed
from app.models.follow_up import FollowUp


async def execute_log_interaction(
    session: AsyncSession,
    entities: dict,
    user_id: str,
) -> dict:
    hcp_repo = HCPRepository(session)
    interaction_repo = InteractionRepository(session)

    hcp_name = entities.get('hcp_name', '')
    matched_hcp = await hcp_repo.find_by_name(hcp_name) if hcp_name else None

    if not matched_hcp:
        return {'error': f'HCP "{hcp_name}" not found. Please ask the user to select from the HCP list.'}

    interaction_date = entities.get('date')
    if not interaction_date:
        interaction_date = date.today().isoformat()

    interaction = Interaction(
        hcp_id=matched_hcp.id,
        user_id=user_id,
        interaction_type=entities.get('interaction_type', 'Face-to-Face'),
        interaction_date=date.fromisoformat(interaction_date),
        summary=entities.get('summary', ''),
        sentiment=entities.get('sentiment'),
        outcome=entities.get('outcome'),
        status='completed',
    )
    session.add(interaction)
    await session.flush()

    for topic in (entities.get('discussion_topics') or []):
        session.add(DiscussionTopic(interaction_id=interaction.id, topic=topic if isinstance(topic, str) else topic.get('topic', '')))

    for product in (entities.get('products_discussed') or []):
        name = product if isinstance(product, str) else product.get('product_name', '')
        session.add(ProductDiscussed(interaction_id=interaction.id, product_name=name))

    for material in (entities.get('materials_shared') or []):
        session.add(MaterialShared(
            interaction_id=interaction.id,
            material_name=material.get('material_name', ''),
            quantity=material.get('quantity', 1),
        ))

    for sample in (entities.get('samples_distributed') or []):
        session.add(SampleDistributed(
            interaction_id=interaction.id,
            product_name=sample.get('product_name', ''),
            quantity=sample.get('quantity', 1),
        ))

    for fu in (entities.get('follow_up_actions') or []):
        fu_date = None
        if fu.get('follow_up_date'):
            fu_date = date.fromisoformat(fu['follow_up_date'])
        session.add(FollowUp(
            interaction_id=interaction.id,
            action=fu.get('action', ''),
            follow_up_date=fu_date,
            status='pending',
        ))

    await session.commit()
    await session.refresh(interaction)

    return {
        'interaction_id': interaction.id,
        'hcp': f'{matched_hcp.first_name} {matched_hcp.last_name}',
        'date': interaction_date,
        'type': interaction.interaction_type,
        'sentiment': interaction.sentiment,
        'status': 'created',
    }
