# Generated by Django 3.1.5 on 2021-01-29 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FPT', '0030_auto_20210129_0457'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='content',
            field=models.TextField(blank=True, default=''),
        ),
    ]
