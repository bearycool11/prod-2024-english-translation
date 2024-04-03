from typing import Union

import requests
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from database.database_connector import get_session
from database.models import DBUser, DBOrganization, DBOrganizationUser, DBPermission, DBOrganizationBot, DBChannel, \
    DBPost, SentStatus, Status, DBTask, DBTag, DBOrganizationStopToggle
from models import ErrorResponse, Organization, OrganizationCreatePostResponse, OrganizationCreatePostRequest, \
    UserOrganizationsGetResponse, OrganizationUsersGetResponse, OrganizationUser, UserPublicProfile, AddBotPostResponse, \
    AddBotPostRequest, ListBotGetResponse, Bot, AddUserPostRequest, UserPostResponse, \
    DeleteUserResponse, DeleteUserRequest, AddChannelPostRequest, GetChannelsResponse, Channel, \
    DeleteChannelRequest, DeleteChannelResponse, GetPostsResponse, Post, \
    AddNewPostRequest, AddNewPostResponse, EditPostResponse, EditPostRequest, ScheduleTimeRequest, PostIdResponse, \
    DeletePostRequest, DeletePostResponse, UserRight, PostSentInfo, OrganizationStopToggleIdResponse, StatusResponse
from tools.auth import get_current_user

router = APIRouter(prefix="/organizations")


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


@router.post(
    '/',
    response_model=Union[OrganizationCreatePostResponse, ErrorResponse],
    responses={
        '201': {'model': OrganizationCreatePostResponse},
        '400': {'model': ErrorResponse},
        '401': {'model': ErrorResponse},
        '409': {'model': ErrorResponse}
    },
    tags=["organizations"]
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
    '/',
    response_model=Union[UserOrganizationsGetResponse, ErrorResponse],
    responses={
        '200': {'model': UserOrganizationsGetResponse},
        '401': {'model': ErrorResponse}
    }, tags=["organizations"]
)
def get_user_organizations(
        current_user: DBUser = Depends(get_current_user)
) -> Union[UserOrganizationsGetResponse, ErrorResponse]:
    return UserOrganizationsGetResponse(
        organizations=get_uniq_orgs([i.organization for i in current_user.organization_bindings]))


@router.get(
    '/{organization_id}/users',
    response_model=Union[OrganizationUsersGetResponse, ErrorResponse],
    responses={
        '200': {'model': OrganizationUsersGetResponse},
        '401': {'model': ErrorResponse},
        '403': {'model': ErrorResponse}
    }, tags=["users"]
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
    '/{organization_id}/users',
    response_model=Union[UserPostResponse, ErrorResponse],
    responses={
        '200': {'model': UserPostResponse},
        '400': {'model': ErrorResponse},
        '401': {'model': ErrorResponse},
        '403': {'model': ErrorResponse},
        '404': {'model': ErrorResponse},
        '409': {'model': ErrorResponse}
    }, tags=["users"]
)
def add_user_to_organization(
        organization_id: int,
        response: Response, body: AddUserPostRequest, db_session: Session = Depends(get_session),
        current_user=Depends(get_current_user)
) -> Union[UserPostResponse, ErrorResponse]:
    if not check_if_all_permissions_in_db(body.permissions, db_session) or len(body.permissions) == 0:
        response.status_code = 400
        return ErrorResponse(reason="Wrong permission type")
    if current_user.organization_bindings.join(DBPermission).filter(
            DBOrganizationUser.organization_id == organization_id, DBPermission.level >= 4).count() == 0:
        response.status_code = 403
        return ErrorResponse(reason="Don\'t have required permissions")
    if "owner" in body.permissions or ("admin" in body.permissions and current_user.organization_bindings.join(
            DBPermission).filter(DBOrganizationUser.organization_id == organization_id,
                                 DBPermission.level == 5).count() == 0):
        response.status_code = 403
        return ErrorResponse(reason="Don\'t have required permissions")
    user = db_session.query(DBUser).filter_by(login=body.login).first()
    if user is None:
        response.status_code = 404
        return ErrorResponse(reason="User not found")
    if user.organization_bindings.filter(DBOrganizationUser.organization_id == organization_id).count() != 0:
        response.status_code = 409
        return ErrorResponse(reason="conflict")
    for permission in body.permissions:
        db_model = DBOrganizationUser(user_id=user.id, organization_id=organization_id, permission=permission)
        db_session.add(db_model)
    try:
        db_session.commit()
    except:
        response.status_code = 409
        return ErrorResponse(reason="conflict")
    return UserPostResponse(user=UserPublicProfile(**user.dict()))


