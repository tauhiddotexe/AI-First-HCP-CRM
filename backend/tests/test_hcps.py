import pytest
from unittest.mock import patch

from httpx import ASGITransport, AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_list_hcps_empty():
    with patch('app.api.v1.hcps.HCPService.list_hcps', return_value=([], 0)):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url='http://test') as client:
            response = await client.get('/api/v1/hcps')
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_list_hcps_with_data():
    mock_hcp = {
        'id': 'hcp-1',
        'first_name': 'John',
        'last_name': 'Smith',
        'title': 'Dr.',
        'specialization': 'Cardiology',
        'hospital': 'General Hospital',
        'city': 'NYC',
        'phone': '555-0100',
        'email': 'john.smith@hospital.com',
        'created_at': '2024-01-01T00:00:00Z',
    }
    mock_hcp_obj = type('HCP', (), {k: v for k, v in mock_hcp.items()})()

    with patch(
        'app.api.v1.hcps.HCPService.list_hcps',
        return_value=([mock_hcp_obj], 1),
    ):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url='http://test') as client:
            response = await client.get('/api/v1/hcps')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_hcp_not_found():
    with patch('app.api.v1.hcps.HCPService.get_hcp', return_value=None):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url='http://test') as client:
            response = await client.get('/api/v1/hcps/nonexistent')
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_hcp_found():
    mock_hcp = type('HCP', (), {
        'id': 'hcp-1',
        'first_name': 'John',
        'last_name': 'Smith',
        'title': 'Dr.',
        'specialization': 'Cardiology',
        'hospital': 'General Hospital',
        'city': 'NYC',
        'phone': '555-0100',
        'email': 'john.smith@hospital.com',
        'created_at': '2024-01-01T00:00:00Z',
    })()

    with patch('app.api.v1.hcps.HCPService.get_hcp', return_value=mock_hcp):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url='http://test') as client:
            response = await client.get('/api/v1/hcps/hcp-1')
    assert response.status_code == 200
    data = response.json()
    assert data['first_name'] == 'John'
    assert data['id'] == 'hcp-1'


@pytest.mark.asyncio
async def test_create_hcp():
    mock_hcp = type('HCP', (), {
        'id': 'hcp-new',
        'first_name': 'Jane',
        'last_name': 'Doe',
        'title': 'Dr.',
        'specialization': 'Neurology',
        'hospital': 'City Hospital',
        'city': 'LA',
        'phone': '555-0200',
        'email': 'jane.doe@hospital.com',
        'created_at': '2024-01-01T00:00:00Z',
    })()

    with patch('app.api.v1.hcps.HCPService.create_hcp', return_value=mock_hcp):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url='http://test') as client:
            response = await client.post(
                '/api/v1/hcps',
                json={
                    'first_name': 'Jane',
                    'last_name': 'Doe',
                    'specialization': 'Neurology',
                },
            )
    assert response.status_code == 201
    data = response.json()
    assert data['first_name'] == 'Jane'
    assert data['id'] == 'hcp-new'
