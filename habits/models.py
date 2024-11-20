from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.core.exceptions import ValidationError

from users.models import User


class Habit(models.Model):
    """Модель для хранения информации о привычках"""
    PERIOD = (
        ('ONE', 'один'),
        ('TWO', 'два'),
        ('THREE', 'три'),
        ('FOUR', 'четыре'),
        ('FIVE', 'пять'),
        ('SIX', 'шесть'),
        ('SEVEN', 'семь'),
    )

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор привычки')
    place = models.CharField(max_length=100, default='любое место', verbose_name='Место выполнения')
    date = models.DateField(verbose_name='Время выполнения')
    action = models.CharField(max_length=100, verbose_name='Действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='Приятная привычка')
    connected = models.ManyToManyField('self', symmetrical=False, blank=True, null=True)
    period = models.CharField(max_length=20, choices=PERIOD, default='ONE', verbose_name='периодичность')
    reward = models.CharField(max_length=100, blank=True, null=True, verbose_name='Награда')
    time_required = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(120)],
        verbose_name='Необходимое время выполнения, сек.'
    )
    is_public = models.BooleanField(default=False, verbose_name='Публичность')

    def __str__(self):
        return f'{self.created_by} - {self.action}'

    def clean(self):
        super().clean()
        if self.is_pleasant and self.connected:
            raise ValidationError('Привычка может быть или приятной, или иметь связанную приятную.')
        if self.connected and self.reward:
            raise ValidationError('Привычка может иметь или связанную приятную, или награду!')

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['-date']
