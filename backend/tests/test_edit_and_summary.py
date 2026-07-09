import pytest
import pytest_asyncio
from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.models.base import Base
from app.models.hcp import HCP
from app.models.interaction import Interaction
from app.models.discussion_topic import DiscussionTopic
from app.models.product_discussed import ProductDiscussed
from app.models.material_shared import MaterialShared
from app.repositories.hcp import HCPRepository
from app.tools.edit_interaction import execute_edit_interaction
from app.tools.generate_summary import execute_generate_summary
from app.tools.log_interaction import execute_log_interaction


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
async def hcp_and_interaction(session: AsyncSession):
    repo = HCPRepository(session)
    hcp = await repo.create(first_name='Jonathan', last_name='Reed', title='Dr.', hospital='City Hospital')
    result = await execute_log_interaction(session, {
        'hcp_name': 'Jonathan Reed',
        'interaction_type': 'Face-to-Face',
        'summary': 'Initial meeting to discuss NeuroVance.',
        'discussion_topics': ['NeuroVance'],
        'products_discussed': ['NeuroVance'],
    }, 'demo-rep-001')
    return hcp, result['interaction_id']


@pytest.mark.asyncio
async def test_edit_adds_discussion_topics(session: AsyncSession, hcp_and_interaction):
    hcp, interaction_id = hcp_and_interaction
    result = await execute_edit_interaction(session, interaction_id, {
        'hcp_name': 'Jonathan Reed',
        'discussion_topics': ['NeuroVance XR'],
    })
    assert result['status'] == 'updated'
    assert 'discussion_topics' in result['updated_fields']

    stmt = select(DiscussionTopic).where(DiscussionTopic.interaction_id == interaction_id)
    rows = (await session.execute(stmt)).scalars().all()
    topics = [r.topic for r in rows]
    assert 'NeuroVance' in topics
    assert 'NeuroVance XR' in topics


@pytest.mark.asyncio
async def test_edit_adds_products(session: AsyncSession, hcp_and_interaction):
    hcp, interaction_id = hcp_and_interaction
    result = await execute_edit_interaction(session, interaction_id, {
        'hcp_name': 'Jonathan Reed',
        'products_discussed': ['NeuroVance XR'],
    })
    assert 'products_discussed' in result['updated_fields']

    stmt = select(ProductDiscussed).where(ProductDiscussed.interaction_id == interaction_id)
    rows = (await session.execute(stmt)).scalars().all()
    products = [r.product_name for r in rows]
    assert 'NeuroVance' in products
    assert 'NeuroVance XR' in products


@pytest.mark.asyncio
async def test_edit_adds_materials(session: AsyncSession, hcp_and_interaction):
    hcp, interaction_id = hcp_and_interaction
    result = await execute_edit_interaction(session, interaction_id, {
        'hcp_name': 'Jonathan Reed',
        'materials_shared': [{'material_name': 'Clinical Brochure', 'quantity': 2}],
    })
    assert 'materials_shared' in result['updated_fields']

    stmt = select(MaterialShared).where(MaterialShared.interaction_id == interaction_id)
    rows = (await session.execute(stmt)).scalars().all()
    names = [r.material_name for r in rows]
    assert 'Clinical Brochure' in names


@pytest.mark.asyncio
async def test_edit_updates_scalar(session: AsyncSession, hcp_and_interaction):
    hcp, interaction_id = hcp_and_interaction
    result = await execute_edit_interaction(session, interaction_id, {
        'hcp_name': 'Jonathan Reed',
        'outcome': 'Positive',
    })
    assert 'outcome' in result['updated_fields']

    stmt = select(Interaction).where(Interaction.id == interaction_id)
    ix = (await session.execute(stmt)).scalar_one()
    assert ix.outcome == 'Positive'


@pytest.mark.asyncio
async def test_summary_includes_all_data(session: AsyncSession, hcp_and_interaction):
    hcp, interaction_id = hcp_and_interaction
    await execute_edit_interaction(session, interaction_id, {
        'hcp_name': 'Jonathan Reed',
        'discussion_topics': ['NeuroVance XR'],
        'products_discussed': ['NeuroVance XR'],
        'materials_shared': [{'material_name': 'Clinical Brochure', 'quantity': 2}],
        'outcome': 'Positive',
        'sentiment': 'Interested',
    })

    result = await execute_generate_summary(session=session, hcp_name='Jonathan Reed')
    summary = result['summary']
    assert 'Face-to-Face' in summary
    assert 'Jonathan Reed' in summary
    assert 'NeuroVance' in summary
    assert 'NeuroVance XR' in summary
    assert 'Clinical Brochure' in summary
    assert 'Positive' in summary
    assert 'Interested' in summary
