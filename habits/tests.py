from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

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


class HabitsListTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@test.ru',
            password='testpass'
        )
        self.client.force_authenticate(user=self.user)

        # Создание тестовых привычек
        self.habit1 = Habit.objects.create(
            place='Place1',
            time_required=30,
            time=timezone.now().time(),
            action='TestAction1',
            is_pleasant=False
        )
        self.habit2 = Habit.objects.create(
            place='Place2',
            time_required=30,
            time=timezone.now().time(),
            action='TestAction2',
            is_pleasant=False
        )

    def test_get_habits_list(self):
        url = reverse('habits:habit-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['action'], self.habit1.action)
        self.assertEqual(response.data[1]['action'], self.habit2.action)


class HabitsCreateTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@test.ru',
            password='testpass'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        url = reverse('habits:habit-create')
        data = {
            'action': 'TestAction1',
            'place': 'Place1',
            'time_required': 60,
            'time': '12:00:00',
            'is_pleasant': False
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.get().action, 'TestAction1')
        self.assertEqual(Habit.objects.get().created_by, self.user)


class HabitsUpdateTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@test.ru',
            password='testpass'
        )
        self.client.force_authenticate(user=self.user)

        # Создание тестовых привычек
        self.habit1 = Habit.objects.create(
            place='Place1',
            time_required=30,
            time=timezone.now().time(),
            action='TestAction1',
            is_pleasant=False
        )

    def test_update_habit(self):
        url = reverse('habits:habit-update', kwargs={'pk': self.habit1.id})
        data = {
            'action': 'TestAction1Updated',
            'place': 'Place1Updated',
            'time_required': 60,
            'time': '12:00:00',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.get(id=self.habit1.id).action, 'TestAction1Updated')
        self.assertEqual(Habit.objects.get(id=self.habit1.id).place, 'Place1Updated')


class HabitsDeleteTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@test.ru',
            password='testpass'
        )
        self.client.force_authenticate(user=self.user)

        # Создание тестовых привычек
        self.habit1 = Habit.objects.create(
            place='Place1',
            time_required=30,
            time=timezone.now().time(),
            action='TestAction1',
            is_pleasant=False
        )

    def test_delete_habit(self):
        url = reverse('habits:habit-delete', kwargs={'pk': self.habit1.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)
        self.assertEqual(Habit.objects.filter(id=self.habit1.id).exists(), False)


class PublicHabitsListTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@test.ru',
            password='testpass'
        )
        self.client.force_authenticate(user=self.user)

        # Создание тестовых привычек
        self.habit1 = Habit.objects.create(
            place='Place1',
            time_required=30,
            time=timezone.now().time(),
            action='TestAction1',
            is_pleasant=False,
            is_public=True
        )
        self.habit2 = Habit.objects.create(
            place='Place2',
            time_required=30,
            time=timezone.now().time(),
            action='TestAction2',
            is_pleasant=False,
            is_public=True
        )
        self.habit3 = Habit.objects.create(
            place='Place3',
            time_required=30,
            time=timezone.now().time(),
            action='TestAction3',
            is_pleasant=False,
            is_public=False
        )

    def test_get_public_habits_list(self):
        url = reverse('habits:public-habit-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['action'], self.habit1.action)
        self.assertEqual(response.data[1]['action'], self.habit2.action)
