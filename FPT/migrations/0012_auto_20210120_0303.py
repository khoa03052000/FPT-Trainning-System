# Generated by Django 3.1.5 on 2021-01-20 03:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('FPT', '0011_user_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='assigned_user_id',
        ),
        migrations.RemoveField(
            model_name='course',
            name='assigned_user_type',
        ),
        migrations.CreateModel(
            name='AssignUserToCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_user_id', models.BigIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assigned_user_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_type', to='contenttypes.contenttype')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_assign', to='FPT.course')),
            ],
        ),
    ]
