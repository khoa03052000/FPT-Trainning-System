# Generated by Django 3.1.5 on 2021-01-26 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FPT', '0021_auto_20210126_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainee',
            name='dot',
            field=models.DateField(blank=True, default='YYYY-MM-DD'),
        ),
    ]