@router.patch(
    '/{organization_id}/users',
    response_model=Union[UserPostResponse, ErrorResponse],
    responses={
        '200': {'model': UserPostResponse},
        '401': {'model': ErrorResponse},
        '403': {'model': ErrorResponse},
        '404': {'model': ErrorResponse}
    }, tags=["users"]
)
def change_user_permissions(
        organization_id: int,
        response: Response, body: AddUserPostRequest, db_session: Session = Depends(get_session),
        current_user=Depends(get_current_user)
) -> Union[UserPostResponse, ErrorResponse]:
    if not check_if_all_permissions_in_db(body.permissions, db_session) or len(body.permissions) == 0:
        response.status_code = 400
        return ErrorResponse(reason="Wrong permission type")
    if current_user.organization_bindings.join(DBPermission).filter(
            DBOrganizationUser.organization_id == organization_id, DBPermission.level >= 4).count() == 0:
        response.status_code = 403
        return ErrorResponse(reason="Don\'t have required permissions")
    user = db_session.query(DBUser).filter(DBUser.login == body.login).first()
    if user is None:
        response.status_code = 404
        return ErrorResponse(reason="User not found")
    user_permissions = user.organization_bindings.filter(DBOrganizationUser.organization_id == organization_id).all()
    permissions = set(body.permissions).symmetric_difference(
        {permission.permission_data.name for permission in user_permissions})
    if "owner" in permissions or ("admin" in permissions and current_user.organization_bindings.join(
            DBPermission).filter(DBOrganizationUser.organization_id == organization_id,
                                 DBPermission.level == 5).count() == 0):
        response.status_code = 403
        return ErrorResponse(reason="Don\'t have required permissions")
    db_session.query(DBOrganizationUser).filter(DBOrganizationUser.user_id == user.id).delete()
    for permission in body.permissions:
        db_model = DBOrganizationUser(user_id=user.id, organization_id=organization_id, permission=permission)
        db_session.add(db_model)
    try:
        db_session.commit()
    except:
        response.status_code = 409
        return ErrorResponse(reason="conflict")
    return UserPostResponse(user=UserPublicProfile(**user.dict()))


