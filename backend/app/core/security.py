from app.core.config import settings


def get_current_user_id() -> str:
    return settings.DEMO_USER_ID
