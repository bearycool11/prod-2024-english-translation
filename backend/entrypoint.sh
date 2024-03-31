wait-for-it smm_you_database:5432
# alembic upgrade head
uvicorn main:app --host 0.0.0.0 --port 5437