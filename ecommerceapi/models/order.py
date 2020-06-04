from django.db import models
from .customer import Customer
from .payment_type import Payment_Type
from django.db.models import F



class Order(models.Model):

    customer= models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    payment_type = models.ForeignKey(Payment_Type, blank=True, null=True, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField()
    products = models.ManyToManyField("Product", through='Order_Product',)

    class Meta:
        verbose_name = "order"
        verbose_name_plural = "orders"
        ordering = (F('created_at').asc(nulls_first = True))

    def __str__(self):
        return self.created_at