from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from src.tweets.models import Tweet, TweetLike
from src.auth.models import User
from src.medias.models import Media


# async def get_all_tweets(session: AsyncSession) -> List[Tweet]:
#     stmt = select(Tweet).options(
#         selectinload(Tweet.author),
#         joinedload(Tweet.attachments).load_only(Media.url),
#         joinedload(Tweet.tweets_likes).joinedload(TweetLike.user),
#     )
#     result = await session.execute(stmt)
#     return result.unique().scalars().all()


# async def get_tweet_by_idx(tweet_id, session: AsyncSession) -> Tweet:
#     stmt = select(Tweet).filter(Tweet.id == tweet_id)
#     result = await session.execute(stmt)
#     return result.scalars().first()


# async def get_tweet_by_idx_with_attachments(tweet_id, session: AsyncSession) -> Tweet:
#     stmt = (
#         select(Tweet)
#         .filter(Tweet.id == tweet_id)
#         .options(joinedload(Tweet.attachments).load_only(Media.url))
#     )
#     result = await session.execute(stmt)
#     return result.scalars().first()


# async def get_tweet_like_by_tweet_id_and_user_id(
#     tweet_id: int, user_id: int, session: AsyncSession
# ) -> TweetLike:
#     stmt = select(TweetLike).filter(
#         TweetLike.tweet_id == tweet_id, TweetLike.user_id == user_id
#     )
#     result = await session.execute(stmt)
#     return result.scalars().first()


# async def create_tweet_like(tweet_id: int, user_id: int, session: AsyncSession) -> None:
#     tweet_like = await get_tweet_like_by_tweet_id_and_user_id(
#         tweet_id, user_id, session
#     )
#     if not tweet_like:
#         tweet_like_instance = TweetLike(user_id=user_id, tweet_id=tweet_id)
#         session.add(tweet_like_instance)
#         await session.commit()


# async def create_tweet(
#     content: str, author: User, attachments: List, session: AsyncSession
# ) -> Tweet:
#     tweet_instance = Tweet(content=content, author=author)
#     tweet_instance.attachments.extend(attachments)
#     session.add(tweet_instance)
#     await session.commit()
#     return tweet_instance


# async def delete_tweet(tweet, session: AsyncSession) -> None:
#     await session.delete(tweet)
#     await session.commit()
