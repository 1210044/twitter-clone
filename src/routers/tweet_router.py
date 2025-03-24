from fastapi import APIRouter, Depends, HTTPException

from src.config.database.db_helper import db_helper
from src.schemas.status_schema import Status
from src.schemas.tweet_schema import TweetIn, TweetOut, TweetsOut
from src.tweets import crud as TweetCrud
from src.medias import crud as MediaCrud
from src.medias import service as MediaService
from src.dependencies import get_current_user
from src.models.user_model import User

router = APIRouter(prefix="/tweets")


@router.get("", response_model=TweetsOut)
async def get_tweets(
    user: User = Depends(get_user), session=Depends(db_helper.get_db_session())
) -> TweetsOut:
    tweets = await TweetCrud.get_all_tweets(session)
    return TweetsOut(result=True, tweets=tweets)


@router.post("", response_model=TweetOut)
async def create_tweet(
    tweet: TweetIn,
    author: User = Depends(get_user),
    session=Depends(db_helper.get_db_session()),
) -> TweetOut:
    attachments = await MediaCrud.get_medias_by_ids(tweet.tweet_media_ids, session)
    tweet_instance = await TweetCrud.create_tweet(
        tweet.tweet_data, author, attachments, session
    )
    return TweetOut(result=True, tweet_id=tweet_instance.id)


@router.delete("/{tweet_id}", response_model=Status)
async def delete_tweet_by_id(
    tweet_id: int,
    author: User = Depends(get_user),
    session=Depends(db_helper.get_db_session()),
) -> Status:
    tweet = await TweetCrud.get_tweet_by_idx_with_attachments(tweet_id, session)
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")

    if author.id == tweet.author_id:
        await MediaService.delete_medias(tweet.attachments)
        await TweetCrud.delete_tweet(tweet, session)

    return Status(result=True)


@router.post("/{tweet_id}/likes", response_model=Status)
async def create_tweet_like_by_id(
    tweet_id: int,
    author: User = Depends(get_user),
    session=Depends(db_helper.get_db_session()),
) -> Status:
    tweet = await TweetCrud.get_tweet_by_idx(tweet_id, session)
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")

    await TweetCrud.create_tweet_like(tweet_id, author.id, session)
    return Status(result=True)


@router.delete("/{tweet_id}/likes", response_model=Status)
async def delete_like_tweet_by_id(
    tweet_id: int,
    author: User = Depends(get_user),
    session=Depends(db_helper.get_db_session()),
) -> Status:
    tweet = await TweetCrud.get_tweet_by_idx(tweet_id, session)
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")

    tweet_like = await TweetCrud.get_tweet_like_by_tweet_id_and_user_id(
        tweet_id, author.id
    )
    if tweet_like:
        await TweetCrud.delete_tweet(tweet_like, session)

    return Status(result=True)
