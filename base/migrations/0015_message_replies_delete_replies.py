# Generated by Django 4.0.1 on 2022-08-24 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_alter_replies_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='replies',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.DeleteModel(
            name='Replies',
        ),
    ]