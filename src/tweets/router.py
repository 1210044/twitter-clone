from fastapi import APIRouter, Header, Depends, HTTPException

from src.logger import logger
from src.db import get_session
from src.schemas import StatusResponse
from src.tweets.schemas import TweetIn, TweetOut, TweetsOut
from src.auth import service as UserService
from src.medias import service as MediaService
from src.tweets import service as TweetService

router = APIRouter(prefix='/tweets')


@router.get('', response_model=TweetsOut)
async def get_tweets(api_key: str = Header(None), session = Depends(get_session)):
    tweets = await TweetService.get_all_tweets(session)
    return {'tweets': tweets}


@router.post('', response_model=TweetOut)
async def create_tweet(tweet: TweetIn, api_key: str = Header(...), session = Depends(get_session)):
    author = await UserService.get_user_by_api_key(api_key, session)
    if not author:
        raise HTTPException(status_code=404, detail='User not found')

    attachments = await MediaService.get_medias_by_ids(tweet.tweet_media_ids, session)
    tweet_instance = await TweetService.create_tweet(tweet.tweet_data, author, attachments, session)
    return {'tweet_id': tweet_instance.id}


@router.delete('/{tweet_id}', response_model=StatusResponse)
async def delete_tweet_by_id(tweet_id: int, api_key: str = Header(...), session = Depends(get_session)) -> StatusResponse:
    user = await UserService.get_user_by_api_key(api_key, session)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    tweet = await TweetService.get_tweet_by_idx(tweet_id, session)
    if not tweet:
        raise HTTPException(status_code=404, detail='Tweet not found')
    
    if user.id == tweet.author_id:
        await TweetService.delete_item(tweet, session)
    
    return StatusResponse()


@router.post('/{tweet_id}/likes', response_model=StatusResponse)
async def create_tweet_like_by_id(tweet_id: int, api_key: str = Header(...), session = Depends(get_session)) -> StatusResponse:
    user = await UserService.get_user_by_api_key(api_key, session)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    tweet = await TweetService.get_tweet_by_idx(tweet_id, session)
    if not tweet:
        raise HTTPException(status_code=404, detail='Tweet not found')
    
    await TweetService.create_tweet_like(tweet_id, user.id, session)
    return StatusResponse()


@router.delete('/{tweet_id}/likes', response_model=StatusResponse)
async def delete_like_tweet_by_id(tweet_id: int, api_key: str = Header(...), session = Depends(get_session)) -> StatusResponse:
    user = await UserService.get_user_by_api_key(api_key, session)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    
    tweet = await TweetService.get_tweet_by_idx(tweet_id, session)
    if not tweet:
        raise HTTPException(status_code=404, detail='Tweet not found')

    tweet_like = await TweetService.get_tweet_like_by_tweet_id_and_user_id(tweet_id, user.id)
    if tweet_like:
        await TweetService.delete_item(tweet_like, session)
    
    return StatusResponse()