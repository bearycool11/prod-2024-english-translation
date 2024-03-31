import os
from dotenv import load_dotenv

load_dotenv()
database_url = os.getenv("POSTGRES_CONN")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 720
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change_me_pls")