@router.delete(
    '/{organization_id}/users',
    response_model=Union[DeleteUserResponse, ErrorResponse],
    responses={
        '200': {'model': DeleteUserResponse},
        '401': {'model': ErrorResponse},
        '403': {'model': ErrorResponse},
        '404': {'model': ErrorResponse}
    }, tags=["users"]
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
    '/{organization_id}/bots',
    response_model=Union[AddBotPostResponse, ErrorResponse],
    responses={
        '200': {'model': AddBotPostResponse},
        '400': {'model': ErrorResponse},
        '401': {'model': ErrorResponse},
        '403': {'model': ErrorResponse},
        '409': {'model': ErrorResponse}
    }, tags=["bots"]
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
    req = requests.get(f'https://api.telegram.org/bot{body.token}/getMe')
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
    '/{organization_id}/bots',
    response_model=Union[ListBotGetResponse, ErrorResponse],
    responses={
        '200': {'model': ListBotGetResponse},
        '401': {'model': ErrorResponse},
        '403': {'model': ErrorResponse}
    }, tags=["bots"]
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
    '/{organization_id}',
    response_model=Union[Organization, ErrorResponse],
    responses={
        '200': {'model': Organization},
        '401': {'model': ErrorResponse},
        '403': {'model': ErrorResponse}
    }, tags=["organizations"]
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


@router.get(
    '/{organization_id}/channels',
    response_model=Union[GetChannelsResponse, ErrorResponse],
    responses={
        '200': {'model': GetChannelsResponse},
        '401': {'model': ErrorResponse},
        '403': {'model': ErrorResponse}
    }, tags=["channels"]
)
def get_organization_channels(
        organization_id: int,
        response: Response, db_session: Session = Depends(get_session), current_user=Depends(get_current_user)
) -> Union[GetChannelsResponse, ErrorResponse]:
    if current_user.organization_bindings.filter(
            DBOrganizationUser.organization_id == organization_id).count() == 0:
        response.status_code = 403
        return ErrorResponse(reason="Don\'t have required permissions")
    return GetChannelsResponse(channels=[Channel(**i.dict()) for i in
                                         db_session.query(DBChannel).join(DBOrganizationBot).filter(
                                             DBOrganizationBot.organization_id == organization_id,
                                             DBOrganizationBot.bot_id == DBChannel.bot_id).all()])


@router.post(
    '/{organization_id}/channels',
    response_model=Union[Channel, ErrorResponse],
    responses={
        '200': {'model': Channel},
        '401': {'model': ErrorResponse},
        '403': {'model': ErrorResponse},
        '404': {'model': ErrorResponse},
        '409': {'model': ErrorResponse}
    }, tags=["channels"]
)
def add_channel_to_organization(
        organization_id: int,
        response: Response, body: AddChannelPostRequest, db_session: Session = Depends(get_session),
        current_user=Depends(get_current_user)
) -> Union[Channel, ErrorResponse]:
    if current_user.organization_bindings.join(DBPermission).filter(
            DBOrganizationUser.organization_id == organization_id, DBPermission.level >= 4).count() == 0:
        response.status_code = 403
        return ErrorResponse(reason="Don\'t have required permissions")
    if db_session.query(DBOrganizationBot).filter(DBOrganizationBot.bot_id == body.bot_id,
                                                  DBOrganizationBot.organization_id == organization_id).count() == 0:
        response.status_code = 403
        return ErrorResponse(reason="Don\'t have required permissions")
    if db_session.query(DBChannel).filter(DBChannel.telegram_id == body.telegram_id,
                                          DBChannel.bot_id == body.bot_id).count() != 0:
        response.status_code = 409
        return ErrorResponse(reason="Channel already exists")
    db_model = DBChannel(**body.dict())
    token = db_session.query(DBOrganizationBot).filter(DBOrganizationBot.bot_id == body.bot_id,
                                                       DBOrganizationBot.organization_id == organization_id).first().bot_token
    channel_info = requests.get(f'https://api.telegram.org/bot{token}/getChat?chat_id={body.telegram_id}')
    if channel_info.status_code != 200:
        response.status_code = 404
        return ErrorResponse(reason="Channel not found")
    db_model.name = channel_info.json()['result']['title']
    db_session.add(db_model)
    db_session.commit()
    return Channel(**db_model.dict())


@router.delete(
    '/{organization_id}/channels',
    response_model=Union[DeleteChannelResponse, ErrorResponse],
    responses={
        '200': {'model': DeleteChannelResponse},
        '401': {'model': ErrorResponse},
        '403': {'model': ErrorResponse},
        '404': {'model': ErrorResponse}
    }, tags=["channels"]
)
def delete_channel_from_organization(
        organization_id: int,
        response: Response, body: DeleteChannelRequest, db_session: Session = Depends(get_session),
        current_user=Depends(get_current_user)
) -> Union[DeleteChannelResponse, ErrorResponse]:
    if current_user.organization_bindings.join(DBPermission).filter(
            DBOrganizationUser.organization_id == organization_id, DBPermission.level >= 4).count() == 0:
        response.status_code = 403
        return ErrorResponse(reason="Don\'t have required permissions")
    if db_session.query(DBChannel).join(DBOrganizationBot).filter(DBChannel.id == body.id,
                                                                  DBOrganizationBot.organization_id == organization_id).count() == 0:
        response.status_code = 404
        return ErrorResponse(reason="No such channel")
    channel_to_delete = db_session.query(DBChannel).filter(DBChannel.id == body.id).first()
    channel_to_delete.posts = []
    channel_to_delete.sent_infos = []
    db_session.delete(channel_to_delete)
    db_session.commit()
    return DeleteChannelResponse(id=body.id)


@router.post(
    '/{organization_id}/posts',
    response_model=Union[AddNewPostResponse, ErrorResponse],
    responses={
        '201': {'model': AddNewPostResponse},
        '400': {'model': ErrorResponse},
        '401': {'model': ErrorResponse},
        '403': {'model': ErrorResponse}
    }, tags=["posts"]
)
def add_new_post(
        organization_id: int,
        response: Response, body: AddNewPostRequest, db_session: Session = Depends(get_session),
        current_user: DBUser = Depends(get_current_user)
) -> Union[AddNewPostResponse, ErrorResponse]:
    if current_user.organization_bindings.join(DBPermission).filter(
            DBOrganizationUser.organization_id == organization_id, DBPermission.level.in_([2, 4, 5])).count() == 0:
        response.status_code = 403
        return ErrorResponse(reason="Don\'t have required permissions")
    channels = body.channels
    body.channels = []
    db_model = DBPost(**body.dict())
    for i in channels:
        channel = db_session.query(DBChannel).join(DBOrganizationBot).filter(DBChannel.id == i,
                                                                             DBOrganizationBot.organization_id == organization_id).first()
        if channel is None:
            response.status_code = 403
            return ErrorResponse(reason="Don\'t have required permissions")
        db_model.channels.append(channel)
    db_model.organization_id = organization_id
    db_model.created_by = current_user.id
    db_session.add(db_model)
    db_session.commit()
    response.status_code = 201
    db_model.id = db_session.query(DBPost).order_by(DBPost.id.desc()).first().id
    post = Post(**db_model.dict(), created_by_name=db_model.user.name,
                channels=[Channel(**j.dict()) for j in db_model.channels], tags=[k.tag for k in db_model.tag_bindings],
                sent_infos=[PostSentInfo(**k.dict()) for k in db_model.sent_infos])
    return AddNewPostResponse(post=post)


@router.delete(
    '/{organization_id}/posts',
    response_model=Union[DeletePostResponse, ErrorResponse],
    responses={
        '200': {'model': DeletePostResponse},
        '400': {'model': ErrorResponse},
        '401': {'model': ErrorResponse},
        '403': {'model': ErrorResponse}
    }, tags=["posts"]
)
def delete_post(
        organization_id: int,
        response: Response, body: DeletePostRequest, db_session: Session = Depends(get_session),
        current_user: DBUser = Depends(get_current_user)
) -> Union[DeletePostResponse, ErrorResponse]:
    if current_user.organization_bindings.join(DBPermission).filter(
            DBOrganizationUser.organization_id == organization_id, DBPermission.level.in_([4, 5])).count() == 0:
        response.status_code = 403
        return ErrorResponse(reason="Don\'t have required permissions")
    post = db_session.query(DBPost).filter(DBPost.organization_id == organization_id, DBPost.id == body.id).first()
    if post is None:
        return ErrorResponse(reason="No such post")
    post.channels = []
    for tag in post.tag_bindings:
        db_session.delete(tag)
    db_session.delete(post)
    db_session.commit()
    return DeletePostResponse(**body.dict())


@router.get(
    '/{organization_id}/posts',
    response_model=Union[GetPostsResponse, ErrorResponse],
    responses={
        '200': {'model': GetPostsResponse},
        '401': {'model': ErrorResponse},
        '403': {'model': ErrorResponse}
    }, tags=["posts"]
)
def get_active_posts(
        organization_id: int,
        response: Response, db_session: Session = Depends(get_session), current_user=Depends(get_current_user)
) -> Union[GetPostsResponse, ErrorResponse]:
    if current_user.organization_bindings.join(DBPermission).filter(
            DBOrganizationUser.organization_id == organization_id).count() == 0:
        response.status_code = 403
        return ErrorResponse(reason="Don\'t have required permissions")
    posts: list[DBPost] = db_session.query(DBPost).filter(DBPost.sent_status != SentStatus.SENT_OK,
                                                          DBPost.organization_id == organization_id).all()
    return GetPostsResponse(
        posts=[Post(**i.dict(), created_by_name=i.user.name, channels=[Channel(**j.dict()) for j in i.channels],
                    tags=[k.tag for k in i.tag_bindings],
                    sent_infos=[PostSentInfo(**k.dict()) for k in i.sent_infos]) for i
               in posts])


@router.patch(
    '/{organization_id}/posts',
    response_model=Union[EditPostResponse, ErrorResponse],
    responses={
        '200': {'model': EditPostResponse},
        '401': {'model': ErrorResponse},
        '403': {'model': ErrorResponse}
    }, tags=["posts"]
)
def edit_post(
        organization_id: int,
        response: Response, body: EditPostRequest, db_session: Session = Depends(get_session),
        current_user=Depends(get_current_user)
) -> Union[EditPostResponse, ErrorResponse]:
    if current_user.organization_bindings.filter(
            DBOrganizationUser.organization_id == organization_id).count() == 0:
        response.status_code = 403
        return ErrorResponse(reason="Don\'t have required permissions")
    if db_session.query(DBPost).filter(DBPost.id == body.id, DBPost.organization_id == organization_id,
                                       DBPost.sent_status != SentStatus.SENT_OK,
                                       DBPost.sent_status != SentStatus.WAITING).count() == 0:
        response.status_code = 403
        return ErrorResponse(reason="Don\'t have required permissions")
    if body.is_approved in [Status.APPROVED, Status.REJECTED]:
        permissions = [3, 4, 5]
    else:
        permissions = [2, 4, 5]
    if (body.is_approved is not None) and current_user.organization_bindings.join(DBPermission).filter(
            DBOrganizationUser.organization_id == organization_id, DBPermission.level.in_(permissions)).count() == 0:
        response.status_code = 403
        return ErrorResponse(reason="Don\'t have required permissions")
    if (body.content is not None or body.channels is not None) and current_user.organization_bindings.join(
            DBPermission).filter(
        DBOrganizationUser.organization_id == organization_id, DBPermission.level.in_([2, 4, 5])).count() == 0:
        response.status_code = 403
        return ErrorResponse(reason="Don\'t have required permissions")
    if (body.comment is not None) and current_user.organization_bindings.join(
            DBPermission).filter(
        DBOrganizationUser.organization_id == organization_id, DBPermission.level.in_([3, 4, 5])).count() == 0:
        response.status_code = 403
        return ErrorResponse(reason="Don\'t have required permissions")
    db_model: DBPost = db_session.query(DBPost).filter(DBPost.id == body.id).first()
    if body.channels is not None:
        db_model.channels = []
        for i in body.channels:
            channel = db_session.query(DBChannel).join(DBOrganizationBot).filter(DBChannel.id == i,
                                                                                 DBOrganizationBot.organization_id == organization_id).first()
            if channel is None:
                response.status_code = 403
                return ErrorResponse(reason="Don\'t have required permissions")
            db_model.channels.append(channel)
    if body.tags is not None:
        for tag in db_model.tag_bindings:
            db_session.delete(tag)
        for i in body.tags:
            tag = DBTag(tag=i, post_id=body.id)
            db_session.add(tag)
            db_model.tag_bindings.append(tag)
    if body.is_approved is not None:
        db_model.is_approved = body.is_approved
    if body.comment is not None:
        db_model.comment = body.comment
    if body.content is not None:
        db_model.content = body.content
        db_model.is_approved = Status.OPEN
    db_session.add(db_model)
    db_session.commit()
    return EditPostResponse(post=Post(**db_model.dict(), created_by_name=db_model.user.name,
                                      channels=[Channel(**j.dict()) for j in db_model.channels],
                                      tags=[k.tag for k in db_model.tag_bindings],
                                      sent_infos=[PostSentInfo(**k.dict()) for k in db_model.sent_infos]))


@router.get(
    '/{organization_id}/inactive_posts',
    response_model=Union[GetPostsResponse, ErrorResponse],
    responses={
        '200': {'model': GetPostsResponse},
        '401': {'model': ErrorResponse},
        '403': {'model': ErrorResponse}
    }, tags=["posts"]
)
def get_inactive_posts(
        organization_id: int,
        response: Response, db_session: Session = Depends(get_session), current_user=Depends(get_current_user)
) -> Union[GetPostsResponse, ErrorResponse]:
    if current_user.organization_bindings.join(DBPermission).filter(
            DBOrganizationUser.organization_id == organization_id).count() == 0:
        response.status_code = 403
        return ErrorResponse(reason="Don\'t have required permissions")
    posts: list[DBPost] = db_session.query(DBPost).filter(DBPost.sent_status == SentStatus.SENT_OK,
                                                          DBPost.organization_id == organization_id).all()
    return GetPostsResponse(
        posts=[Post(**i.dict(), created_by_name=i.user.name, channels=[Channel(**j.dict()) for j in i.channels],
                    tags=[k.tag for k in i.tag_bindings],
                    sent_infos=[PostSentInfo(**k.dict()) for k in i.sent_infos]) for i
               in posts])


@router.get(
    '/{organization_id}/mypermissions',
    response_model=Union[OrganizationUser, ErrorResponse],
    responses={
        '200': {'model': OrganizationUser},
        '401': {'model': ErrorResponse},
        '404': {'model': ErrorResponse}
    }, tags=["permissions"]
)
def get_my_permissions(
        organization_id: int,
        response: Response, current_user=Depends(get_current_user), db_session=Depends(get_session)
) -> Union[OrganizationUser, ErrorResponse]:
    if current_user.organization_bindings.join(DBPermission).filter(
            DBOrganizationUser.organization_id == organization_id).count() == 0:
        response.status_code = 403
        return ErrorResponse(reason="Don\'t have required permissions")
    user_data = db_session.query(DBOrganizationUser).filter(DBOrganizationUser.organization_id == organization_id,
                                                            DBOrganizationUser.user_id == current_user.id).all()
    if not user_data:
        response.status_code = 404
        return ErrorResponse(reason="Not found")
    return get_uniq_users(user_data)[0]


@router.post(
    '/{organization_id}/posts/{post_id}/schedule',
    response_model=Union[PostIdResponse, ErrorResponse],
    responses={
        '200': {'model': PostIdResponse},
        '400': {'model': ErrorResponse},
        '401': {'model': ErrorResponse},
        '403': {'model': ErrorResponse},
        '404': {'model': ErrorResponse},
    }, tags=["posts"]
)
def schedule_post(organization_id: int, post_id: int, response: Response, body: ScheduleTimeRequest,
                  db_session: Session = Depends(get_session),
                  current_user=Depends(get_current_user)) -> Union[PostIdResponse, ErrorResponse]:
    if current_user.organization_bindings.join(DBPermission).filter(
            DBOrganizationUser.organization_id == organization_id, DBPermission.level.in_([2, 4, 5])).count() == 0:
        response.status_code = 403
        return ErrorResponse(reason="Don\'t have required permissions")
    post_model = db_session.query(DBPost).join(DBOrganization).filter(DBPost.id == post_id,
                                                                      DBOrganization.id == organization_id).first()
    if post_model is None:
        response.status_code = 404
        return ErrorResponse(reason="Not found")
    if post_model.is_approved != Status.APPROVED or post_model.sent_status != SentStatus.NOT_READY:
        response.status_code = 400
        return ErrorResponse(reason="Post must be approved")
    if len(post_model.organization.bots) == 0:
        response.status_code = 400
        return ErrorResponse(reason="Organization has not any bots")
    post_model.planned_time = body.time
    post_model.sent_status = SentStatus.WAITING
    db_session.add(post_model)
    for channel in post_model.channels:
        task = DBTask(handler="send_message",
                      arguments={"bot_token": channel.bot.bot_token, "telegram_channel_id": channel.telegram_id,
                                 "message_text": post_model.content, "post_id": post_model.id,
                                 "channel_id": channel.id, "organization_id": organization_id},
                      planned_time=body.time)
        db_session.add(task)
    db_session.commit()
    return PostIdResponse(**post_model.dict())


@router.post(
    '/{organization_id}/block_tasks',
    response_model=Union[OrganizationStopToggleIdResponse, ErrorResponse],
    responses={
        '200': {'model': OrganizationStopToggleIdResponse},
        '401': {'model': ErrorResponse},
        '403': {'model': ErrorResponse},
        '409': {'model': ErrorResponse},
    }, tags=["organizations"]
)
def block_tasks(organization_id: int, response: Response,
                db_session: Session = Depends(get_session),
                current_user=Depends(get_current_user)) -> Union[OrganizationStopToggleIdResponse, ErrorResponse]:
    if current_user.organization_bindings.join(DBPermission).filter(
            DBOrganizationUser.organization_id == organization_id, DBPermission.level >= 4).count() == 0:
        response.status_code = 403
        return ErrorResponse(reason="Don\'t have required permissions")
    block_model = DBOrganizationStopToggle(organization_id=organization_id)
    db_session.add(block_model)
    try:
        db_session.commit()
    except:
        response.status_code = 409
        return ErrorResponse(reason="Already blocked")
    return OrganizationStopToggleIdResponse(**block_model.dict())


@router.post(
    '/{organization_id}/unblock_tasks',
    response_model=Union[OrganizationStopToggleIdResponse, ErrorResponse],
    responses={
        '200': {'model': OrganizationStopToggleIdResponse},
        '400': {'model': ErrorResponse},
        '401': {'model': ErrorResponse},
        '403': {'model': ErrorResponse},
    }, tags=["organizations"]
)
def unblock_tasks(organization_id: int, response: Response,
                  db_session: Session = Depends(get_session),
                  current_user=Depends(get_current_user)) -> Union[OrganizationStopToggleIdResponse, ErrorResponse]:
    if current_user.organization_bindings.join(DBPermission).filter(
            DBOrganizationUser.organization_id == organization_id, DBPermission.level >= 4).count() == 0:
        response.status_code = 403
        return ErrorResponse(reason="Don\'t have required permissions")
    block_model = db_session.query(DBOrganizationStopToggle).filter(
        DBOrganizationStopToggle.organization_id == organization_id).first()
    if block_model is None:
        response.status_code = 400
        return ErrorResponse(reason="Not blocked")
    db_session.delete(block_model)
    db_session.commit()
    return OrganizationStopToggleIdResponse(organization_id=organization_id)
