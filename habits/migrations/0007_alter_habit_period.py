# Generated by Django 5.1.3 on 2024-11-24 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0006_remove_habit_connected_habit_connected'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='period',
            field=models.CharField(blank=True, choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7)], default='ONE', max_length=20, null=True, verbose_name='периодичность'),
        ),
    ]
