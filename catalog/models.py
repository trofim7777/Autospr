from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

class Brand(models.Model):
    name = models.CharField('Марка', max_length=100, unique=True)
    class Meta:
        verbose_name = 'Марка'
        verbose_name_plural = 'Марки'
        ordering = ['name']
    def __str__(self):
        return self.name

class CarModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='models', verbose_name='Марка')
    name = models.CharField('Модель', max_length=100)
    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'
        unique_together = ('brand', 'name')
        ordering = ['brand__name', 'name']
    def __str__(self):
        return f'{self.brand} {self.name}'

class Car(models.Model):
    ENGINE_CHOICES = [
        ('petrol', 'Бензин'),
        ('diesel', 'Дизель'),
        ('hybrid', 'Гибрид'),
        ('electric', 'Электро'),
    ]
    TRANSMISSION_CHOICES = [
        ('mt', 'Механика'),
        ('at', 'Автомат'),
        ('cvt', 'Вариатор'),
        ('dct', 'Робот (DCT)'),
    ]
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, verbose_name='Марка')
    model = models.ForeignKey(CarModel, on_delete=models.PROTECT, verbose_name='Модель')
    year = models.PositiveIntegerField('Год выпуска')
    engine_type = models.CharField('Двигатель', max_length=20, choices=ENGINE_CHOICES)
    transmission = models.CharField('Коробка', max_length=20, choices=TRANSMISSION_CHOICES)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    image = models.ImageField('Фото', upload_to='cars/', blank=True, null=True)
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
        ordering = ['-created_at']
    def __str__(self):
        return f'{self.brand} {self.model.name} ({self.year})'
    def clean(self):
        if self.model and self.brand and self.model.brand_id != self.brand_id:
            raise ValidationError('Выбранная модель не относится к выбранной марке.')

# ⬇️ Перенесён сюда, после Car
class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    car = models.ForeignKey(
        Car,  # теперь класс уже определён
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'car')
        ordering = ['-created_at']
    def __str__(self):
        return f'{self.user} → {self.car}'
