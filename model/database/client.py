from motor.motor_asyncio import AsyncIOMotorClient
from bot import DB_CONNECTION

db_client = AsyncIOMotorClient(DB_CONNECTION)
