from fastapi import APIRouter, Depends

from src.config.database.db_helper import db_helper
from src.schemas.status_schema import Status
from src.schemas.error_schema import ErrorOut
from src.models.user_model import User
from src.dependencies.auth_dependencies import get_current_user
from src.schemas.user_schema import UserOut
from src.exceptions import user_exceptions


router = APIRouter(prefix="/users", tags=["Users"])


# @router.get("/me", response_model=UserOut, responses={404: {"model": ErrorOut}})
# async def get_user_me(user: User = Depends(get_current_user)) -> UserOut:
#     return UserOut(result=True, user=user)


# @router.get(
#     "/{user_id}", response_model=UserOut, responses={404: {"model": ErrorOut}}
# )
# async def get_user_by_id(user_id: int, session=Depends(db_helper.get_db_session())) -> UserOut:
#     user = await UserCrud.get_user_by_id(user_id, session)
#     if not user:
#         raise user_exceptions.UserNotFoundException()
#     return UserOut(result=True, user=user)


# @router.post(
#     "/{follow_id}/follow",
#     response_model=Status,
#     responses={404: {"model": ErrorOut}},
# )
# async def follow_user_by_id(
#     follow_id: int, user: User = Depends(get_current_user), session=Depends(db_helper.get_db_session())
# ) -> Status:
#     if user.id == follow_id:
#         raise exceptions.FollowToYouSelfException()

#     following = await UserCrud.get_user_by_id(follow_id, session)
#     if not following:
#         raise exceptions.UserToFollowNotFoundException()

#     await UserCrud.create_follow(user.id, follow_id, session)
#     return Status(result=True)


# @router.delete(
#     "/{follow_id}/follow",
#     response_model=Status,
#     responses={404: {"model": ErrorOut}},
# )
# async def unfollow_user_by_id(
#     follow_id: int, user: User = Depends(get_current_user), session=Depends(db_helper.get_db_session())
# ) -> Status:
#     if user.id == follow_id:
#         raise exceptions.FollowToYouSelfException()

#     following = await UserCrud.get_user_by_id(follow_id, session)
#     if not following:
#         raise exceptions.UserToFollowNotFoundException()

#     await UserCrud.delete_follow(user.id, follow_id, session)
#     return Status(result=True)
