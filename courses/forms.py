from ckeditor.widgets import CKEditorWidget
from django import forms
from dal import autocomplete

from courses.models import Course, Review


class CourseForm(forms.ModelForm):
    course_description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Course
        exclude = ["update_time"]


class ReviewForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].disabled = True
        self.fields['reviewer'].disabled = True
    class Meta:
        model = Review
        widgets = {
            'lecturer': autocomplete.ModelSelect2Multiple(
                url="courses:lecturer-autocomplete",
            ),
        }
        exclude = ["submit_date"]
