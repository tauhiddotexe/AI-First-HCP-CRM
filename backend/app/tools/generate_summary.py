from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.interaction import Interaction
from app.repositories.hcp import HCPRepository


async def execute_generate_summary(
    session: AsyncSession | None = None,
    hcp_name: str = '',
) -> dict:
    if not session or not hcp_name:
        return {'summary': 'No interaction data available to generate summary.'}

    hcp = await HCPRepository(session).find_by_name(hcp_name)
    if not hcp:
        return {'summary': f'No HCP found for "{hcp_name}".'}

    result = await session.execute(
        select(Interaction)
        .options(
            selectinload(Interaction.discussion_topics),
            selectinload(Interaction.products_discussed),
            selectinload(Interaction.materials_shared),
            selectinload(Interaction.samples_distributed),
            selectinload(Interaction.follow_ups),
        )
        .where(Interaction.hcp_id == hcp.id, Interaction.deleted_at.is_(None))
        .order_by(desc(Interaction.interaction_date), desc(Interaction.created_at))
        .limit(1)
    )
    ix = result.scalar_one_or_none()
    if not ix:
        return {'summary': f'No interactions found for {hcp.first_name} {hcp.last_name}.'}

    lines = []
    date_str = ix.interaction_date.isoformat() if ix.interaction_date else 'Unknown date'
    hcp_full = f'{hcp.first_name} {hcp.last_name}'
    loc = f' at {ix.location}' if ix.location else ''
    lines.append(f'On {date_str}, you conducted a {ix.interaction_type} with {hcp_full}{loc}.')

    topics = [dt.topic for dt in ix.discussion_topics]
    if topics:
        lines.append(f'You discussed {", ".join(topics)}.')

    products = [pd.product_name for pd in ix.products_discussed]
    if products:
        lines.append(f'Products discussed: {", ".join(products)}.')

    materials = [ms.material_name for ms in ix.materials_shared]
    if materials:
        parts = []
        for ms in ix.materials_shared:
            parts.append(f'{ms.material_name}' + (f' (x{ms.quantity})' if ms.quantity > 1 else ''))
        lines.append(f'Materials shared: {", ".join(parts)}.')

    samples = [sd.product_name for sd in ix.samples_distributed]
    if samples:
        parts = []
        for sd in ix.samples_distributed:
            parts.append(f'{sd.product_name}' + (f' (x{sd.quantity})' if sd.quantity > 1 else ''))
        lines.append(f'Samples distributed: {", ".join(parts)}.')

    if ix.outcome:
        lines.append(f'Outcome: {ix.outcome}.')

    if ix.sentiment:
        lines.append(f'Sentiment: {ix.sentiment}.')

    follow_ups = [fu for fu in ix.follow_ups]
    if follow_ups:
        fu_strs = []
        for fu in follow_ups:
            part = fu.action
            if fu.follow_up_date:
                part += f' (due: {fu.follow_up_date.isoformat()})'
            fu_strs.append(part)
        lines.append(f'Follow-up: {", ".join(fu_strs)}.')

    if ix.summary:
        lines.append(f'Summary: {ix.summary}')

    return {
        'summary': ' '.join(lines),
        'interaction_id': str(ix.id),
    }
