from rest_framework.permissions import AllowAny

from habits.models import Habit
from habits.paginators import CustomPagination
from rest_framework import generics

from habits.serializers import HabitSerializer
from users.permissions import IsOwner


class HabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
#     pagination_class = CustomPagination

    def get_queryset(self):
        return Habit.objects.filter(created_by=self.request.user)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner]


class HabitCreateAPIView(generics.CreateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.created_by = self.request.user
        habit.save()


class HabitUpdateAPIView(generics.UpdateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner]


class HabitDestroyAPIView(generics.DestroyAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner]


class PublicHabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    permission_classes = (AllowAny,)
#     pagination_class = CustomPagination

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)
