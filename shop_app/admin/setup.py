from .views import UserProfileAdmin, CategoryAdmin, ProductAdmin
from fastapi import FastAPI
from sqladmin import Admin
from shop_app.database.db import engine


def  setup_admin(shop_app: FastAPI):
    admin = Admin(shop_app, engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(ProductAdmin)
