# Generated by Django 3.1.5 on 2021-01-25 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FPT', '0016_auto_20210125_0227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
