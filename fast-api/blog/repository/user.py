from fastapi import Depends, status, HTTPException
from blog import schemas
from blog import models
from blog import hash_p
from blog.database import get_db
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import create_engine, Column, Integer, String, select
from typing import Tuple, Optional, Dict, Any


async def create(request: schemas.User, db: AsyncSession = Depends(get_db)) -> models.Users:
    new_user: models.Users = models.Users(
        name=request.name, email=request.email,
        password=hash_p.hashing.create_hash(request.password))
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    finally:
        await db.close()
    return new_user


async def get(id: int, db: AsyncSession = Depends(get_db)) -> Optional[Dict[str, str]]:
    # add types please
    statement = select(models.Users.name, models.Users.email).where(
        models.Users.id == id)
    result = await db.execute(statement)
    user: schemas.ShowUserNameAndEmail = result.first()
    # print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user
