from shop_app.database.db import Base
from sqlalchemy import Integer, String, Enum, Date, ForeignKey, Text, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from enum import Enum as PyEnum
from datetime import date, datetime


class StatusChoices(str, PyEnum):
    gold = 'gold'
    silver = 'silver'
    bronze = 'bronze'
    simple = 'simple'


class UserProfile(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    username: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    avatar: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[StatusChoices] = mapped_column(Enum(StatusChoices), default=StatusChoices.simple)
    password: Mapped[str] = mapped_column(String, nullable=False)
    date_register: Mapped[date] = mapped_column(Date, default=date.today)

    user_review: Mapped[List['Review']] = relationship(back_populates='user', cascade='all, delete-orphan')
    user_token: Mapped[List["RefreshToken"]] = relationship(back_populates='token_user',
                                                            cascade='all, delete-orphan')

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    token: Mapped[str] = mapped_column(String)  # ← ушул жок болчу, кош
    token_user: Mapped[UserProfile] = relationship(UserProfile, back_populates='user_token')


class Category(Base):
    __tablename__ = 'category'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_image: Mapped[str] = mapped_column(String)
    category_name: Mapped[str] = mapped_column(String(30), unique=True)
    subcategories: Mapped[List['SubCategory']] = relationship('SubCategory', back_populates='category',
                                                              cascade='all, delete-orphan')
    def __repr__(self):
        return f'{self.category_name }'

class SubCategory(Base):
    __tablename__ = 'subcategory'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subcategory_name: Mapped[str] = mapped_column(String(30))
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    category: Mapped[Category] = relationship('Category', back_populates='subcategories')
    product_sub: Mapped[List['Product']] = relationship(back_populates='subcategory', cascade='all, delete-orphan')


class Product(Base):
    __tablename__ = 'product'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subcategory_id: Mapped[int] = mapped_column(ForeignKey('subcategory.id'))
    subcategory: Mapped[SubCategory] = relationship(SubCategory, back_populates='product_sub')
    product_name: Mapped[str] = mapped_column(String(30))
    price: Mapped[int] = mapped_column(Integer)
    article_number: Mapped[int] = mapped_column(Integer, unique=True)
    description: Mapped[str] = mapped_column(Text)
    product_type: Mapped[bool] = mapped_column(Boolean)
    video: Mapped[str] = mapped_column(String)
    created_date: Mapped[date] = mapped_column(Date, default=date.today)
    product_images: Mapped[List['ProductImage']] = relationship(back_populates='product', cascade='all, delete-orphan')

    product_reviews: Mapped[List['Review']] = relationship(back_populates='products', cascade='all, delete-orphan')


class ProductImage(Base):
    __tablename__ = 'product_image'


    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    image: Mapped[str] = mapped_column(String)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    product: Mapped[Product] = relationship(Product, back_populates='product_images')


class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped[UserProfile] = relationship(UserProfile, back_populates='user_review')

    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    products: Mapped[Product] = relationship(Product, back_populates='product_reviews')

    stars: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str] = mapped_column(Text)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)