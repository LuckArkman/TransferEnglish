from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.middleware.tenant import TenantMiddleware
from app.api.v1.endpoints import login, linguistics, analytics, progression, gamification, recommendation, admin, privacy, billing
from app.api.ws.audio import audio_manager
from fastapi import WebSocket

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(TenantMiddleware)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/")
def root():
    return {"message": "Welcome to LuckArkman English Fluency API"}

@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy", "version": "0.1.0"}

app.include_router(login.router, prefix=settings.API_V1_STR, tags=["auth"])
app.include_router(linguistics.router, prefix=f"{settings.API_V1_STR}/linguistics", tags=["linguistics"])
app.include_router(analytics.router, prefix=f"{settings.API_V1_STR}/analytics", tags=["analytics"])
app.include_router(progression.router, prefix=f"{settings.API_V1_STR}/progression", tags=["progression"])
app.include_router(gamification.router, prefix=f"{settings.API_V1_STR}/gamification", tags=["gamification"])
app.include_router(recommendation.router, prefix=f"{settings.API_V1_STR}/recommendation", tags=["recommendation"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["admin"])
app.include_router(privacy.router, prefix=f"{settings.API_V1_STR}/privacy", tags=["privacy"])
app.include_router(billing.router, prefix=f"{settings.API_V1_STR}/billing", tags=["billing"])

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.websocket("/ws/audio/{tenant_id}")
async def websocket_audio_endpoint(websocket: WebSocket, tenant_id: str):
    await audio_manager.connect(websocket, tenant_id)
    await audio_manager.handle_audio_stream(websocket, tenant_id)
