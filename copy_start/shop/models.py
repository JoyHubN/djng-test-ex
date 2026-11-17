from django.db import models
from users.models import CustomUser
from .validate import validate_file_size

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Категория')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    price = models.FloatField(default=0, verbose_name='Цена')
    count = models.IntegerField(default=0, verbose_name='Количество в наличии')
    total_stock = models.IntegerField(default=0, verbose_name='Общий запас')
    
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name='Страна-производитель')
    year = models.IntegerField(blank=True, null=True, verbose_name='Год выпуска')
    model_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Модель')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Изображение')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.total_stock = self.count
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

class KorzinaItem(models.Model):
    us = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='items', db_column='us_id', verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return f'{self.us.username} - {self.product.name} ({self.quantity} шт.)'

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('confirmed', 'Подтвержденный'),
        ('canceled', 'Отмененный'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders', verbose_name='Заказчик')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Таймстамп заказа')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    cancel_reason = models.TextField(blank=True, null=True, verbose_name='Причина отказа')

    def __str__(self):
        return f'Заказ #{self.id} от {self.user.username} ({self.get_status_display()})'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    product_name = models.CharField(max_length=255, verbose_name='Наименование товара на момент заказа')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    price = models.FloatField(verbose_name='Цена за единицу')

    def __str__(self):
        return f'{self.product_name} x {self.quantity}'

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'


class Document(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название документа')
    file = models.FileField(
        upload_to='documents/',
        validators=[validate_file_size],
        verbose_name='Файл'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

