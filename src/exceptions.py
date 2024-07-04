from fastapi import HTTPException

from src.schemas import ErrorResponse


class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, error_type: str, error_message: str):
        self.status_code = status_code
        self.detail = ErrorResponse(
            result=False,
            error_type=error_type,
            error_message=error_message
        ).model_dump()
        super().__init__(status_code=status_code, detail=self.detail)


class UserNotFoundException(CustomHTTPException):
    def __init__(self):
        super().__init__(status_code=404, error_type="UserNotFound", error_message="User not found")


class UserToFollowNotFoundException(CustomHTTPException):
    def __init__(self):
        super().__init__(status_code=404, error_type="UserToFollowNotFound", error_message="User to follow not found")


class CannotFollowYourselfException(CustomHTTPException):
    def __init__(self):
        super().__init__(status_code=400, error_type="CannotFollowYourself", error_message="You cannot follow yourself")


class UserAlreadyFollowedException(CustomHTTPException):
    def __init__(self):
        super().__init__(status_code=400, error_type="UserAlreadyFollowed", error_message="User is already followed")


class UserNotFollowedException(CustomHTTPException):
    def __init__(self):
        super().__init__(status_code=400, error_type="UserNotFollowed", error_message="User is not followed")


class CannotUnfollowYourselfException(CustomHTTPException):
    def __init__(self):
        super().__init__(status_code=400, error_type="CannotUnfollowYourself", error_message="You cannot unfollow yourself")
