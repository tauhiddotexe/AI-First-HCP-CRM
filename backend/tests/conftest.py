import os

os.environ['DATABASE_URL'] = 'sqlite+aiosqlite:///:memory:'

pytest_plugins = ('pytest_asyncio',)
