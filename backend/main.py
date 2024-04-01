from typing import Union

from fastapi import FastAPI, APIRouter, Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response

from database.database_connector import get_session
from database.models import DBUser, DBOrganization, DBOrganizationUser, DBPermission, DBOrganizationBot
from models import PingResponse, AuthSignInPostResponse, AuthSignInPostRequest, ErrorResponse, ProfileResponse, \
    AuthRegisterPostRequest, UserProfile, Organization, OrganizationCreatePostResponse, OrganizationCreatePostRequest, \
    UserOrganizationsGetResponse, OrganizationUsersGetResponse, OrganizationUser, UserPublicProfile, UserRight, \
    AddBotPostResponse, AddBotPostRequest, ListBotGetResponse, Bot, AddUserPostRequest, AddUserPostResponse, \
    DeleteUserResponse, DeleteUserRequest
from tools.auth import create_access_token, get_current_user

import requests as r

import uvicorn

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


def get_uniq_users(users: list[DBOrganizationUser]):
    ids = []
    uniq_users = []
    for i in users:
        if i.user_id in ids:
            uniq_users[ids.index(i.user_id)].rights.append(UserRight(**i.permission_data.dict()))
        else:
            ids.append(i.user_id)
            uniq_users.append(
                OrganizationUser(user=UserPublicProfile(**i.user.dict()),
                                 rights=[UserRight(**i.permission_data.dict())]))
    return uniq_users


def check_if_all_permissions_in_db(permissions: list[str], session: Session):
    permissions_from_db = [i.name for i in session.query(DBPermission).all()]
    for i in range(len(permissions)):
        if permissions[i] in permissions_from_db:
            continue
        else:
            return False
    return True


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


@router.get('/auth/check', response_model=PingResponse)
def auth_check(current_user: DBUser = Depends(get_current_user)) -> PingResponse:  # noqa: unused
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
    response_model=Union[ProfileResponse, ErrorResponse],
    responses={
        '201': {'model': ProfileResponse},
        '400': {'model': ErrorResponse},
        '409': {'model': ErrorResponse},
    },
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
    '/auth/profile',
    response_model=ProfileResponse,
)
def auth_profile(
        current_user: DBUser = Depends(get_current_user)
) -> ProfileResponse:
    return ProfileResponse(profile=UserProfile(**current_user.dict()))


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
        current_user: DBUser = Depends(get_current_user)
) -> Union[OrganizationCreatePostResponse, ErrorResponse]:
    organization = DBOrganization(**body.dict())
    db_session.add(organization)
    try:
        db_session.commit()
    except:
        response.status_code = 409
        return ErrorResponse(reason="conflict")
    response.status_code = 201
    db_session.add(DBOrganizationUser(
        user_id=current_user.id,
        organization_id=organization.id,
        permission="owner"
    ))
    try:
        db_session.commit()
    except:
        response.status_code = 409
        return ErrorResponse(reason="conflict when adding owner")
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
        current_user: DBUser = Depends(get_current_user)
) -> Union[UserOrganizationsGetResponse, ErrorResponse]:
    return UserOrganizationsGetResponse(
        organizations=get_uniq_orgs([i.organization for i in current_user.organization_bindings]))


@router.get(
    '/organizations/{organization_id}/users',
    response_model=Union[OrganizationUsersGetResponse, ErrorResponse],
    responses={
        '200': {'model': OrganizationUsersGetResponse},
        '401': {'model': ErrorResponse},
        '403': {'model': ErrorResponse}
    }
)
def get_organization_users(
        organization_id: int, response: Response, db_session=Depends(get_session),
        current_user: DBUser = Depends(get_current_user)
) -> Union[OrganizationUsersGetResponse, ErrorResponse]:
    if current_user.organization_bindings.join(DBPermission).filter(
            DBOrganizationUser.organization_id == organization_id, DBPermission.level >= 4).count() == 0:
        response.status_code = 403
        return ErrorResponse(reason="Don\'t have required permissions")
    result = db_session.query(DBOrganizationUser).filter(DBOrganizationUser.organization_id == organization_id).all()
    return OrganizationUsersGetResponse(users=get_uniq_users(result))


@router.post(
    '/organizations/{organization_id}/users',
    response_model=Union[AddUserPostResponse, ErrorResponse],
    responses={
        '200': {'model': AddUserPostResponse},
        '400': {'model': ErrorResponse},
        '401': {'model': ErrorResponse},
        '403': {'model': ErrorResponse},
        '404': {'model': ErrorResponse},
        '409': {'model': ErrorResponse}
    }
)
def add_user_to_organization(
        organization_id: int,
        response: Response, body: AddUserPostRequest, db_session: Session = Depends(get_session),
        current_user=Depends(get_current_user)
) -> Union[AddUserPostResponse, ErrorResponse]:
    if not check_if_all_permissions_in_db(body.permissions, db_session) or len(body.permissions) == 0:
        response.status_code = 400
        return ErrorResponse(reason="Wrong permission type")
    if current_user.organization_bindings.join(DBPermission).filter(
            DBOrganizationUser.organization_id == organization_id, DBPermission.level >= 4).count() == 0:
        response.status_code = 403
        return ErrorResponse(reason="Don\'t have required permissions")
    user = db_session.query(DBUser).filter_by(login=body.login).first()
    if user is None:
        response.status_code = 404
        return ErrorResponse(reason="User not found")
    if user.organization_bindings.filter(DBOrganizationUser.organization_id == organization_id).count() != 0:
        response.status_code = 409
        return ErrorResponse(reason="conflict")
    db_model = DBOrganizationUser(user_id=user.id, organization_id=organization_id, permission="viewer")
    db_session.add(db_model)
    try:
        db_session.commit()
    except:
        response.status_code = 409
        return ErrorResponse(reason="conflict")
    return AddUserPostResponse(user=UserPublicProfile(**user.dict()))


