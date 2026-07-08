import pytest
from unittest.mock import patch

from httpx import ASGITransport, AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_list_interactions_empty():
    with patch('app.api.v1.interactions.InteractionService.list_interactions', return_value=([], 0)):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url='http://test') as client:
            response = await client.get('/api/v1/interactions')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_interaction():
    mock = type('Interaction', (), {'id': 'int-1', 'status': 'created'})()
    with patch('app.api.v1.interactions.InteractionService.create_interaction', return_value=mock):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url='http://test') as client:
            response = await client.post(
                '/api/v1/interactions',
                json={
                    'hcp_id': 'hcp-1',
                    'interaction_type': 'Face-to-Face',
                    'interaction_date': '2024-06-15',
                },
            )
    assert response.status_code == 201
    data = response.json()
    assert data['data']['id'] == 'int-1'
    assert data['success'] is True


@pytest.mark.asyncio
async def test_get_interaction_not_found():
    with patch('app.api.v1.interactions.InteractionService.get_interaction', return_value=None):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url='http://test') as client:
            response = await client.get('/api/v1/interactions/nonexistent')
    assert response.status_code == 404
