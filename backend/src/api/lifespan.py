__all__ = ["lifespan"]

import json
import httpx
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import timeout
from pymongo.errors import ConnectionFailure
from starlette.datastructures import State

from src.config import settings
from src.logging_ import logger
from src.storages.mongo import document_models


async def setup_database() -> AsyncIOMotorClient:
    # ------------------- Repositories Dependencies -------------------

    motor_client = AsyncIOMotorClient(
        settings.database.uri.get_secret_value(), connectTimeoutMS=5000, serverSelectionTimeoutMS=5000
    )

    # healthcheck mongo
    try:
        with timeout(1):
            server_info = await motor_client.server_info()
            server_info_pretty_text = json.dumps(server_info, indent=2, default=str)
            logger.info(f"Connected to MongoDB: {server_info_pretty_text}")
    except ConnectionFailure as e:
        logger.critical("Could not connect to MongoDB: %s" % e)
        raise e

    mongo_db = motor_client.get_default_database()
    await init_beanie(database=mongo_db, document_models=document_models, recreate_views=True)
    return motor_client


async def setup_predefined() -> None:
    from src.modules.user.repository import user_repository
    from src.modules.files.repository import files_repository

    await user_repository.create_predefined_users()
    await files_repository.insert_all_existing_files()
    await files_repository.check_existing_files()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Application startup

    motor_client = await setup_database()
    if TYPE_CHECKING:
        app.state = State()
    await setup_predefined()

    app.state.httpx_client = httpx.AsyncClient()

    yield

    # Application shutdown
    motor_client.close()
    await app.state.httpx_client.aclose()
