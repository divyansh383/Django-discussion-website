# Generated by Django 4.0.1 on 2022-08-05 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_alter_room_host'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='pp',
            field=models.ImageField(default='default.jpg', upload_to='propics'),
        ),
    ]