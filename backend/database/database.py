from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from envparse import Env
from dotenv import load_dotenv
from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import DeclarativeBase

from backend.database.hash import config


env = Env()

load_dotenv()


DATABASE_URL = env.str('DATABASE_URL')

engine = create_async_engine(DATABASE_URL, future=True, echo=False)

new_session = async_sessionmaker(autoflush=False, expire_on_commit=False, bind=engine)

SECRET_KEY = env.str("SECRET_KEY")
config.JWT_SECRET_KEY = SECRET_KEY

async def get_session():
    async with new_session() as session:
        yield session

session_dep = Annotated[AsyncSession, Depends(get_session)]

class Base(DeclarativeBase):
    pass

#Потом не понадобится
#def get_user_requests(ip_address: str):
#    with new_session() as session:
#        query = select(ChatRequest).filter_by(ip_address=ip_address)
#        result = session.execute(query)

#        return result.scalars().all()


#Это можно делать через ручку добавления
#def add_request_data(ip_address: str, prompt: str, response: str) -> None:
#    with new_session() as session:
#        new_request = ChatRequest(
#            ip_address=ip_address,
#            prompt=prompt,
#            response=response
#        )
        
#        session.add(new_request)
#        session.commit()