echo "Running migrations"
alembic -x url=$DATABASE_CONNECTION_STRING upgrade head

# Run fastapi app
echo "Running fastapi app"
python src/main.py