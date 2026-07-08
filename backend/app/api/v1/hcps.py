from fastapi import APIRouter, Depends, Query
from app.services.hcp_service import HCPService
from app.schemas.hcp import HCPCreate, HCPUpdate, HCPResponse
from app.schemas.common import SuccessResponse
from app.core.exceptions import NotFoundError

router = APIRouter(prefix='/hcps', tags=['HCPs'])


@router.get('')
async def list_hcps(
    search: str | None = Query(None),
    service: HCPService = Depends(),
):
    if search:
        hcps = await service.search_hcps(search)
    else:
        hcps, _ = await service.list_hcps()
    return [HCPResponse.model_validate(h) for h in hcps]


@router.get('/{hcp_id}')
async def get_hcp(hcp_id: str, service: HCPService = Depends()):
    hcp = await service.get_hcp(hcp_id)
    if not hcp:
        raise NotFoundError('HCP not found')
    return HCPResponse.model_validate(hcp)


@router.post('', status_code=201)
async def create_hcp(data: HCPCreate, service: HCPService = Depends()):
    hcp = await service.create_hcp(data)
    return HCPResponse.model_validate(hcp)


@router.patch('/{hcp_id}')
async def update_hcp(hcp_id: str, data: HCPUpdate, service: HCPService = Depends()):
    hcp = await service.update_hcp(hcp_id, data)
    if not hcp:
        raise NotFoundError('HCP not found')
    return HCPResponse.model_validate(hcp)
