from fastapi import FastAPI, APIRouter
from models import PingResponse

app = FastAPI(
    title='SMM app API',
    version='1.0',
)

router = APIRouter(prefix='/api')

@router.get('/ping', response_model=PingResponse)
def ping() -> PingResponse:
    return PingResponse(status="ok")