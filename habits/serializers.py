from rest_framework import serializers

from habits.models import Habit
from habits.validators import (
    PleasantHabitValidator,
    ConnectedAndRewardValidator,
    PleasantHabitNoRewardValidator
)


class HabitSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Habit, привязаны валидаторы"""
    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            PleasantHabitValidator(),
            ConnectedAndRewardValidator(),
            PleasantHabitNoRewardValidator()
        ]
