from fastapi import APIRouter, Depends, HTTPException, status
from shop_app.database.models import SubCategory, Category
from shop_app.database.schema import SubCategoryOutSchema, SubCategoryInputSchema
from shop_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

subcategories_router = APIRouter(prefix='/subcategories', tags=['SubCategory'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@subcategories_router.post('/', response_model=SubCategoryOutSchema, status_code=status.HTTP_201_CREATED)
async def create_subcategory(subcategory: SubCategoryInputSchema, db: Session = Depends(get_db)):
    category_exists = db.query(Category).filter(Category.id == subcategory.category_id).first()
    if not category_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ката: ID = {subcategory.category_id} болгон башкы категория базада жок!"
        )

    subcategory_exists = db.query(SubCategory).filter(
        SubCategory.subcategory_name == subcategory.subcategory_name,
        SubCategory.category_id == subcategory.category_id
    ).first()

    if subcategory_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Бул категорияда мындай аталыштагы субкатегория буга чейин түзүлгөн!"
        )

    subcategory_db = SubCategory(**subcategory.model_dump())
    db.add(subcategory_db)
    db.commit()
    db.refresh(subcategory_db)
    return subcategory_db





@subcategories_router.put('/{subcategory_id}/', response_model=dict)
async def update_subcategory(subcategory_id: int, subcategory: SubCategoryInputSchema, db: Session = Depends(get_db)):
    subcategory_db = db.query(SubCategory).filter(SubCategory.id == subcategory_id).first()
    if not subcategory_db:
        raise HTTPException(detail='Мындай субкатегория жок', status_code=400)

    category_exists = db.query(Category).filter(Category.id == subcategory.category_id).first()
    if not category_exists:
        raise HTTPException(
            status_code=400,
            detail=f"Ката: ID = {subcategory.category_id} болгон башкы категория базада жок!"
        )

    for sub_key, sub_value in subcategory.model_dump().items():
        setattr(subcategory_db, sub_key, sub_value)

    db.commit()
    db.refresh(subcategory_db)
    return {'message': 'Субкатегория өзгөрүлдү'}


@subcategories_router.delete('/{subcategory_id}/', response_model=dict)
async def delete_subcategory(subcategory_id: int, db: Session = Depends(get_db)):
    subcategory_db = db.query(SubCategory).filter(SubCategory.id == subcategory_id).first()
    if not subcategory_db:
        raise HTTPException(detail='Мындай субкатегория жок', status_code=400)

    db.delete(subcategory_db)
    db.commit()
    return {'message': 'Субкатегория удалить болду'}