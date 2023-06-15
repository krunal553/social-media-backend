# Generated by Django 4.1.7 on 2023-06-14 03:05

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_userprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profilePic',
            field=models.ImageField(default='/default.jpg', upload_to=user.models.path_and_rename),
        ),
    ]
