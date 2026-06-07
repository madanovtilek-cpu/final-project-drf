from fastapi import APIRouter, Depends, HTTPException, status
from shop_app.database.models import Product, SubCategory
from shop_app.database.schema import ProductOutSchema, ProductInputSchema
from shop_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

products_router = APIRouter(prefix='/products', tags=['Product'])


# База менен туташуу
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@products_router.post('/', response_model=ProductOutSchema, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductInputSchema, db: Session = Depends(get_db)):
    # 1-текшерүү: Киргизилген subcategory_id базада барбы?
    # Эскертүү: Эгер input схемаңызда subcategory_id жок болсо, аны сөзсүз кошуңуз!
    subcategory_exists = db.query(SubCategory).filter(SubCategory.id == product.subcategory_id).first()
    if not subcategory_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ката: ID = {product.subcategory_id} болгон субкатегория базада жок!"
        )

    article_exists = db.query(Product).filter(Product.article_number == product.article_number).first()
    if article_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ката: Артикул №{product.article_number} болгон продукт базада мурун эле бар!"
        )

    # Базага сактоо
    product_db = Product(**product.model_dump())
    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db


@products_router.get('/', response_model=List[ProductOutSchema])
async def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@products_router.get('/{product_id}/', response_model=ProductOutSchema)
async def detail_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мындай ID менен продукт табылган жок"
        )
    return product

@products_router.put('/{product_id}/', response_model=dict)
async def update_product(product_id: int, product: ProductInputSchema, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(detail='Мындай продукт жок', status_code=400)

    subcategory_exists = db.query(SubCategory).filter(SubCategory.id == product.subcategory_id).first()
    if not subcategory_exists:
        raise HTTPException(
            status_code=400,
            detail=f"Ката: ID = {product.subcategory_id} болгон субкатегория базада жок!"
        )

    for prod_key, prod_value in product.model_dump().items():
        setattr(product_db, prod_key, prod_value)

    db.commit()
    db.refresh(product_db)
    return {'message': 'Продукт өзгөрүлдү'}


@products_router.delete('/{product_id}/', response_model=dict)
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(detail='Мындай продукт жок', status_code=400)

    db.delete(product_db)
    db.commit()
    return {'message': 'Продукт удалить болду'}