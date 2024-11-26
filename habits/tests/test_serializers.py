from django.test import TestCase
from habits.serializers import HabitSerializer
from users.models import User


class HabitSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_valid_data(self):
        data = {
            'created_by': self.user.id,
            'place': 'Home',
            'time_required': 30,
            'time': '12:00:00',
            'action': 'Do something',
            'is_pleasant': False
        }
        serializer = HabitSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data(self):
        data = {
            'created_by': self.user.id,
            'place': 'Home',
            'time_required': 150,
            'time': '25:00:00',
            'action': 'Do something',
            'is_pleasant': False
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('time_required', serializer.errors)
        self.assertIn('time', serializer.errors)
