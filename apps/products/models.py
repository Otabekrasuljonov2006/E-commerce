from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 100)
    def __str__(self):
        return self.name
class Product(models.Model):
    nomi=models.CharField(max_length = 200)
    tavsifi = models.TextField()
    narxi = models.DecimalField(max_digits = 15, decimal_places = 2)
    rasmi = models.ImageField(upload_to = 'products/')
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = 'mahsulotlar')
    omborda_bor = models.PositiveIntegerField(default = 0)
    qoshgan_sana = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return self.nomi