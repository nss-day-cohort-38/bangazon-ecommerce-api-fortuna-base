from django.db import models
from .customer import Customer


class Payment_Type(models.Model):

    merchant_name = models.CharField(max_length=25)
    account_number = models.CharField(max_length=25)
    expiration_date = models.DateTimeField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField()


    class Meta:
        verbose_name = "payment type"
        verbose_name_plural = "payment types"


    def __str__(self):
        return self.merchant_name    