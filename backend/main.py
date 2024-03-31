from typing import Union

from fastapi import FastAPI, APIRouter, Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response

from database.database_connector import get_session
from database.models import DBUser, DBOrganization, DBPermission
from models import PingResponse, AuthSignInPostResponse, AuthSignInPostRequest, ErrorResponse, AuthRegisterPostResponse, \
    AuthRegisterPostRequest, UserProfile, Organization, OrganizationCreatePostResponse, OrganizationCreatePostRequest, \
    UserOrganizationsGetResponse
from tools.auth import create_access_token, get_current_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_uniq_orgs(orgs: list[DBOrganization]):
    ids = []
    uniq_orgs = []
    for i in orgs:
        if i.id in ids:
            continue
        ids.append(i.id)
        uniq_orgs.append(Organization(**i.dict()))
    return uniq_orgs


app = FastAPI(
    title='SMM app API',
    version='1.0',
    docs_url='/api/docs',
    openapi_url="/api/v1/openapi.json",
)

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix='/api')


@router.get('/ping', response_model=PingResponse)
def ping() -> PingResponse:
    return PingResponse(status="ok")


@router.post(
    '/auth/sign-in',
    response_model=Union[AuthSignInPostResponse, ErrorResponse],
    responses={
        '200': {'model': AuthSignInPostResponse},
        '401': {'model': ErrorResponse},
    },
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
    '/auth/register',
    response_model=Union[AuthRegisterPostResponse, ErrorResponse],
    responses={
        '201': {'model': AuthRegisterPostResponse},
        '400': {'model': ErrorResponse},
        '409': {'model': ErrorResponse},
    },
    response_model_exclude_none=True,
)
def auth_register(
        response: Response, body: AuthRegisterPostRequest, db_session: Session = Depends(get_session)
) -> Union[AuthRegisterPostResponse, ErrorResponse]:
    db_model = DBUser(**body.dict())
    db_model.password = get_password_hash(db_model.password)
    db_session.add(db_model)
    try:
        db_session.commit()
    except:
        response.status_code = 409
        return ErrorResponse(reason="conflict")
    response.status_code = 201
    return AuthRegisterPostResponse(profile=UserProfile(**db_model.dict()))


# add new orgs
@router.post(
    '/organizations',
    response_model=Union[OrganizationCreatePostResponse, ErrorResponse],
    responses={
        '201': {'model': OrganizationCreatePostResponse},
        '400': {'model': ErrorResponse},
        '401': {'model': ErrorResponse},
        '409': {'model': ErrorResponse}
    }
)
def organization_create(
        response: Response, body: OrganizationCreatePostRequest, db_session=Depends(get_session),
        current_user=Depends(get_current_user)
) -> Union[OrganizationCreatePostResponse, ErrorResponse]:
    organization = DBOrganization(**body.dict())
    db_session.add(organization)
    db_session.add(DBPermission(name="owner", level=5, can_grant=True))
    try:
        db_session.commit()
    except:
        response.status_code = 409
        return ErrorResponse(reason="conflict")
    response.status_code = 201
    return OrganizationCreatePostResponse(organization=Organization(**organization.dict()))


@router.get(
    '/organizations',
    response_model=Union[UserOrganizationsGetResponse, ErrorResponse],
    responses={
        '200': {'model': UserOrganizationsGetResponse},
        '401': {'model': ErrorResponse}
    }
)
def get_user_ogranizations(
        response: Response, db_session=Depends(get_session), current_user: DBUser = Depends(get_current_user)
) -> Union[UserOrganizationsGetResponse, ErrorResponse]:
    return UserOrganizationsGetResponse(
        organizations=get_uniq_orgs([i.organization for i in current_user.organization_bindings]))


# TODO: fetch organization users
# @router.get(
#    '/organizations/{organization_id}/users',
#    response_model=Union[list[OrganizationUser], ErrorResponse]
# )

app.include_router(router)
