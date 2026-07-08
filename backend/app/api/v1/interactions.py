from datetime import date
from fastapi import APIRouter, Depends, Query
from app.services.interaction_service import InteractionService
from app.schemas.interaction import InteractionCreate, InteractionUpdate
from app.schemas.common import SuccessResponse, PaginatedResponse
from app.core.exceptions import NotFoundError
from app.core.dependencies import get_current_user_id

router = APIRouter(prefix='/interactions', tags=['Interactions'])


@router.post('', status_code=201)
async def create_interaction(
    data: InteractionCreate,
    user_id: str = Depends(get_current_user_id),
    service: InteractionService = Depends(),
):
    interaction = await service.create_interaction(data, user_id)
    return SuccessResponse(message='Interaction created', data={'id': interaction.id, 'status': 'created'})


@router.get('')
async def list_interactions(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    hcp: str | None = Query(None),
    date_from: date | None = Query(None),
    date_to: date | None = Query(None),
    interaction_type: str | None = Query(None),
    user_id: str = Depends(get_current_user_id),
    service: InteractionService = Depends(),
):
    items, total = await service.list_interactions(
        user_id=user_id,
        hcp_id=hcp,
        date_from=date_from,
        date_to=date_to,
        interaction_type=interaction_type,
        page=page,
        limit=limit,
    )
    return PaginatedResponse(
        items=[i.to_dict() if hasattr(i, 'to_dict') else {'id': i.id} for i in items],
        page=page,
        limit=limit,
        total=total,
        pages=max(1, (total + limit - 1) // limit),
    )


@router.get('/{interaction_id}')
async def get_interaction(interaction_id: str, service: InteractionService = Depends()):
    interaction = await service.get_interaction(interaction_id)
    if not interaction:
        raise NotFoundError('Interaction not found')
    return interaction


@router.patch('/{interaction_id}')
async def update_interaction(
    interaction_id: str,
    data: InteractionUpdate,
    service: InteractionService = Depends(),
):
    interaction = await service.update_interaction(interaction_id, data)
    if not interaction:
        raise NotFoundError('Interaction not found')
    return SuccessResponse(message='Interaction updated', data={'id': interaction_id})


@router.delete('/{interaction_id}')
async def delete_interaction(interaction_id: str, service: InteractionService = Depends()):
    deleted = await service.delete_interaction(interaction_id)
    if not deleted:
        raise NotFoundError('Interaction not found')
    return SuccessResponse(message='Interaction deleted')
