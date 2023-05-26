from app.core.configs import settings
from app.core.database import engine
import aiomysql

async def create_tables() -> None:
    import app.models.__all_models
    print('Create db')

    async with engine.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)

    print('Tables created')

    await engine.dispose()


if __name__ == '__main__':
    import asyncio

    asyncio.run(create_tables())