# Generated by Django 3.1.7 on 2021-04-07 09:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_courses_created_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courses',
            old_name='Department',
            new_name='department',
        ),
        migrations.RenameField(
            model_name='courses',
            old_name='Instructor',
            new_name='instructor',
        ),
    ]