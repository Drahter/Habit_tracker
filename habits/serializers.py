from rest_framework import serializers

from habits.models import Habit
from habits.validators import (
    PleasantHabitValidator,
    ConnectedAndRewardValidator,
    PleasantHabitNoRewardValidator
)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            PleasantHabitValidator(),
            ConnectedAndRewardValidator(),
            PleasantHabitNoRewardValidator()
        ]
