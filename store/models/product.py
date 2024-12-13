from django.db import models
from .category import Category
from django.core.validators import MinValueValidator

class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name="Product Name")
    price = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Product Price")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Product Category")
    description = models.CharField(max_length=200, null=True, blank=True, verbose_name="Product Description")
    image = models.ImageField(upload_to='upload/product/', verbose_name="Product Image")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['name']

    def __str__(self):
        return self.name
    

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)
    
    @staticmethod
    def get_all_products():
        return Product.objects.all()
    
    @staticmethod
    def get_all_products_by_category_id(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        return Product.get_all_products()