@router.delete(
    '/organizations/{organization_id}/users',
    response_model=Union[DeleteUserResponse, ErrorResponse],
    responses={
        '200': {'model': DeleteUserResponse},
        '401': {'model': ErrorResponse},
        '403': {'model': ErrorResponse},
        '404': {'model': ErrorResponse}
    }
)
def delete_user_from_organization(
        organization_id: int,
        response: Response, body: DeleteUserRequest, db_session: Session = Depends(get_session),
        current_user: DBUser = Depends(get_current_user)
) -> Union[DeleteUserResponse, ErrorResponse]:
    if current_user.organization_bindings.join(DBPermission).filter(
            DBOrganizationUser.organization_id == organization_id, DBPermission.level >= 4).count() == 0:
        response.status_code = 403
        return ErrorResponse(reason="Don\'t have required permissions")
    user_to_delete = db_session.query(DBUser).filter_by(login=body.login).first()
    if user_to_delete is None or user_to_delete.organization_bindings.filter(
            DBOrganizationUser.organization_id == organization_id).count() == 0:
        response.status_code = 404
        return ErrorResponse(reason="No such user in organization")
    current_user_level = current_user.organization_bindings.join(DBPermission).order_by(
        DBPermission.level.desc()).filter(
        DBOrganizationUser.organization_id == organization_id).first().permission_data.level
    if user_to_delete.organization_bindings.join(DBPermission).filter(
            DBOrganizationUser.organization_id == organization_id,
            DBPermission.level >= current_user_level).count() != 0:
        response.status_code = 403
        return ErrorResponse(reason="You can\'t delete admin or owner")
    user_to_delete.organization_bindings.filter(DBOrganizationUser.organization_id == organization_id).delete()
    db_session.commit()
    return DeleteUserResponse(user=UserPublicProfile(**user_to_delete.dict()))


@router.post(
    '/organizations/{organization_id}/bots',
    response_model=Union[AddBotPostResponse, ErrorResponse],
    responses={
        '200': {'model': AddBotPostResponse},
        '400': {'model': ErrorResponse},
        '401': {'model': ErrorResponse},
        '403': {'model': ErrorResponse},
        '409': {'model': ErrorResponse}
    }
)
def add_organization_bot(
        organization_id: int,
        response: Response, body: AddBotPostRequest, db_session=Depends(get_session),
        current_user: DBUser = Depends(get_current_user)
) -> Union[AddBotPostResponse, ErrorResponse]:
    if current_user.organization_bindings.join(DBPermission).filter(
            DBOrganizationUser.organization_id == organization_id, DBPermission.level >= 4).count() == 0:
        response.status_code = 403
        return ErrorResponse(reason="Don\'t have required permissions")
    req = r.get(f'https://api.telegram.org/bot{body.token}/getMe')
    if req.status_code != 200:
        return ErrorResponse(reason="Invalid token")
    db_model = DBOrganizationBot(organization_id=organization_id, bot_token=body.token)
    db_session.add(db_model)
    try:
        db_session.commit()
    except:
        response.status_code = 409
        return ErrorResponse(reason="conflict")
    return AddBotPostResponse(id=db_model.bot_id)


@router.get(
    '/organizations/{organization_id}/bots',
    response_model=Union[ListBotGetResponse, ErrorResponse],
    responses={
        '200': {'model': ListBotGetResponse},
        '401': {'model': ErrorResponse},
        '403': {'model': ErrorResponse}
    }
)
def get_organization_bots(
        organization_id: int,
        response=Response, db_session=Depends(get_session), current_user=Depends(get_current_user)
) -> Union[ListBotGetResponse, ErrorResponse]:
    if current_user.organization_bindings.join(DBPermission).filter(
            DBOrganizationUser.organization_id == organization_id, DBPermission.level >= 4).count() == 0:
        response.status_code = 403
        return ErrorResponse(reason="Don\'t have required permissions")
    result = db_session.query(DBOrganizationBot).filter(DBOrganizationBot.organization_id == organization_id).all()
    return ListBotGetResponse(bots=[Bot(**i.dict()) for i in result])


@router.get(
    '/organizations/{organization_id}',
    response_model=Union[Organization, ErrorResponse],
    responses={
        '200': {'model': Organization},
        '401': {'model': ErrorResponse},
        '403': {'model': ErrorResponse}
    }
)
def get_organization_info(
        organization_id: int,
        response: Response, db_session=Depends(get_session), current_user=Depends(get_current_user)
) -> Union[Organization, ErrorResponse]:
    if current_user.organization_bindings.filter(
            DBOrganizationUser.organization_id == organization_id).count() == 0:
        response.status_code = 403
        return ErrorResponse(reason="Don\'t have required permissions")
    return Organization(**db_session.query(DBOrganization).filter_by(id=organization_id).all()[0].dict())


app.include_router(router)
# uvicorn.run(app, host='0.0.0.0', port=5437, log_level="debug")
