import schemas
import models
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException


def get_all_users(db: Session):
    all_users = db.query(models.User).all()
    return all_users


def get_user_data(db: Session, id: int):
    user_id = db.query(models.User).filter(models.User.id == id).first()
    user = db.query(models.User).join(models.Address).filter(models.User.id == models.Address.user_id,
                                                             models.Address.user_id == id).first()
    if user:
        return user
    elif not user_id:
        return user_id
    else:
        return {"name": user_id.name, "id": user_id.id, "address": []}


def update_user_address(db: Session, address_id: int, user_address, id: int):

    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        tmp_user = db.query(models.Address).filter(models.Address.id == address_id).first()
        if tmp_user:
            asd = jsonable_encoder(tmp_user)
            address_data = user_address.dict(exclude_unset=True)
            for key, value in address_data.items():
                asd[key] = value
            tmp = models.Address(**asd)
            db.query(models.Address).filter(models.Address.id == address_id).update(jsonable_encoder(tmp))
            db.commit()
    return tmp_user


def create_user(db: Session, user_def: schemas.User):
    tmp_user = models.User(name=user_def.name)
    db.add(tmp_user)
    db.commit()
    return tmp_user


def delete_user(db: Session, id: int):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return user


def delete_user_address(db: Session, id: int, address_id: int):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if address is None:
        raise HTTPException(status_code=404, detail="Address not found")

    db.delete(address)
    db.commit()
    return address


def add_address_for_user_by_user_id(db: Session, user_id: int, user_address):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    list_of_addresses = []
    for address in user_address:
        list_of_addresses.append(models.Address(**address.dict(), user_id=user_id))
        print(address)
    db.add_all(list_of_addresses)
    db.commit()
    return list_of_addresses


def update_user_by_id(db: Session, id: int, user):
    user_id = db.query(models.User).filter(models.User.id == id).first()
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    user_id.name = user.name
    db.add(user_id)
    db.commit()
    return user_id

