# Generated by Django 3.1.5 on 2021-01-28 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FPT', '0027_auto_20210128_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='department',
            field=models.CharField(blank=True, default='FPT', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='full_name',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
