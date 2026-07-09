from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.hcp import HCPRepository


async def execute_create_hcp(session: AsyncSession, entities: dict) -> dict:
    hcp_repo = HCPRepository(session)
    hcp_name = entities.get('hcp_name', '')

    if not hcp_name:
        return {'error': 'No HCP name provided. Please specify a name to create a new HCP profile.'}

    cleaned = hcp_name.replace('Dr. ', '').replace('Dr ', '').strip()
    parts = cleaned.split(' ', 1)
    first_name = parts[0] if parts else ''
    last_name = parts[1] if len(parts) > 1 else ''

    missing_name = not first_name and not last_name
    one_word = bool(first_name) and not last_name

    existing = await hcp_repo.find_all_by_name(hcp_name)

    if len(existing) > 1:
        names = [f'{h.first_name} {h.last_name}' for h in existing]
        return {
            'error': f'I found {len(existing)} similar HCPs: {", ".join(names)}. Which one did you mean?',
            'multiple_matches': names,
        }

    if len(existing) == 1:
        hcp = existing[0]
        return {
            'hcp_id': str(hcp.id),
            'hcp_name': f'{hcp.first_name} {hcp.last_name}',
            'title': hcp.title or '',
            'hospital': hcp.hospital or '',
            'status': 'exists',
        }

    if missing_name:
        return {'error': 'Could not parse a valid HCP name. Please provide a first and last name.'}

    hcp = await hcp_repo.create(
        first_name=first_name,
        last_name=last_name,
        title='Dr.',
        hospital=entities.get('hcp_hospital'),
    )

    return {
        'hcp_id': str(hcp.id),
        'hcp_name': f'{hcp.first_name} {hcp.last_name}',
        'title': hcp.title or '',
        'hospital': hcp.hospital or '',
        'status': 'created',
    }
