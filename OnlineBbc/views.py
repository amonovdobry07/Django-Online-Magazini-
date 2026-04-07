from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Product, Category, Order, Customer, Cart, CartItem, SubCategory

from django.contrib import messages



# Mavjud kodlaringiz (o'zgartirilmagan)
class BaseView(View): 
    def get(self, request, *args, **kwargs): 
        products = Product.objects.all()
        categories = Category.objects.all()
        return render(request, "base.html", {"products": products, "categories": categories})

class ProductDetailView(View): 
    def get(self, request, slug, *args, **kwargs): 
        product = Product.objects.get(slug = slug )
        categories = Category.objects.all()
        return render(request, "product_detail.html", {"product" : product, "categories": categories })

class CategoryDetailView(View): 
    def get(self, request, slug, *args, **kwargs): 
        category = Category.objects.get(slug = slug )
        products = Product.objects.filter(category = category)
        categories = Category.objects.all()
        subcategories = SubCategory.objects.filter(category=category)
        return render(request, "category_detail.html", {"category" : category, "products" :
                                                        products, "categories": categories, 
                                                        'subcategories' : subcategories })

class SubCategoryDetailView(View): 
    def get(self, request, slug, *args, **kwargs): 
        subcategory = SubCategory.objects.get(slug = slug)
        products = Product.objects.filter(category = subcategory.category)
        categories = Category.objects.all()
        subcategories = SubCategory.objects.filter(category = subcategory.category)
        return render(request, 'subcategory_detail.html', {'subcategory': subcategory, 'products': products, "categories": categories, 'subcategories' : subcategories })

# --- SAVATCHA UCHUN YANGI QISMLAR ---

# Yordamchi funksiya: Savatchani olish yoki yaratish
def get_cart_for_user(request):
    # Hozircha login tizimi bo'lmagani uchun doimiy bitta mijozdan foydalanamiz
    # Agar foydalanuvchi tizimga kirgan bo'lsa request.user orqali filtrlash mumkin
    customer, _ = Customer.objects.get_or_create(
        name="Guest User", 
        defaults={'email': 'guest@example.com', 'phone_number': '000'}
    )
    cart, _ = Cart.objects.get_or_create(customer=customer)
    return cart

class CartView(View):
    """Savatcha sahifasini ko'rsatish (Jadval ko'rinishida)"""
    def get(self, request):
        cart = get_cart_for_user(request)
        cart_items = CartItem.objects.filter(cart=cart).order_by('id')
        categories = Category.objects.all()
        
        # Umumiy summani hisoblash
        total_sum = sum(item.total_price for item in cart_items)
        
        return render(request, "card.html", {
            "cart_items": cart_items, 
            "categories": categories,
            "total_sum": total_sum
        })

class AddToCardView(View):
    """Maxsulotni savatga qo'shish"""
    def post(self, request, *args, **kwargs): 
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, id=product_id)
        cart = get_cart_for_user(request)

        # Savatda ushbu maxsulot bormi?
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 1, 'total_price': product.price}
        )

        if not created:
            cart_item.quantity += 1
            cart_item.total_price = cart_item.quantity * product.price
            cart_item.save()

        return redirect('cart_view')

class ChangeQuantityView(View):
    """Miqdorni oshirish yoki kamaytirish (+ / -)"""
    def post(self, request, item_id, action):
        cart_item = get_object_or_404(CartItem, id=item_id)
        
        if action == 'plus':
            cart_item.quantity += 1
        elif action == 'minus' and cart_item.quantity > 1:
            cart_item.quantity -= 1
            
        cart_item.total_price = cart_item.quantity * cart_item.product.price
        cart_item.save()
        return redirect('cart_view')

class DeleteFromCartView(View):
    """Maxsulotni savatdan butunlay o'chirish"""
    def post(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.delete()
        return redirect('cart_view')
    

class CheckoutView(View):
    def post(self, request, *args, **kwargs):
        cart = get_cart_for_user(request)
        cart_items = CartItem.objects.filter(cart=cart)
        categories = Category.objects.all()
        
        if not cart_items.exists():
            messages.error(request, "Savatchangiz bo'sh!")
            return redirect('cart_view')

        # Har bir savatdagi elementni buyurtmaga aylantiramiz
        for item in cart_items:
            Order.objects.create(
                product=item.product,
                quantity=item.quantity,
                total_price=item.total_price,
                status=Order.STATUS_NEW,
                buying_type=Order.BUYING_TYPE_DELIVERY # Standart yetkazib berish
            )

        # Buyurtma berilgandan keyin savatchani bo'shatamiz
        cart_items.delete()

        messages.success(request, "Buyurtmangiz muvaffaqiyatli qabul qilindi!")
        return render(request, "success_order.html",)