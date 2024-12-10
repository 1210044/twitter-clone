from shutil import rmtree
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import TWEETS_MEDIA_DIR
from src.logger import logger
from src.models import Base

PG_USER = 'admin'
PG_PASSWORD = 'admin'
PG_HOST = 'postgres'
PG_PORT = 5432
PG_DATABASE_NAME = 'twitter'
PG_DB_URL = f'postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE_NAME}'


engine = create_async_engine(PG_DB_URL)
SessionLocal = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)   # type: ignore


@asynccontextmanager
async def lifespan(app):
    async with engine.begin() as conn:
        logger.info('Dropping table...')
        await conn.run_sync(Base.metadata.drop_all)
        logger.info('Creating tables...')
        await conn.run_sync(Base.metadata.create_all)
        logger.info('Deleted media director...')
        rmtree(TWEETS_MEDIA_DIR, ignore_errors=True)
        logger.info('Created media director...')
        TWEETS_MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    logger.info('Created data...')
    await create_data()
    yield
    await engine.dispose()


async def get_session():
    async with SessionLocal() as session:
        yield session


async def create_data(num_users=10, num_tweets=20):
    import random
    from src.auth.models import User, Follow
    from src.tweets.models import Tweet

    async with SessionLocal() as session:
        users = [User(name=f'user_{num}', api_key=f'user_{num}') for num in range(1, num_users + 1)]
        tweets = [Tweet(content=f'content_{num}', author=random.choice(users)) for num in range(1, num_tweets + 1)]
        for tweet in tweets:
            likes = set(random.choices(users, k=random.randint(1, num_users)))
            tweet.likes.extend(likes)

        session.add_all(users + tweets)
        await session.flush()
        
        follows = [Follow(following_id=user.id, follower_id=follower_id)
                   for user in users
                   for follower_id in set(random.randint(1, num_users) for _ in range(random.randint(1, num_users + 1)))
                   if user.id != follower_id]

        session.add_all(follows)
        await session.commit()