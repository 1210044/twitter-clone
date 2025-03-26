from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles

from src.core.lifespan import lifespan
from src.config.project_config import settings
from src.exceptions.exception_handlers import custom_http_exception_handler, validation_exception_handler
from src.schemas.error_schema import ValidationErrors

from src.routers.user_router import router as auth_router
from src.routers.tweet_router import router as tweet_router
from src.routers.media_router import router as media_router


app = FastAPI(
    title="Twitter Clone",
    description="Api for Twitter clone",
    version="0.1.0",
    lifespan=lifespan,
    responses={
        422: {"description": "Validation Error", "model": ValidationErrors},
    },
)

# app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, custom_http_exception_handler)

app.include_router(auth_router, prefix="/api")
app.include_router(tweet_router, prefix="/api")
app.include_router(media_router, prefix="/api")

app.mount(
    f"/{settings.TWEETS_MEDIA_DIR}/",
    StaticFiles(directory=settings.TWEETS_MEDIA_DIR, check_dir=False),
    name="media",
)
app.mount("/", StaticFiles(directory=settings.STATIC_DIR, html=True), name="static")
