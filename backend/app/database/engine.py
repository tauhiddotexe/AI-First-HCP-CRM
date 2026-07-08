from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings

engine_args: dict = {
    'echo': False,
}

if 'postgresql' in settings.DATABASE_URL:
    engine_args['pool_size'] = 5
    engine_args['max_overflow'] = 10
    engine = create_async_engine(settings.DATABASE_URL, **engine_args)
elif 'sqlite' in settings.DATABASE_URL:
    engine = create_async_engine(
        settings.DATABASE_URL,
        connect_args={'check_same_thread': False},
        **engine_args,
    )
else:
    engine = create_async_engine(settings.DATABASE_URL, **engine_args)

async_session = async_sessionmaker(engine, expire_on_commit=False)
