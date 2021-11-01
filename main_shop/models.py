from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Product(models.Model):
    product_name = models.CharField(max_length=200, blank=False,null=False)
    product_desc = models.TextField(blank= False, null=False)
    product_img = models.ImageField(blank=True, null=True, upload_to= 'product_images')
    quantity = models.IntegerField(default=10, validators=[MinValueValidator(0), MaxValueValidator(100)])
    price = models.DecimalField(max_digits=7, decimal_places=2, default=50)
    is_available = models.BooleanField()
    is_active = models.BooleanField()

    def __str__(self):
        return self.product_name

class Order(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    post_code = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    braintree_id = models.CharField(max_length=150,blank=True)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())



class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return self.product.product_name

    def get_cost(self):
        return self.quantity*self.price

