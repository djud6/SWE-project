# Generated by Django 5.1.3 on 2024-12-09 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0010_bookrecommendation_delete_book'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookrecommendation',
            name='club',
        ),
        migrations.AddField(
            model_name='club',
            name='recommendation',
            field=models.ManyToManyField(blank=True, related_name='club_theme', to='discussion.bookrecommendation'),
        ),
    ]
