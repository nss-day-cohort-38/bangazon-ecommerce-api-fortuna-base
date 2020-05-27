from django.db import models


class Product_Type(models.Model):

    name = models.CharField(max_length=55)


    class Meta:
        verbose_name = "product type"
        verbose_name_plural = "product types"
        ordering = ["name",]

    def __str__(self):
        return self.name
        
        