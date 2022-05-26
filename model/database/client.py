from motor.motor_asyncio import AsyncIOMotorClient
from bot import MONGODB_URI

db_client = AsyncIOMotorClient(MONGODB_URI)
