from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import SQLAlchemyError
from odoo_contacts.logger import logger
from odoo_contacts.sql.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, obj_id: int):
        """Find object by ID"""
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(id=obj_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        """Find object by any filters"""
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls):
        """Find all objects from table"""
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(cls, **data):
        """Insert object to DB"""
        try:
            async with async_session_maker() as session:
                query = insert(cls.model).values(**data).returning(cls.model.id)
                result = await session.execute(query)
                await session.commit()
                return result.mappings().first()
        except (SQLAlchemyError, Exception) as e:
            msg = ''
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot insert data into table"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot insert data into table"

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None

    @classmethod
    async def update(cls, obj_id: int, **kwargs):
        """Insert object in DB"""
        try:
            query = update(cls.model).where(cls.model.id == obj_id).values(**kwargs)
            async with async_session_maker() as session:
                await session.execute(query)
                await session.commit()
        except (SQLAlchemyError, Exception) as e:
            msg = ''
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot update data in table"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot insert data in table"

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None

    @classmethod
    async def add_bulk(cls, *data):
        """Insert objects to DB"""
        # For inserting array of data [{"id": 1}, {"id": 2}]
        try:
            query = insert(cls.model).values(*data).returning(cls.model.id)
            async with async_session_maker() as session:
                result = await session.execute(query)
                await session.commit()
                return result.mappings().first()
        except (SQLAlchemyError, Exception) as e:
            msg = ''
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc"
            elif isinstance(e, Exception):
                msg = "Unknown Exc"
            msg += ": Cannot bulk insert data into table"

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None

    @classmethod
    async def delete(cls, **filter_by):
        """Delete object from DB"""
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()
