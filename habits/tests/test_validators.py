from django.test import TestCase
from django.utils import timezone

from habits.validators import (PleasantHabitValidator,
                               ConnectedAndRewardValidator,
                               PleasantHabitNoRewardValidator)
from habits.models import Habit
from users.models import User


class ConnectedAndRewardValidatorTest(TestCase):

    def setUp(self):
        self.validator = ConnectedAndRewardValidator()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.ru',
            password='testpass'
        )

    def test_both_reward_and_connected(self):
        data = {
            'reward': 'TestReward',
            'connected': 1
        }
        with self.assertRaisesMessage(
                Exception,
                'Может быть заявлена либо '
                'связанная привычка, либо вознаграждение.'
        ):
            self.validator(data)

    def test_only_reward(self):
        data = {
            'reward': 'TestReward',
            'connected': None
        }
        try:
            self.validator(data)
        except Exception as e:
            self.fail(f'Validator raised exception unexpectedly: {e}')

    def test_only_connected(self):
        data = {
            'reward': None,
            'connected': 1
        }
        try:
            self.validator(data)
        except Exception as e:
            self.fail(f'Validator raised exception unexpectedly: {e}')


class PleasantHabitValidatorTest(TestCase):
    def setUp(self):
        self.validator = PleasantHabitValidator()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.ru',
            password='testpass'
        )

        self.pleasant_habit = Habit.objects.create(
            created_by=self.user,
            place='Home',
            time_required=30,
            action='Do something',
            is_pleasant=True
        )

        self.habit = Habit.objects.create(
            created_by=self.user,
            place='Home',
            time_required=30,
            time=timezone.now().time(),
            action='Do something',
            is_pleasant=False,
        )

    def test_connected_is_pleasant(self):
        data = {
            'connected': self.pleasant_habit.id,
            'action': 'New Habit',
            'place': 'New Place',
            'time_required': 15,
            'time': '08:00:00',
            'is_pleasant': False
        }

        try:
            self.validator(data)
        except Exception as e:
            self.fail(f'Validator raised exception unexpectedly: {e}')

    def test_connected_not_pleasant(self):
        data = {
            'connected': self.habit.id,
            'action': 'New Habit',
            'place': 'New Place',
            'time_required': 15,
            'time': '08:00:00',
            'is_pleasant': False
        }

        with self.assertRaisesMessage(
                Exception,
                'Связанная привычка должна быть приятной.'
        ):
            self.validator(data)


class PleasantHabitNoRewardValidatorTest(TestCase):
    def setUp(self):
        self.validator = PleasantHabitNoRewardValidator()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.ru',
            password='testpass'
        )

    def test_pleasant_and_connected(self):
        data = {
            'is_pleasant': True,
            'connected': 1
        }
        with self.assertRaisesMessage(
                Exception,
                'У приятной привычки не может быть '
                'вознаграждения или связанной привычки.'
        ):
            self.validator(data)

    def test_pleasant_and_reward(self):
        data = {
            'is_pleasant': True,
            'reward': 'test reward'
        }
        with self.assertRaisesMessage(
                Exception,
                'У приятной привычки не может быть '
                'вознаграждения или связанной привычки.'
        ):
            self.validator(data)
