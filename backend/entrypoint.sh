wait-for-it smm_ya_database:5432
alembic upgrade head
uvicorn main:app --host 0.0.0.0 --port 5437 --proxy-headers --forwarded-allow-ips="172.31.0.5"