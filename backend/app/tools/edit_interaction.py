from datetime import date
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.hcp import HCP
from app.models.interaction import Interaction
from app.models.discussion_topic import DiscussionTopic
from app.models.product_discussed import ProductDiscussed
from app.models.material_shared import MaterialShared
from app.models.sample_distributed import SampleDistributed
from app.models.follow_up import FollowUp
from app.repositories.interaction import InteractionRepository
from app.repositories.hcp import HCPRepository


def _ensure_list(val, default=None):
    if val is None:
        return default or []
    if isinstance(val, list):
        return val
    if isinstance(val, str):
        return [s.strip() for s in val.replace(' and ', ',').split(',') if s.strip()]
    return [str(val)]


async def _load_existing(interaction_id: str, session: AsyncSession, model: type) -> set:
    result = await session.execute(select(model).where(model.interaction_id == interaction_id))
    return {r.topic if hasattr(r, 'topic') else r.product_name if hasattr(r, 'product_name') else r.material_name if hasattr(r, 'material_name') else r.action for r in result.scalars().all()}


async def execute_edit_interaction(
    session: AsyncSession,
    interaction_id: str,
    entities: dict,
) -> dict:
    repo = InteractionRepository(session)
    interaction = None

    if interaction_id:
        interaction = await repo.get(interaction_id)

    if not interaction:
        hcp_name = entities.get('hcp_name', '')
        if hcp_name:
            hcp = await HCPRepository(session).find_by_name(hcp_name)
            if hcp:
                stmt = (
                    select(Interaction)
                    .where(Interaction.hcp_id == hcp.id, Interaction.deleted_at.is_(None))
                    .order_by(desc(Interaction.created_at))
                    .limit(1)
                )
                result = await session.execute(stmt)
                interaction = result.scalar_one_or_none()

    if not interaction:
        return {'error': 'No interaction found to edit. Please specify an HCP name or provide an interaction ID.'}

    interaction_id = str(interaction.id)
    scalar_updates = {}
    list_updates = {}

    hcp_resolved = await session.execute(select(HCP).where(HCP.id == interaction.hcp_id))
    hcp_obj = hcp_resolved.scalar_one_or_none()
    hcp_name_resolved = f'Dr. {hcp_obj.first_name} {hcp_obj.last_name}' if hcp_obj else ''

    raw_date = entities.get('date')
    if raw_date:
        try:
            scalar_updates['interaction_date'] = date.fromisoformat(raw_date)
        except (ValueError, TypeError):
            pass
    if entities.get('interaction_type'):
        scalar_updates['interaction_type'] = entities['interaction_type']
    if entities.get('sentiment'):
        scalar_updates['sentiment'] = entities['sentiment']
    if entities.get('summary'):
        scalar_updates['summary'] = entities['summary']
    if entities.get('outcome'):
        scalar_updates['outcome'] = entities['outcome']

    if scalar_updates:
        for key, value in scalar_updates.items():
            setattr(interaction, key, value)

    existing_topics = await _load_existing(interaction_id, session, DiscussionTopic)
    new_topics = [t for t in _ensure_list(entities.get('discussion_topics')) if t not in existing_topics]
    for topic in new_topics:
        session.add(DiscussionTopic(interaction_id=interaction.id, topic=topic))
    if new_topics:
        list_updates['discussion_topics'] = new_topics

    existing_products = await _load_existing(interaction_id, session, ProductDiscussed)
    new_products = [p for p in _ensure_list(entities.get('products_discussed')) if p not in existing_products]
    for product in new_products:
        session.add(ProductDiscussed(interaction_id=interaction.id, product_name=product))
    if new_products:
        list_updates['products_discussed'] = new_products

    existing_materials = await _load_existing(interaction_id, session, MaterialShared)
    for material in (entities.get('materials_shared') or []):
        name = material if isinstance(material, str) else material.get('material_name', '')
        if name and name not in existing_materials:
            qty = 1 if isinstance(material, str) else material.get('quantity', 1)
            session.add(MaterialShared(interaction_id=interaction.id, material_name=name, quantity=qty))
    new_material_names = [
        m if isinstance(m, str) else m.get('material_name', '')
        for m in (entities.get('materials_shared') or [])
    ]
    new_materials = [n for n in new_material_names if n and n not in existing_materials]
    if new_materials:
        list_updates['materials_shared'] = new_materials

    existing_samples = await _load_existing(interaction_id, session, SampleDistributed)
    for sample in (entities.get('samples_distributed') or []):
        name = sample if isinstance(sample, str) else sample.get('product_name', '')
        if name and name not in existing_samples:
            qty = 1 if isinstance(sample, str) else sample.get('quantity', 1)
            session.add(SampleDistributed(interaction_id=interaction.id, product_name=name, quantity=qty))
    new_sample_names = [
        s if isinstance(s, str) else s.get('product_name', '')
        for s in (entities.get('samples_distributed') or [])
    ]
    new_samples = [n for n in new_sample_names if n and n not in existing_samples]
    if new_samples:
        list_updates['samples_distributed'] = new_samples

    existing_followups = await _load_existing(interaction_id, session, FollowUp)
    for fu in (entities.get('follow_up_actions') or []):
        action = fu.get('action', '')
        if action and action not in existing_followups:
            fu_date = None
            if fu.get('follow_up_date'):
                try:
                    fu_date = date.fromisoformat(fu['follow_up_date'])
                except (ValueError, TypeError):
                    fu_date = None
            session.add(FollowUp(
                interaction_id=interaction.id,
                action=action,
                follow_up_date=fu_date,
                status='pending',
            ))
    new_fu_actions = [f.get('action', '') for f in (entities.get('follow_up_actions') or [])]
    new_fus = [a for a in new_fu_actions if a and a not in existing_followups]
    if new_fus:
        list_updates['follow_up_actions'] = new_fus

    if scalar_updates or list_updates:
        await session.commit()

    all_updated = list(scalar_updates.keys()) + list(list_updates.keys())

    return {
        'interaction_id': interaction_id,
        'updated_fields': all_updated,
        'status': 'updated',
        'hcp_name': hcp_name_resolved,
    }
