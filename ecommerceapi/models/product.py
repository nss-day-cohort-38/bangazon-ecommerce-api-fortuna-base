from django.db import models
from .customer import Customer
from .product_type import Product_Type

class Product(models.Model):

    title = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField(null=True)
    location = models.CharField(max_length=75)
    image_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    product_type = models.ForeignKey(Product_Type, related_name="products", on_delete=models.CASCADE)
    orders = models.ManyToManyField('Order', through='Order_Product',)

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"
        

    def __str__(self):
        return self.title