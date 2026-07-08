import pytest
import pytest_asyncio
from datetime import datetime
from sqlalchemy import DateTime, String, func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.repositories.base import BaseRepository


class RepoModel(DeclarativeBase):
    pass


class RepoItem(RepoModel):
    __tablename__ = 'test_items'

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine('sqlite+aiosqlite:///:memory:', echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(RepoItem.metadata.create_all)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as s:
        yield s
    await engine.dispose()


@pytest_asyncio.fixture
async def repo(session: AsyncSession):
    return BaseRepository(session, RepoItem)


@pytest.mark.asyncio
async def test_create(repo: BaseRepository):
    item = await repo.create(id='1', name='Test Item')
    assert item.id == '1'
    assert item.name == 'Test Item'


@pytest.mark.asyncio
async def test_get_returns_none_for_missing(repo: BaseRepository):
    item = await repo.get('nonexistent')
    assert item is None


@pytest.mark.asyncio
async def test_get_returns_item(repo: BaseRepository):
    await repo.create(id='1', name='Test Item')
    item = await repo.get('1')
    assert item is not None
    assert item.id == '1'
    assert item.name == 'Test Item'


@pytest.mark.asyncio
async def test_list_empty(repo: BaseRepository):
    items, total = await repo.list()
    assert items == []
    assert total == 0


@pytest.mark.asyncio
async def test_list_with_items(repo: BaseRepository):
    await repo.create(id='1', name='Item A')
    await repo.create(id='2', name='Item B')
    items, total = await repo.list()
    assert len(items) == 2
    assert total == 2


@pytest.mark.asyncio
async def test_list_with_limit(repo: BaseRepository):
    await repo.create(id='1', name='Item A')
    await repo.create(id='2', name='Item B')
    items, total = await repo.list(limit=1)
    assert len(items) == 1
    assert total == 2


@pytest.mark.asyncio
async def test_update(repo: BaseRepository):
    await repo.create(id='1', name='Original')
    updated = await repo.update('1', name='Updated')
    assert updated is not None
    assert updated.name == 'Updated'


@pytest.mark.asyncio
async def test_update_nonexistent(repo: BaseRepository):
    item = await repo.update('nonexistent', name='Updated')
    assert item is None


@pytest.mark.asyncio
async def test_delete(repo: BaseRepository):
    await repo.create(id='1', name='Test Item')
    result = await repo.delete('1')
    assert result is True
    item = await repo.get('1')
    assert item is None


@pytest.mark.asyncio
async def test_delete_nonexistent(repo: BaseRepository):
    result = await repo.delete('nonexistent')
    assert result is False
