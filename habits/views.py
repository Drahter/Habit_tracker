from habits.models import Habit
from habits.paginators import CustomPagination
from rest_framework import generics

from habits.serializers import HabitSerializer


class HabitListAPIView(generics.ListAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = CustomPagination


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    # permission_classes = (IsAuthenticated, IsOwner)


class HabitCreateAPIView(generics.CreateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    # permission_classes = (IsAuthenticated)

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.created_by = self.request.user
        habit.save()


class HabitUpdateAPIView(generics.UpdateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    # permission_classes = (IsAuthenticated, IsOwner)


class HabitDestroyAPIView(generics.DestroyAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    # permission_classes = (IsAuthenticated, IsOwner)
