from fastapi import FastAPI
from models import PingResponse

app = FastAPI(
    title='Pulse API',
    version='1.0',
)


@app.get('/ping', response_model=PingResponse)
def ping() -> PingResponse:
    return PingResponse(status="ok")
