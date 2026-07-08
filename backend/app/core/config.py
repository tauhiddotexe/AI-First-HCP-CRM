from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = 'AI-First CRM'
    VERSION: str = '0.1.0'
    API_V1_PREFIX: str = '/api/v1'

    DATABASE_URL: str = 'postgresql+asyncpg://crm_user:crm_pass@localhost:5432/crm_db'
    GROQ_API_KEY: str = ''

    ALLOWED_ORIGINS: list[str] = [
        'http://localhost:5173',
        'http://localhost:3000',
        'http://127.0.0.1:5173',
        'http://127.0.0.1:3000',
    ]

    DEMO_USER_ID: str = 'demo-rep-001'
    DEMO_USER_NAME: str = 'Demo Representative'
    DEMO_USER_EMAIL: str = 'rep@pharma.com'

    model_config = {'env_file': '.env', 'case_sensitive': True}


settings = Settings()
