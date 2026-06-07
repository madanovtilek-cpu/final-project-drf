from fastapi import APIRouter, Depends, HTTPException
from shop_app.database.models import UserProfile
from shop_app.database.schema import UserProfileOutSchema, UserProfileInputSchema
from shop_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

users_router = APIRouter(prefix='/users', tags=['UserProfile'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@users_router.post('/', response_model=UserProfileOutSchema)
async def create_user(user: UserProfileInputSchema, db: Session = Depends(get_db)) :
    user_db = UserProfile(**user.dict())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db








@users_router.put('/{user_id}/', response_model=dict)
async def update_user(user_id: int, user: UserProfileInputSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(detail='Мындай колдонуучу жок', status_code=400)

    for user_key, user_value in user.model_dump().items():
        setattr(user_db, user_key, user_value)

    db.commit()
    db.refresh(user_db)
    return {'message': 'Колдонуучу өзгөртүлдү'}


@users_router.delete('/{user_id}/', response_model=dict)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(detail='Мындай колдонуучу жок', status_code=400)

    db.delete(user_db)
    db.commit()
    return {'message': 'Колдонуучу удалить болду'}

