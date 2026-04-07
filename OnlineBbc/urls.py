from django.urls import path
# Yangi view-larni import qismiga qo'shishni unutmang
from .views import (
    BaseView, 
    ProductDetailView, 
    CategoryDetailView, 
    SubCategoryDetailView, 
    AddToCardView, 
    CartView,             # Qo'shildi
    ChangeQuantityView,    # Qo'shildi
    DeleteFromCartView,     # Qo'shildi
    CheckoutView
)

urlpatterns = [
    path("", BaseView.as_view(), name="base"), 
    path("product/<slug:slug>/", ProductDetailView.as_view(), name="product_detail"), 
    path("category/<slug:slug>/", CategoryDetailView.as_view(), name="category_detail"),
    path("subcategory/<slug:slug>/", SubCategoryDetailView.as_view(), name="subcategory_detail"), 
    
    # --- SAVATCHA UCHUN YO'LLAR ---
    
    # Savatga qo'shish
    path("add-to-card/", AddToCardView.as_view(), name="add-to-card"),
    
    # Savatcha sahifasini ko'rish (jadval ko'rinishi)
    path("cart/", CartView.as_view(), name="cart_view"),
    
    # Miqdorni o'zgartirish (+/- tugmalari uchun)
    # <int:item_id> - qaysi maxsulot, <str:action> - plus yoki minus ekanligini bildiradi
    path("change-quantity/<int:item_id>/<str:action>/", ChangeQuantityView.as_view(), name="change_quantity"),
    
    # Savatdan o'chirish (Delete tugmasi uchun)
    path("delete-item/<int:item_id>/", DeleteFromCartView.as_view(), name="delete_item"),

    path("checkout/", CheckoutView.as_view(), name="checkout"),
]