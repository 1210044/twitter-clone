import random

from src.config.database.db_helper import db_helper
from src.models.user_model import User
from src.models.follow_model import Follow
from src.models.tweet_model import Tweet


async def create_data(num_users=10, num_tweets=20):
    async with db_helper.get_db_session() as session:
        users = [
            User(name=f"user_{num}", api_key=f"user_{num}")
            for num in range(1, num_users + 1)
        ]
        users.append(User(name="test", api_key="test"))
        tweets = [
            Tweet(content=f"content_{num}", author=random.choice(users))
            for num in range(1, num_tweets + 1)
        ]
        for tweet in tweets:
            likes = set(random.choices(users, k=random.randint(1, num_users)))
            tweet.likes.extend(likes)

        session.add_all(users + tweets)
        await session.flush()

        follows = [
            Follow(following_id=user.id, follower_id=follower_id)
            for user in users
            for follower_id in set(
                random.randint(1, num_users)
                for _ in range(random.randint(1, num_users + 1))
            )
            if user.id != follower_id
        ]

        session.add_all(follows)
        await session.commit()