from rest_framework import serializers

from habits.models import Habit


class PleasantHabitValidator:
    """Проверка прокрепляемой заявки на наличие маркера приятной"""
    def __call__(self, value):
        connected_id = value.get('connected')
        if connected_id:
            connected_habit = Habit.objects.get(id=connected_id)
            if connected_habit and not connected_habit.is_pleasant:
                raise serializers.ValidationError(
                    'Связанная привычка должна быть приятной.'
                )


class ConnectedAndRewardValidator:
    """Проверка, исключающая заполнения награды и связанной привычки"""
    def __call__(self, value):
        if value.get('reward') and value.get('connected'):
            raise serializers.ValidationError(
                'Может быть заявлена либо связанная '
                'привычка, либо вознаграждение.'
            )


class PleasantHabitNoRewardValidator:
    """Проверка, исключающая назначение награды или связанной привычки у приятной"""
    def __call__(self, value):
        if (value.get('is_pleasant')
                and (value.get('reward') or value.get('connected'))):
            raise serializers.ValidationError(
                'У приятной привычки не может быть'
                ' вознаграждения или связанной привычки.'
            )
