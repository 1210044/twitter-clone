from typing import List
from fastapi import APIRouter, Header, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from src.logger import logger
from src.db import get_session
from src.tweets.models import Tweet, TweetLike
from src.auth.models import User
from src.medias.models import Media
from src.schemas import StatusResponse
from src.tweets.schemas import TweetIn, TweetOut, TweetsOut
from src.auth import service as UserService

router = APIRouter(prefix='/tweets')


@router.get('', response_model=TweetsOut)
async def get_tweets(api_key: str = Header(None), session = Depends(get_session)):
    stmt = select(Tweet).options(
        selectinload(Tweet.author),
        joinedload(Tweet.attachments).load_only(Media.url),
        joinedload(Tweet.tweets_likes).joinedload(TweetLike.user)
    )
    result = await session.execute(stmt)
    tweets = result.unique().scalars().all()
    return {'tweets': tweets}


@router.post('', response_model=TweetOut)
async def create_tweet(tweet: TweetIn, api_key: str = Header(...), session = Depends(get_session)):
    author = await UserService.get_user_by_api_key(api_key, session)
    if not author:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Получение вложений
    stmt = select(Media).where(Media.id.in_(tweet.tweet_media_ids))
    result = await session.execute(stmt)
    attachments = result.scalars().all()
    
    # Создание твита
    tweet_instance = Tweet(
        content=tweet.tweet_data, 
        author=author
    )
    tweet_instance.attachments.extend(attachments)
    session.add(tweet_instance)
    
    # Коммит транзакции
    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        logger.error(f"Failed to commit transaction: {e}")
        raise HTTPException(status_code=500, detail="Failed to create tweet")
    
    return {'tweet_id': tweet_instance.id}


@router.delete('/{id}', response_model=StatusResponse)
async def delete_tweet_by_id(id: int, api_key: str = Header(...), session = Depends(get_session)) -> StatusResponse:
    stmt = select(User).filter(User.api_key == api_key)
    result = await session.execute(stmt)
    user = result.scalars().first()

    stmt = select(Tweet).filter(Tweet.id == id)
    result = await session.execute(stmt)
    tweet = result.scalars().first()

    if user.id == tweet.author_id:
        await session.delete(tweet)
        await session.commit()
        return StatusResponse()
    return StatusResponse(result=False)


@router.post('/{id}/likes', response_model=StatusResponse)
async def create_like_tweet_by_id(id: int, api_key: str = Header(...), session = Depends(get_session)) -> StatusResponse:
    stmt = select(User).filter(User.api_key == api_key)
    result = await session.execute(stmt)
    user = result.scalars().first()

    stmt = select(Tweet).options(joinedload(Tweet.tweets_likes)).filter(Tweet.id == id)
    result = await session.execute(stmt)
    tweet = result.scalars().first()
    tweet.likes.append(user)
    await session.commit()

    return StatusResponse()


@router.delete('/{id}/likes', response_model=StatusResponse)
async def delete_like_tweet_by_id(id: int, api_key: str = Header(...), session = Depends(get_session)) -> StatusResponse:
    stmt = select(User).filter(User.api_key == api_key)
    result = await session.execute(stmt)
    user = result.scalars().first()

    stmt = select(TweetLike).filter(TweetLike.tweet_id == id, TweetLike.user_id == user.id)
    result = await session.execute(stmt)
    like = result.scalars().first()

    if like:
        await session.delete(like)
        await session.commit()
        return StatusResponse()
    return StatusResponse(result=False)