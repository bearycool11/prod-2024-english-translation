wait-for-it smm_ya_database:5432
alembic upgrade head
uvicorn main:app --host 0.0.0.0 --port 5437
#python3 main.py