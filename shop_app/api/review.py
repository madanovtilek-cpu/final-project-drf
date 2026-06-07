from fastapi import APIRouter, Depends, HTTPException, status
from shop_app.database.models import Review, UserProfile, Product
from shop_app.database.schema import ReviewOutSchema, ReviewInputSchema
from shop_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

reviews_router = APIRouter(prefix='/reviews', tags=['Review'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@reviews_router.post('/', response_model=ReviewOutSchema, status_code=status.HTTP_201_CREATED)
async def create_review(review: ReviewInputSchema, db: Session = Depends(get_db)):
    user_exists = db.query(UserProfile).filter(UserProfile.id == review.user_id).first()
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ката: ID = {review.user_id} болгон колдонуучу базада жок!"
        )

    product_exists = db.query(Product).filter(Product.id == review.product_id).first()
    if not product_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ката: ID = {review.product_id} болгон продукт базада жок!"
        )

    if review.stars < 1 or review.stars > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Баалоо (stars) 1ден 5ке чейинки сан болушу шарт!"
        )

    review_db = Review(**review.model_dump())
    db.add(review_db)
    db.commit()
    db.refresh(review_db)
    return review_db


@reviews_router.get('/', response_model=List[ReviewOutSchema])
async def list_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()


@reviews_router.get('/{review_id}/', response_model=ReviewOutSchema)
async def detail_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мындай ID менен пикир табылган жок"
        )
    return review


@reviews_router.put('/{review_id}/', response_model=dict)
async def update_review(review_id: int, review: ReviewInputSchema, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if not review_db:
        raise HTTPException(detail='Мындай пикир жок', status_code=400)

    user_exists = db.query(UserProfile).filter(UserProfile.id == review.user_id).first()
    if not user_exists:
        raise HTTPException(
            status_code=400,
            detail=f"Ката: ID = {review.user_id} болгон колдонуучу базада жок!"
        )

    product_exists = db.query(Product).filter(Product.id == review.product_id).first()
    if not product_exists:
        raise HTTPException(
            status_code=400,
            detail=f"Ката: ID = {review.product_id} болгон продукт базада жок!"
        )

    if review.stars < 1 or review.stars > 5:
        raise HTTPException(
            status_code=400,
            detail="Баалоо (stars) 1ден 5ке чейинки сан болушу шарт!"
        )

    for rev_key, rev_value in review.model_dump().items():
        setattr(review_db, rev_key, rev_value)

    db.commit()
    db.refresh(review_db)
    return {'message': 'Пикир өзгөрүлдү'}


@reviews_router.delete('/{review_id}/', response_model=dict)
async def delete_review(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if not review_db:
        raise HTTPException(detail='Мындай пикир жок', status_code=400)

    db.delete(review_db)
    db.commit()
    return {'message': 'Пикир удалить болду'}