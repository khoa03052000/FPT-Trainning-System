# Generated by Django 3.1.5 on 2021-01-21 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FPT', '0013_auto_20210121_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='category',
            field=models.ManyToManyField(blank=True, null=True, to='FPT.Category'),
        ),
    ]
