from typing import Union

from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import Response

from database.database_connector import get_session
from database.models import DBPost, DBSentPostInfo
from models import StatusResponse, ErrorResponse, PrivateSetPostStatusRequest

router = APIRouter(prefix='/private')


@router.post(
    "/set_post_sent_state",
    response_model=Union[StatusResponse, ErrorResponse],
    responses={
        '200': {'model': StatusResponse},
        '400': {'model': ErrorResponse},
        '403': {'model': ErrorResponse},
        '404': {'model': ErrorResponse},
    },
    include_in_schema=False,
)
def set_post_sent_state(request: Request, response: Response, body: PrivateSetPostStatusRequest,
                        db_session=Depends(get_session)):
    if not request.client.host.startswith("172.31."):
        response.status_code = 403
        return ErrorResponse(reason="access denied")
    post = db_session.query(DBPost).filter(DBPost.id == body.post_id).first()
    if post is None:
        response.status_code = 404
        return ErrorResponse(reason="not found")
    post.sent_status = body.post_status
    if body.clear_planned_time:
        post.planned_time = None
    if body.post_status == "SENT_OK":
        post_send_data = DBSentPostInfo(channel_id=body.channel_id,
                                        post_id=body.post_id,
                                        telegram_message_id=body.telegram_message_id,
                                        chat_username=body.chat_username)
        db_session.add(post_send_data)
    db_session.add(post)
    try:
        db_session.commit()
    except:
        response.status_code = 400
        return ErrorResponse(reason="bad request")
    return StatusResponse(status="ok")
