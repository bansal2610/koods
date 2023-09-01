# Generated by Django 4.2.4 on 2023-08-19 05:23

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_alter_courses_course_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='course_image',
            field=cloudinary.models.CloudinaryField(default='courses/courses-1_p8zphw.jpg', max_length=255, verbose_name='image'),
        ),
    ]
