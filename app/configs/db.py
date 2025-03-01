from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm import sessionmaker 

Database_url="postgresql+asyncpg://postgres:9843@localhost/fast"
engine=create_async_engine(Database_url)

AsyncSessionLocal=sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session