from shop_app.database.models import UserProfile, Category, Product, SubCategory, RefreshToken, ProductImage, Review
from sqladmin import ModelView


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.first_name, UserProfile.last_name]


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.category_name]

class ProductAdmin(ModelView, model=Product):
    column_list = [Product.product_name, Product.product_images]

class SubCategoryAdmin(ModelView, model=SubCategory):
    column_list = [SubCategory.subcategory_name]
