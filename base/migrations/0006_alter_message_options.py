# Generated by Django 4.0.1 on 2022-08-01 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_message_options_alter_room_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-updated', '-created']},
        ),
    ]