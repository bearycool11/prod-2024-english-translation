from fastapi import FastAPI, APIRouter
from passlib.context import CryptContext
from starlette.middleware.cors import CORSMiddleware

from handlers import private, organizations, auth

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


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

router.include_router(private.router)
router.include_router(auth.router)
router.include_router(organizations.router)
app.include_router(router)
