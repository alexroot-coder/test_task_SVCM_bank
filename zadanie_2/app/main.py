import service
import schemas
from fastapi import Depends, FastAPI, HTTPException
from dependencies import engine, get_db, Base, init_db
from sqlalchemy.ext.asyncio import AsyncSession


app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.patch("/users/{id}/addresses/{address_id}", response_model=schemas.AddressUpdate, tags=['Задание_2'])
async def update_user_address(id: int = None, address_id: int = None, user_address: schemas.AddressUpdate = None,
                              db: AsyncSession = Depends(get_db)):
    db_user_address = await service.update_user_address(id=id, db=db, address_id=address_id, user_address=user_address)
    return db_user_address


@app.get("/user/{id}", response_model=schemas.ShowUserByID, tags=['Задание_2'])
async def get_user_data(id: int = None, db: AsyncSession = Depends(get_db)):
    users = await service.get_user_data(db, id)
    if users is None:
        raise HTTPException(status_code=404, detail="User not found")
    return users


@app.get("/users", response_model=list[schemas.ViewUser], tags=['Задание_2'])
async def get_users(db: AsyncSession = Depends(get_db)):
    return await service.get_all_users(db)


@app.post("/users/{id}/address", response_model=list[schemas.UserAddress], tags=['Задание_2'])
async def add_address_for_user(id: int = None, user_address: list[schemas.UserAddAddress] = None, db: AsyncSession = Depends(get_db)):
    return await service.add_address_for_user_by_user_id(db=db, user_id=id, user_address=user_address)


@app.post("/user", response_model=schemas.User, tags=['Задание_2'])
async def add_user(user: schemas.User, db: AsyncSession = Depends(get_db)):
    return await service.create_user(db=db, user_def=user)


@app.put("/user/{id}", response_model=schemas.User, tags=['Задание_2'])
async def update_user(id: int = None, user: schemas.User = None, db: AsyncSession = Depends(get_db)):
    return await service.update_user_by_id(db=db, id=id, user=user)


@app.delete("/user/{id}", response_model=schemas.ViewUser, tags=['Задание_2'])
async def delete_user(id: int = None, db: AsyncSession = Depends(get_db)):
    result = await service.delete_user(db, id)
    return result


@app.delete("/users/{id}/addresses/{address_id}", response_model=schemas.UserAddress, tags=['Задание_2'])
async def delete_user_address(id: int = None, address_id: int = None,
                              db: AsyncSession = Depends(get_db)):
    db_user_address = await service.delete_user_address(id=id, db=db, address_id=address_id)
    return db_user_address
