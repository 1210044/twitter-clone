from typing import Dict
from fastapi import APIRouter, Header, Depends, HTTPException

from src.logger import logger
from src.db import get_session
from src.schemas import StatusResponseTrue
from src.tweets.schemas import TweetIn, TweetOut, TweetsOut
from src.tweets import service as TweetService
from src.auth import crud as UserCrud
from src.medias import service as MediaService

router = APIRouter(prefix='/tweets')


@router.get('', response_model=TweetsOut)
async def get_tweets(api_key: str = Header(None), session = Depends(get_session)) -> Dict:
    tweets = await TweetService.get_all_tweets(session)
    return {'tweets': tweets}


@router.post('', response_model=TweetOut)
async def create_tweet(tweet: TweetIn, api_key: str = Header(...), session = Depends(get_session)) -> Dict:
    author = await UserCrud.get_user_by_api_key(api_key, session)
    if not author:
        raise HTTPException(status_code=404, detail='User not found')

    attachments = await MediaService.get_medias_by_ids(tweet.tweet_media_ids, session)
    tweet_instance = await TweetService.create_tweet(tweet.tweet_data, author, attachments, session)
    return {'tweet_id': tweet_instance.id}


@router.delete('/{tweet_id}', response_model=StatusResponseTrue)
async def delete_tweet_by_id(tweet_id: int, api_key: str = Header(...), session = Depends(get_session)) -> StatusResponseTrue:
    user = await UserCrud.get_user_by_api_key(api_key, session)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    tweet = await TweetService.get_tweet_by_idx_with_attachments(tweet_id, session)
    if not tweet:
        raise HTTPException(status_code=404, detail='Tweet not found')
    
    if user.id == tweet.author_id:
        await MediaService.delete_medias(tweet.attachments)
        await TweetService.delete_tweet(tweet, session)
    
    return StatusResponseTrue()


@router.post('/{tweet_id}/likes', response_model=StatusResponseTrue)
async def create_tweet_like_by_id(tweet_id: int, api_key: str = Header(...), session = Depends(get_session)) -> StatusResponseTrue:
    user = await UserCrud.get_user_by_api_key(api_key, session)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    tweet = await TweetService.get_tweet_by_idx(tweet_id, session)
    if not tweet:
        raise HTTPException(status_code=404, detail='Tweet not found')
    
    await TweetService.create_tweet_like(tweet_id, user.id, session)
    return StatusResponseTrue()


@router.delete('/{tweet_id}/likes', response_model=StatusResponseTrue)
async def delete_like_tweet_by_id(tweet_id: int, api_key: str = Header(...), session = Depends(get_session)) -> StatusResponseTrue:
    user = await UserCrud.get_user_by_api_key(api_key, session)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    
    tweet = await TweetService.get_tweet_by_idx(tweet_id, session)
    if not tweet:
        raise HTTPException(status_code=404, detail='Tweet not found')

    tweet_like = await TweetService.get_tweet_like_by_tweet_id_and_user_id(tweet_id, user.id)
    if tweet_like:
        await TweetService.delete_item(tweet_like, session)
    
    return StatusResponseTrue()