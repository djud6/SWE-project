# Generated by Django 5.1.3 on 2024-12-08 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0007_club_club_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='club_image',
            field=models.ImageField(blank=True, null=True, upload_to='static/club'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='static/profile'),
        ),
    ]
