# Generated by Django 4.2.4 on 2023-09-22 06:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courses',
            name='id',
        ),
        migrations.AddField(
            model_name='courses',
            name='course_id',
            field=models.AutoField(default=None, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='courses',
            name='user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]