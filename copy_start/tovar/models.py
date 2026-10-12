from django.db import models
from users.models import CustomUser

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(default=0)
    count = models.IntegerField(default=0, null=False, blank=False)
    total_stock = models.IntegerField(default=0, null=False, blank=False)

    def save(self):
        if not self.pk:
            self.total_stock = self.count
        super().save()

    def __str__(self):
        return self.name

class KorzinaItem(models.Model):
    us = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='items', db_column='us_id', verbose_name='Имя пользователя (ФИО / логин)')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return f"{self.us.username} - {self.product.name} ({self.quantity} шт.)"

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'


