import schemas
import models
from fastapi import HTTPException
from sqlalchemy import select, update
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_users(db: AsyncSession):
    all_users = await db.execute(select(models.User))
    return all_users.scalars().all()


async def get_user_data(db: AsyncSession, id: int):
    user = await db.execute(select(models.User).filter(models.User.id == id))
    user = user.scalars().first()
    user_addresses = await db.execute(select(models.Address).filter(models.Address.user_id == id))
    user_addresses = user_addresses.scalars().all()
    if user_addresses:
        return {"name": user.name, "id": user.id, "address": jsonable_encoder(user_addresses)}
    elif not user:
        return user
    else:
        return {"name": user.name, "id": user.id, "address": []}


async def update_user_address(db: AsyncSession, address_id: int, user_address, id: int):
    user = await db.execute(select(models.User).filter(models.User.id == id))
    user = user.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        tmp_user = await db.execute(select(models.Address).filter(models.Address.id == address_id))
        tmp_user = tmp_user.scalars().first()
        if tmp_user is None:
            raise HTTPException(status_code=404, detail="Address not found")
        if tmp_user:
            asd = jsonable_encoder(tmp_user)
            address_data = user_address.dict(exclude_unset=True)
            for key, value in address_data.items():
                asd[key] = value
            tmp = models.Address(**asd)
            await db.execute(update(models.Address).filter(models.Address.id == address_id).values(jsonable_encoder(tmp)))
            await db.commit()
    return tmp_user


async def create_user(db: AsyncSession, user_def: schemas.User):
    tmp_user = models.User(name=user_def.name)
    db.add(tmp_user)
    await db.commit()
    return tmp_user


async def delete_user(db: AsyncSession, id: int):
    user = await db.execute(select(models.User).filter(models.User.id == id))
    user = user.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    return user


async def delete_user_address(db: AsyncSession, id: int, address_id: int):
    user = await db.execute(select(models.User).filter(models.User.id == id))
    user = user.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    address = await db.execute(select(models.Address).filter(models.Address.id == address_id))
    address = address.scalars().first()
    if address is None:
        raise HTTPException(status_code=404, detail="Address not found")

    await db.delete(address)
    await db.commit()
    return address


async def add_address_for_user_by_user_id(db: AsyncSession, user_id: int, user_address):
    db_user = await db.execute(select(models.User).filter(models.User.id == user_id))
    db_user = db_user.scalars().first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    list_of_addresses = []
    for address in user_address:
        list_of_addresses.append(models.Address(**address.dict(), user_id=user_id))
    db.add_all(list_of_addresses)
    await db.commit()
    return list_of_addresses


async def update_user_by_id(db: AsyncSession, id: int, user):
    user_id = await db.execute(select(models.User).filter(models.User.id == id))
    if not user_id.scalars().first():
        raise HTTPException(status_code=404, detail="User not found")
    result = await db.execute(update(models.User).filter(models.User.id == id).values(jsonable_encoder(user)))
    await db.commit()
    user_id = await db.execute(select(models.User).filter(models.User.id == id))
    return user_id.scalars().first()
