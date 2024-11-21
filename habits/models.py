from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from users.models import User


class Habit(models.Model):
    """Модель для хранения информации о привычках"""
    PERIOD = (
        ('ONE', 1),
        ('TWO', 2),
        ('THREE', 3),
        ('FOUR', 4),
        ('FIVE', 5),
        ('SIX', 6),
        ('SEVEN', 7),
    )

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор привычки')
    place = models.CharField(max_length=100, default='любое место',
                             blank=True, null=True, verbose_name='Место выполнения')
    date = models.DateField(verbose_name='Время выполнения', blank=True, null=True)
    action = models.CharField(max_length=100, verbose_name='Действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='Приятная привычка')
    connected = models.ManyToManyField('self', symmetrical=False, blank=True, null=True)
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

    def clean(self):
        super().clean()
        if self.is_pleasant and self.connected:
            raise ValidationError('Привычка может быть или приятной, или иметь связанную приятную.')
        if self.connected and self.reward:
            raise ValidationError('Привычка может иметь или связанную приятную, или награду!')
        if self.date < timezone.now().date():
            raise ValidationError('Дата не может быть раньше сегодняшнего дня.')

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['-date']
