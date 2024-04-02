from typing import Union

from fastapi import Depends, APIRouter
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette.responses import Response

from database.database_connector import get_session
from database.models import DBUser
from models import StatusResponse, AuthSignInPostResponse, AuthSignInPostRequest, ErrorResponse, ProfileResponse, \
    AuthRegisterPostRequest, UserProfile
from tools.auth import create_access_token, get_current_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/auth")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


@router.get('/check', response_model=StatusResponse, tags=["auth"])
def auth_check(current_user: DBUser = Depends(get_current_user)) -> StatusResponse:  # noqa: unused
    return StatusResponse(status="ok")


@router.post(
    '/sign-in',
    response_model=Union[AuthSignInPostResponse, ErrorResponse],
    responses={
        '200': {'model': AuthSignInPostResponse},
        '401': {'model': ErrorResponse},
    }, tags=["auth"]
)
def auth_sign_in(response: Response, body: AuthSignInPostRequest,
                 db_session: Session = Depends(get_session)) -> Union[AuthSignInPostResponse, ErrorResponse]:
    user = db_session.query(DBUser).filter(DBUser.login == body.login).first()
    if user is None or not verify_password(body.password, user.password):
        response.status_code = 401
        return ErrorResponse(reason="user not found")
    token = create_access_token({"login": user.login})
    return AuthSignInPostResponse(token=token)


@router.post(
    '/register',
    response_model=Union[ProfileResponse, ErrorResponse],
    responses={
        '201': {'model': ProfileResponse},
        '400': {'model': ErrorResponse},
        '409': {'model': ErrorResponse},
    }, tags=["auth"]
)
def auth_register(
        response: Response, body: AuthRegisterPostRequest, db_session: Session = Depends(get_session)
) -> Union[ProfileResponse, ErrorResponse]:
    db_model = DBUser(**body.dict())
    db_model.password = get_password_hash(db_model.password)
    db_session.add(db_model)
    try:
        db_session.commit()
    except:
        response.status_code = 409
        return ErrorResponse(reason="conflict")
    response.status_code = 201
    return ProfileResponse(profile=UserProfile(**db_model.dict()))


@router.get(
    '/profile',
    response_model=ProfileResponse, tags=["auth"]
)
def auth_profile(
        current_user: DBUser = Depends(get_current_user)
) -> ProfileResponse:
    return ProfileResponse(profile=UserProfile(**current_user.dict()))
