# Generated by Django 5.1.3 on 2024-12-09 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0015_comment_book_discussion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookdiscussion',
            name='goodreads_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='bookrecommendation',
            name='goodreads_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
