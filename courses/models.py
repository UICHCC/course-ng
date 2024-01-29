from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from django.db import models
from django.forms import CharField, ModelForm

# Create your models here.


class Course(models.Model):
    COURSE_TYPE = [
        ("MR", "Major Required"),
        ("ME", "Major Elective"),
        ("GEC", "General Education Core"),
        ("GED", "General Education Distribution"),
        ("WPE", "Whole Person Education Experiential Learning"),
        ("FE", "Free Elective"),
        ("BBA", "BBA (Hons) Core"),
        ("CR", "Concentration Required"),
    ]
    course_code = models.CharField(max_length=32, verbose_name="Course Code")
    course_name_en = models.CharField(max_length=128, verbose_name="Course English Name")
    course_name_cn = models.CharField(max_length=128, verbose_name="Course Chinese Name")
    course_units = models.IntegerField(default=3, verbose_name="Course Credit")
    course_prerequisites = models.CharField(verbose_name="Course Prerequisites", default="", blank=True)
    course_exclusions = models.CharField(verbose_name="Course Exclusions", default="", blank=True)
    course_type = models.CharField(max_length=10, choices=COURSE_TYPE, default="MR")
    course_description = RichTextField()
    is_visible = models.BooleanField(default=True, verbose_name="Visibility of the course")
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course_code} {self.course_name_en}"


class CourseForm(ModelForm):
    course_description = CharField(widget=CKEditorWidget())

    class Meta:
        model = Course
        exclude = ["update_time"]


class CourseNote(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="notes")
    note = models.CharField(max_length=500, verbose_name="Course Note")
    update_time = models.DateTimeField(auto_now=True)


class Lecturer(models.Model):
    name = models.CharField(verbose_name="Lecturer Name")
    url = models.URLField(verbose_name="Lecturer Homepage URL")
    is_resigned = models.BooleanField(default=False, verbose_name="The lecturer is resigned from the college")
