from pydantic import BaseModel, EmailStr
from typing import Optional
from .models import StatusChoices
from datetime import date, datetime


class UserProfileOutSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    age: Optional[str]
    phone_number: Optional[str]
    avatar: Optional[str]
    status: StatusChoices
    password: str
    date_registered: date

class UserProfileInputSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    age: Optional[str]
    phone_number: Optional[str]
    avatar: Optional[str]
    password: str

class UserLoginSchema(BaseModel):
    username: str
    password: str
# ========================================================
class CategoryOutSchema(BaseModel):
    id: int
    category_image: str
    category_name: str

class CategoryInputSchema(BaseModel):
    category_image: str
    category_name: str
# ========================================================
class SubCategoryOutSchema(BaseModel):
    id: int
    subcategory_name: str
    category_id: int

class SubCategoryInputSchema(BaseModel):
    subcategory_name: str
# ========================================================
class ProductOutSchema(BaseModel):
    id: int
    subcategory_id: int
    product_name: str
    price: int
    article_number: int
    description: str
    product_type: bool
    video: str
    created_date: date

class ProductInputSchema(BaseModel):
    product_name: str
    price: int
    article_number: int
    description: str
    product_type: bool
    video: str

# ========================================================
class ProductImageOutSchema(BaseModel):
    id: int
    image: str
    product_id: int

class ProductImageInputSchema(BaseModel):
    image: str
# ========================================================
class ReviewOutSchema(BaseModel):
    id: int
    user_id: int
    product_id: int
    stars: int
    comment: str
    created_date: datetime

class ReviewInputSchema(BaseModel):
    user_id: int
    product_id: int
    stars: int
    comment: str
# ========================================================