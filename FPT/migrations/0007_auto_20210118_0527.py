# Generated by Django 3.1.5 on 2021-01-18 05:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('FPT', '0006_auto_20210118_0516'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='assigned_user_id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='assigned_user_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
    ]