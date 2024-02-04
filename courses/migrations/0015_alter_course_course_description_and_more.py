# Generated by Django 4.2.8 on 2024-02-04 08:10

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0014_review_one_review_per_course_for_an_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="course_description",
            field=ckeditor.fields.RichTextField(blank=True, default="", verbose_name="Course Description"),
        ),
        migrations.AlterField(
            model_name="course",
            name="course_type",
            field=models.CharField(
                choices=[
                    ("NR", "No Record"),
                    ("MR", "Major Required"),
                    ("ME", "Major Elective"),
                    ("GE", "General Education"),
                    ("UC", "University Core"),
                    ("FE", "Free Elective"),
                    ("BBA", "BBA (Hons) Core"),
                    ("CR", "Concentration Required"),
                ],
                default="NR",
                max_length=10,
                verbose_name="Course Type",
            ),
        ),
        migrations.AlterField(
            model_name="course",
            name="update_time",
            field=models.DateTimeField(auto_now=True, verbose_name="Course information update time"),
        ),
    ]