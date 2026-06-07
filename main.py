from fastapi import FastAPI
from shop_app.api import users
from shop_app.api import category
from shop_app.api import  subcategory
from shop_app.api import  product
from shop_app.api import  product_img
from shop_app.api import  review
from shop_app.api import auth
import uvicorn
from shop_app.admin.setup import setup_admin

shop_app = FastAPI()

shop_app.include_router(users.users_router)
shop_app.include_router(category.categories_router)
shop_app.include_router(subcategory.subcategories_router)
shop_app.include_router(product.products_router)
shop_app.include_router(product_img.product_images_router)
shop_app.include_router(review.reviews_router)
shop_app.include_router(auth.auth_router)
setup_admin(shop_app)

if __name__ == '__main__':
    uvicorn.run(shop_app, host='127.0.0.1', port=8000) # Финальный запуск магазина