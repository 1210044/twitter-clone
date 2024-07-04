from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.auth.router import router as auth_router
from src.tweets.router import router as tweets_router
from src.medias.router import router as medias_router
from src.db import lifespan
from src.config import STATIC_DIR, TWEETS_MEDIA_DIR


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix='/api')
app.include_router(tweets_router, prefix='/api')
app.include_router(medias_router, prefix='/api')

app.mount(f'/{TWEETS_MEDIA_DIR}/', StaticFiles(directory=TWEETS_MEDIA_DIR, check_dir=False), name='media')
app.mount('/', StaticFiles(directory=STATIC_DIR, html=True), name='static')