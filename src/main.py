from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles

from src.db import lifespan
from src.config import STATIC_DIR, TWEETS_MEDIA_DIR
from src.exceptions import custom_http_exception_handler#, validation_exception_handler
from src.schemas import ValidationErrors

from src.auth.router import router as auth_router
from src.tweets.router import router as tweets_router
from src.medias.router import router as medias_router


app = FastAPI(
    title='Twitter Clone',
    description='Api for Twitter clone',
    version='0.1.0',
    lifespan=lifespan, 
    responses={
        422: {
            'description': 'Validation Error',
            'model': ValidationErrors
        },
    }
)

# app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, custom_http_exception_handler)

app.include_router(auth_router, prefix='/api')
app.include_router(tweets_router, prefix='/api')
app.include_router(medias_router, prefix='/api')

app.mount(f'/{TWEETS_MEDIA_DIR}/', StaticFiles(directory=TWEETS_MEDIA_DIR, check_dir=False), name='media')
app.mount('/', StaticFiles(directory=STATIC_DIR, html=True), name='static')