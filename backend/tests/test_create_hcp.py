import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.models.base import Base
from app.models.hcp import HCP
from app.repositories.hcp import HCPRepository
from app.tools.create_hcp import execute_create_hcp


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine('sqlite+aiosqlite:///:memory:', echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as s:
        yield s
    await engine.dispose()


@pytest_asyncio.fixture
async def repo(session: AsyncSession):
    return HCPRepository(session)


@pytest.mark.asyncio
async def test_find_all_by_name_exact_match(repo: HCPRepository):
    await repo.create(first_name='John', last_name='Smith', title='Dr.')
    results = await repo.find_all_by_name('Dr. John Smith')
    assert len(results) == 1
    assert results[0].first_name == 'John'
    assert results[0].last_name == 'Smith'


@pytest.mark.asyncio
async def test_find_all_by_name_last_name_only(repo: HCPRepository):
    await repo.create(first_name='John', last_name='Smith', title='Dr.')
    await repo.create(first_name='Jane', last_name='Smith', title='Dr.')
    results = await repo.find_all_by_name('Dr. Smith')
    assert len(results) == 2


@pytest.mark.asyncio
async def test_find_all_by_name_no_match(repo: HCPRepository):
    results = await repo.find_all_by_name('Dr. Nonexistent')
    assert len(results) == 0


@pytest.mark.asyncio
async def test_find_all_by_name_returns_by_last_name(repo: HCPRepository):
    await repo.create(first_name='John', last_name='Smith', title='Dr.')
    await repo.create(first_name='Jane', last_name='Doe', title='Dr.')
    results = await repo.find_all_by_name('Smith')
    assert len(results) == 1
    assert results[0].last_name == 'Smith'


@pytest.mark.asyncio
async def test_execute_create_hcp_new(session: AsyncSession):
    result = await execute_create_hcp(session, {'hcp_name': 'Dr. Michael Brown'})
    assert result['status'] == 'created'
    assert 'Michael Brown' in result['hcp_name']
    assert 'hcp_id' in result


@pytest.mark.asyncio
async def test_execute_create_hcp_existing(session: AsyncSession, repo: HCPRepository):
    await repo.create(first_name='Michael', last_name='Brown', title='Dr.')
    result = await execute_create_hcp(session, {'hcp_name': 'Dr. Michael Brown'})
    assert result['status'] == 'exists'
    assert 'hcp_id' in result


@pytest.mark.asyncio
async def test_execute_create_hcp_multiple_matches(session: AsyncSession, repo: HCPRepository):
    await repo.create(first_name='Michael', last_name='Brown', title='Dr.')
    await repo.create(first_name='Mike', last_name='Brown', title='Dr.')
    result = await execute_create_hcp(session, {'hcp_name': 'Dr. Brown'})
    assert 'error' in result
    assert 'similar HCPs' in result['error']
    assert 'multiple_matches' in result


@pytest.mark.asyncio
async def test_execute_create_hcp_missing_name(session: AsyncSession):
    result = await execute_create_hcp(session, {})
    assert 'error' in result


@pytest.mark.asyncio
async def test_execute_create_hcp_with_hospital(session: AsyncSession):
    result = await execute_create_hcp(session, {
        'hcp_name': 'Dr. Sarah Wilson',
        'hcp_hospital': 'City Medical Center',
    })
    assert result['status'] == 'created'
    repo = HCPRepository(session)
    hcp = await repo.get(result['hcp_id'])
    assert hcp is not None
    assert hcp.hospital == 'City Medical Center'
    assert hcp.title == 'Dr.'
