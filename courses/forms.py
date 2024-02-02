from ckeditor.widgets import CKEditorWidget
from django import forms
from dal import autocomplete
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, MultiField
from crispy_forms.bootstrap import InlineRadios
from courses.models import Course, Review


class CourseForm(forms.ModelForm):
    course_description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Course
        exclude = ["update_time"]


class ReviewForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['course'].disabled = True
        self.fields['reviewer'].disabled = True
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Basic',
                Div(
                    Div('course', css_class='col-md-6'),
                    Div('reviewer', css_class='col-md-6'),
                    css_class='row',
                ),
                'semester',
                'lecturer',
                'summary',
            ),
            Fieldset(
                'Your Comments',
                Div(
                    Div(
                        Div(
                            'content',
                            InlineRadios('content_grade'), css_class='col-md-6'
                        ),
                        Div(
                            'teaching',
                            InlineRadios('teaching_grade'), css_class='col-md-6'
                        ), css_class='row',
                    ),
                    Div(
                        Div(
                            'grading',
                            InlineRadios('grading_grade'), css_class='col-md-6'
                        ),
                        Div(
                            'workload',
                            InlineRadios('workload_grade'), css_class='col-md-6'
                        ), css_class='row',
                    )
                )

            ),
            Fieldset(
                'Assessments/Materials',
                'quiz',
                'assignment',
                'essay',
                'project',
                'attendance',
                'reading_material',
                'presentation',
                'mid_term',
                'final_exam',
                css_class="d-flex flex-wrap justify-content-evenly"
            ),
            Submit('submit', 'Submit', css_class='btn btn-primary'),
        )

    class Meta:
        model = Review
        widgets = {
            'lecturer': autocomplete.ModelSelect2Multiple(
                url="courses:lecturer-autocomplete",
            ),
            'content_grade': forms.RadioSelect(),
            'teaching_grade': forms.RadioSelect(),
            'workload_grade': forms.RadioSelect(),
            'grading_grade': forms.RadioSelect(),
        }
        exclude = ["submit_date"]
