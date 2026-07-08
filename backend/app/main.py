from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.datastructures import MutableHeaders
from app.core.config import settings
from app.api.v1 import health, hcps, interactions, dashboard, followups, chat, agent

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url='/docs',
    redoc_url='/redoc',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        headers = MutableHeaders(response.headers)
        headers['X-Content-Type-Options'] = 'nosniff'
        headers['X-Frame-Options'] = 'DENY'
        headers['X-XSS-Protection'] = '1; mode=block'
        headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    _requests: dict[str, list[float]] = {}

    def __init__(self, app, max_requests: int = 30, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else 'unknown'
        now = __import__('time').time()
        timestamps = RateLimitMiddleware._requests.setdefault(client_ip, [])

        while timestamps and timestamps[0] < now - self.window_seconds:
            timestamps.pop(0)

        if len(timestamps) >= self.max_requests:
            return JSONResponse(
                status_code=429,
                content={'success': False, 'message': 'Too many requests. Please wait before trying again.'},
            )

        timestamps.append(now)
        return await call_next(request)


app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware, max_requests=30, window_seconds=60)


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={'success': False, 'message': 'Resource not found'},
    )


@app.exception_handler(422)
async def validation_handler(request: Request, exc):
    return JSONResponse(
        status_code=422,
        content={'success': False, 'message': 'Validation failed', 'errors': exc.errors() if hasattr(exc, 'errors') else []},
    )


@app.exception_handler(500)
async def internal_handler(request: Request, exc):
    return JSONResponse(
        status_code=500,
        content={'success': False, 'message': 'Internal server error'},
    )


app.include_router(health.router, prefix='/api/v1')
app.include_router(hcps.router, prefix='/api/v1')
app.include_router(interactions.router, prefix='/api/v1')
app.include_router(dashboard.router, prefix='/api/v1')
app.include_router(followups.router, prefix='/api/v1')
app.include_router(chat.router, prefix='/api/v1')
app.include_router(agent.router, prefix='/api/v1')


@app.get('/')
async def root():
    return {'message': f'{settings.PROJECT_NAME} API', 'version': settings.VERSION}