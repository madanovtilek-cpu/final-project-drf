from fastapi import APIRouter, Depends, HTTPException, status
from shop_app.database.models import ProductImage, Product
from shop_app.database.schema import ProductImageOutSchema, ProductImageInputSchema
from shop_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

product_images_router = APIRouter(prefix='/product-images', tags=['ProductImage'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@product_images_router.post('/', response_model=ProductImageOutSchema, status_code=status.HTTP_201_CREATED)
async def create_product_image(product_image: ProductImageInputSchema, db: Session = Depends(get_db)):
    product_exists = db.query(Product).filter(Product.id == product_image.product_id).first()
    if not product_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ката: ID = {product_image.product_id} болгон продукт базада жок!"
        )

    image_db = ProductImage(**product_image.model_dump())
    db.add(image_db)
    db.commit()
    db.refresh(image_db)
    return image_db


@product_images_router.get('/', response_model=List[ProductImageOutSchema])
async def list_product_images(db: Session = Depends(get_db)):
    return db.query(ProductImage).all()


@product_images_router.get('/{image_id}/', response_model=ProductImageOutSchema)
async def detail_product_image(image_id: int, db: Session = Depends(get_db)):
    image = db.query(ProductImage).filter(ProductImage.id == image_id).first()
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мындай ID менен сүрөт табылган жок"
        )
    return image

@product_images_router.put('/{image_id}/', response_model=dict)
async def update_product_image(image_id: int, product_image: ProductImageInputSchema, db: Session = Depends(get_db)):
    image_db = db.query(ProductImage).filter(ProductImage.id == image_id).first()
    if not image_db:
        raise HTTPException(detail='Мындай сүрөт жок', status_code=400)

    product_exists = db.query(Product).filter(Product.id == product_image.product_id).first()
    if not product_exists:
        raise HTTPException(
            status_code=400,
            detail=f"Ката: ID = {product_image.product_id} болгон продукт базада жок!"
        )

    for img_key, img_value in product_image.model_dump().items():
        setattr(image_db, img_key, img_value)

    db.commit()
    db.refresh(image_db)
    return {'message': 'Продукттун сүрөтү өзгөрүлдү'}


@product_images_router.delete('/{image_id}/', response_model=dict)
async def delete_product_image(image_id: int, db: Session = Depends(get_db)):
    image_db = db.query(ProductImage).filter(ProductImage.id == image_id).first()
    if not image_db:
        raise HTTPException(detail='Мындай сүрөт жок', status_code=400)

    db.delete(image_db)
    db.commit()
    return {'message': 'Продукттун сүрөтү удалить болду'}