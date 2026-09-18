from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import health, auth, users, courses, chat, diagnostic

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.VERSION,
        description="GENESIS: Personal Learning Operating System with Learner Digital Twin and Dynamic Knowledge Graph",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router, prefix=settings.API_PREFIX)
    app.include_router(auth.router, prefix=settings.API_PREFIX)
    app.include_router(users.router, prefix=settings.API_PREFIX)
    app.include_router(courses.router, prefix=settings.API_PREFIX)
    app.include_router(chat.router, prefix=settings.API_PREFIX)
    app.include_router(diagnostic.router, prefix=settings.API_PREFIX)

    @app.get("/")
    async def root():
        return {
            "message": "Welcome to GENESIS API",
            "tagline": "AI that learns how you learn.",
            "docs": "/docs",
            "health": f"{settings.API_PREFIX}/health"
        }

    return app

app = create_app()
