# Generated by Django 4.2.4 on 2023-09-22 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_remove_courses_id_courses_course_id_courses_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='course_price',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
    ]