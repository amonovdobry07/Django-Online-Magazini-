from django.db import models
from django.urls import reverse

class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to="product_images/")
    image1 = models.ImageField(upload_to="product_images/", null=True, blank=True)
    image2 = models.ImageField(upload_to="product_images/", null=True, blank=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, related_name='categories')
    subcategory = models.ForeignKey("SubCategory", on_delete=models.CASCADE, null=True, related_name='subcategories')
    discount = models.DecimalField(max_digits=4,  decimal_places=2, default=0, null=True)

    def get_absolute_url(self): 
        return reverse("product_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name
    
class Category(models.Model): 
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def get_absolute_url(self): 
        return reverse("category_detail", kwargs={"slug": self.slug})


    def __str__(self):
        return self.name

class SubCategory(models.Model): 
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategory")

    def get_absolute_url(self): 
        return reverse("subcategory_detail", kwargs={'slug': self.slug})

    def __str__(self):
        return self.name
    


class Order(models.Model): 
    STATUS_NEW = "new"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_READY = "is_ready"
    STATUS_COMPLATED = "complated"

    BUYING_TYPE_SELF = "self"
    BUYING_TYPE_DELIVERY = "delivery"

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS,  'Заказ в обработке'),
        (STATUS_READY,  'Заказ готов'), 
        (STATUS_COMPLATED,  'Заказ выполнен')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'), 
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )





    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_data = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)

    buying_type = models.CharField(max_length=20, choices=BUYING_TYPE_CHOICES, default=BUYING_TYPE_SELF)

    def __str__(self):
        return f"Order of {self.quantity} {self.product.name} (s) on {self.order_data}"
    
class Customer(models.Model): 
    name = models.CharField(max_length=100)
    email = models.EmailField()
    adress = models.TextField()
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class Cart(models.Model): 
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="CartItem")

    def get_total_price(self):
        # Barcha CartItem'lar summasini yig'ib beradi
        return sum(item.total_price for item in self.cartitem_set.all())

    def __str__(self):
        return f"Cart of {self.customer.name}"
    

    
class CartItem(models.Model): 
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1) # Default 1 bo'lgani yaxshi
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Saqlashdan oldin avtomatik hisoblaydi
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"