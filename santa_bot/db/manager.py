import asyncio
import logging

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from santa_bot import config
from santa_bot.db.engine_manager import EngineManager
from santa_bot.db.tables import User, Base


class DBManager:
    def __init__(self):
        self.session_maker = None
        asyncio.run(self._init())

    async def _init(self):
        async with EngineManager(config.DATABASE_URL) as engine:
            self.session_maker = async_sessionmaker(engine, expire_on_commit=False)
            logging.info("HEREE")
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

    async def close(self):
        async with self.session_maker() as session:
            session.close()

    async def get_records(self, model, **kwargs):
        query = select(model).where(
            *[getattr(model, key) == value for key, value in kwargs.items()]
        )
        async with self.session_maker() as session:
            result = await session.execute(query)
            records = result.scalars().all()
        return records

    async def add_record(self, new_record):
        async with self.session_maker() as session:
            async with session.begin():
                session.add(new_record)
                await session.commit()
                return new_record

    async def get_record(self, model, **kwargs):
        return (
            records[0]
            if (records := (await self.get_records(model, **kwargs)))
            else None
        )

    async def update_record(self, user_id: int, **kwargs):
        async with self.session_maker() as session:
            async with session.begin():
                # noinspection PyTypeChecker
                query = (
                    update(User)
                    .values(**kwargs)
                    .where(User.id == user_id)
                )
                await session.execute(query)
                await session.commit()


db_manager = DBManager()
