from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import create_db_and_tables
from app.routers import expenses_category, auth, accounts

@asynccontextmanager
async def lifespan(_: FastAPI):
    # Load the database and create tables
    create_db_and_tables()
    yield
    # Clean up and release the resources

app = FastAPI(lifespan=lifespan)

# Include your routers here
app.include_router(expenses_category.router)
app.include_router(auth.router)
app.include_router(accounts.router)


