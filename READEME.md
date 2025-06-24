docker run --name fastapi-postgres \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=admin \
  -e POSTGRES_DB=homebudgetapi_db \
  -p 5432:5432 \
  -d postgres