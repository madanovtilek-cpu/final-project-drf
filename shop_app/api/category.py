from fastapi import APIRouter, Depends, HTTPException, status
from shop_app.database.models import Category
from shop_app.database.schema import CategoryOutSchema, CategoryInputSchema
from shop_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

categories_router = APIRouter(prefix='/categories', tags=['Category'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@categories_router.post('/', response_model=CategoryOutSchema, status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryInputSchema, db: Session = Depends(get_db)):
    category_exists = db.query(Category).filter(Category.category_name == category.category_name).first()
    if category_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Мындай аталыштагы категория буга чейин түзүлгөн!'
        )

    category_db = Category(**category.model_dump())
    db.add(category_db)
    db.commit()
    db.refresh(category_db)
    return category_db


@categories_router.get('/', response_model=List[CategoryOutSchema])
async def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


@categories_router.get('/{category_id}/', response_model=CategoryOutSchema)
async def detail_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Мындай ID менен категория табылган жок'
        )
    return category


@categories_router.put('/{category_id}/', response_model=dict)
async def update_category(category_id: int, category: CategoryInputSchema,
                          db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if not category_db:
        raise HTTPException(detail='Мындай категори жок', status_code=400)

    for category_key, category_value in category.dict().items():
        setattr(category_db, category_key, category_value)

    db.commit()
    db.refresh(category_db)
    return {'message': 'Категори озгорулду'}


@categories_router.delete('/{category_id}/', response_model=dict)
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if not category_db:
        raise HTTPException(detail='Мындай категори жок', status_code=400)

    db.delete(category_db)
    db.commit()
    return {'message': 'Категори удалить болду'}