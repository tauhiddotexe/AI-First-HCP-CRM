"""Seed the database with demo data. Idempotent: safe to run on restarts."""

import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings
from app.models.base import Base
from app.models.user import User
from app.models.hcp import HCP


async def seed():
    engine = create_async_engine(settings.DATABASE_URL)
    session_factory = async_sessionmaker(engine)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with session_factory() as session:
        existing = await session.execute(select(User).where(User.id == settings.DEMO_USER_ID))
        if existing.scalar_one_or_none():
            print('Seed skipped: data already exists')
            await engine.dispose()
            return

        demo_user = User(
            id=settings.DEMO_USER_ID,
            full_name=settings.DEMO_USER_NAME,
            email=settings.DEMO_USER_EMAIL,
            role='sales_rep',
        )
        session.add(demo_user)

        hcps = [
            HCP(first_name='Sarah', last_name='Patel', title='Dr.', specialization='Cardiology', hospital='City Hospital', city='Mumbai'),
            HCP(first_name='Rajesh', last_name='Shah', title='Dr.', specialization='Neurology', hospital='Neuro Care Center', city='Delhi'),
            HCP(first_name='Priya', last_name='Gupta', title='Dr.', specialization='Pediatrics', hospital='Children\'s Hospital', city='Bangalore'),
            HCP(first_name='Anand', last_name='Verma', title='Dr.', specialization='Orthopedics', hospital='Bone & Joint Clinic', city='Pune'),
            HCP(first_name='Meera', last_name='Reddy', title='Dr.', specialization='Dermatology', hospital='Skin Care Institute', city='Hyderabad'),
        ]
        for hcp in hcps:
            session.add(hcp)

        await session.commit()
        print(f'Seeded: 1 user, {len(hcps)} HCPs')

    await engine.dispose()


if __name__ == '__main__':
    asyncio.run(seed())
