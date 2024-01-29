# Generated by Django 4.2.8 on 2024-01-28 07:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0003_alter_course_course_exclusions_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="course_exclusions",
            field=models.CharField(blank=True, default="", verbose_name="Course Exclusions"),
        ),
        migrations.AlterField(
            model_name="course",
            name="course_prerequisites",
            field=models.CharField(blank=True, default="", verbose_name="Course Prerequisites"),
        ),
    ]