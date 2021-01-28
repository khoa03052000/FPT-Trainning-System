# Generated by Django 3.1.5 on 2021-01-28 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FPT', '0026_auto_20210128_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainee',
            name='age',
            field=models.IntegerField(blank=True, default=18, null=True),
        ),
        migrations.AlterField(
            model_name='trainee',
            name='education',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='trainee',
            name='experience',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='trainee',
            name='location',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='trainee',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='trainee',
            name='toeic_score',
            field=models.IntegerField(blank=True, default=5, null=True),
        ),
    ]