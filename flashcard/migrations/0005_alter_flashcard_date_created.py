# Generated by Django 4.2.5 on 2023-09-18 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcard', '0004_flashcard_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flashcard',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
