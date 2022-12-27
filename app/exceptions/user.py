from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

UserAlreadyExist = HTTPException(
    status_code=HTTP_400_BAD_REQUEST,
    detail="User Already Exist",
)

UserNotFound = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail="User Not Found",
)
