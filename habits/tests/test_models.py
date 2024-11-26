from django.test import TestCase

from django.utils import timezone
from habits.models import Habit
from users.models import User


class HabitModelTest(TestCase):
    """Тесты для модели Habit"""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@test.ru', password='testpass')

        Habit.objects.create(
            created_by=self.user,
            place='Home',
            time_required=30,
            time=timezone.now().time(),
            action='Do something',
            is_pleasant=False
        )

    def test_create_habit(self):
        habit = Habit.objects.get(id=1)
        self.assertEqual(habit.action, 'Do something')
        self.assertEqual(habit.created_by, self.user)
        self.assertFalse(habit.is_pleasant)


