from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from users.models import User


class Habit(models.Model):
    """Модель для хранения информации о привычках"""
    PERIOD = (
        ('1', 1),
        ('2', 2),
        ('3', 3),
        ('4', 4),
        ('5', 5),
        ('6', 6),
        ('7', 7),
    )

    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Автор привычки')
    place = models.CharField(max_length=100, default='любое место',
                             blank=True, null=True, verbose_name='Место выполнения')
    date = models.DateField(blank=True, null=True, verbose_name='Дата выполнения привычки')
    time = models.TimeField(max_length=30, blank=True, null=True, verbose_name='Время выполнения привычки')
    action = models.CharField(max_length=100, verbose_name='Действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='Приятная привычка')
    connected = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    period = models.CharField(max_length=20, choices=PERIOD, default='ONE',
                              blank=True, null=True, verbose_name='периодичность')
    reward = models.CharField(max_length=100, blank=True, null=True, verbose_name='Награда')
    time_required = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(120)],
        blank=True, null=True,
        verbose_name='Необходимое время выполнения, сек.'
    )
    is_public = models.BooleanField(default=False, blank=True, null=True, verbose_name='Публичность')

    def __str__(self):
        return f'{self.created_by} - {self.action}'


    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['-date']
