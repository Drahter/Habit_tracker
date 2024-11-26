from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class BlogArticleAdmin(admin.ModelAdmin):
    list_display = (
        'created_by',
        'place',
        'date',
        'time',
        'action',
        'is_pleasant',
        'period',
        'is_public',
        'reward',
    )
    search_fields = ('created_by', 'place',)
