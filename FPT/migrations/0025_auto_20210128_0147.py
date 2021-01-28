# Generated by Django 3.1.5 on 2021-01-28 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FPT', '0024_auto_20210127_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainee',
            name='dot',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='trainer',
            name='education',
            field=models.CharField(blank=True, default='Greenwich', max_length=50),
        ),
        migrations.AlterField(
            model_name='trainer',
            name='phone',
            field=models.CharField(blank=True, default='09xx', max_length=12),
        ),
        migrations.AlterField(
            model_name='trainer',
            name='working_place',
            field=models.CharField(blank=True, default='FPT Co.', max_length=50),
        ),
    ]