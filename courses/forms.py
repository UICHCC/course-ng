from ckeditor.widgets import CKEditorWidget
from django import forms

from courses.models import Course


class CourseForm(forms.Form):
    course_description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Course
        exclude = ["update_time"]
