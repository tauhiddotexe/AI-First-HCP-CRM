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


def _ensure_list(val, default=None):
    if val is None:
        return default or []
    if isinstance(val, list):
        return val
    if isinstance(val, str):
        return [s.strip() for s in val.replace(' and ', ',').split(',') if s.strip()]
    return [str(val)]


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

    raw_date = entities.get('date')
    if not raw_date:
        interaction_date = date.today()
    else:
        try:
            interaction_date = date.fromisoformat(raw_date)
        except (ValueError, TypeError):
            interaction_date = date.today()

    interaction = Interaction(
        hcp_id=matched_hcp.id,
        user_id=user_id,
        interaction_type=entities.get('interaction_type', 'Face-to-Face'),
        interaction_date=interaction_date,
        summary=entities.get('summary', ''),
        sentiment=entities.get('sentiment'),
        outcome=entities.get('outcome'),
        status='completed',
    )
    session.add(interaction)
    await session.flush()

    for topic in _ensure_list(entities.get('discussion_topics')):
        session.add(DiscussionTopic(interaction_id=interaction.id, topic=topic if isinstance(topic, str) else topic.get('topic', '')))

    for product in _ensure_list(entities.get('products_discussed')):
        name = product if isinstance(product, str) else product.get('product_name', '')
        session.add(ProductDiscussed(interaction_id=interaction.id, product_name=name))

    for material in (entities.get('materials_shared') or []):
        if isinstance(material, str):
            session.add(MaterialShared(interaction_id=interaction.id, material_name=material, quantity=1))
        else:
            mn = material.get('material_name')
            if mn:
                session.add(MaterialShared(
                    interaction_id=interaction.id,
                    material_name=mn,
                    quantity=material.get('quantity') or 1,
                ))

    for sample in (entities.get('samples_distributed') or []):
        if isinstance(sample, str):
            session.add(SampleDistributed(interaction_id=interaction.id, product_name=sample, quantity=1))
        else:
            pn = sample.get('product_name')
            if pn:
                session.add(SampleDistributed(
                    interaction_id=interaction.id,
                    product_name=pn,
                    quantity=sample.get('quantity') or 1,
                ))

    for fu in (entities.get('follow_up_actions') or []):
        fu_date = None
        if fu.get('follow_up_date'):
            try:
                fu_date = date.fromisoformat(fu['follow_up_date'])
            except (ValueError, TypeError):
                fu_date = None
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
        'date': interaction_date.isoformat(),
        'type': interaction.interaction_type,
        'sentiment': interaction.sentiment,
        'status': 'created',
    }
