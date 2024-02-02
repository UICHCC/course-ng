from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from django.db import models
from django.forms import CharField, ModelForm
# from django.utils.functional import lazy
from django.db.models import UniqueConstraint, Q

from course_ng.users.models import User

MAPPING = {
    'A': 4.0,
    'B': 3.0,
    'C': 2.0,
    'D': 1.0,
    'F': 0.0,
}


def digit_grade_to_letter(grade_sum):
    if grade_sum > 3.9:
        return 'A+'
    elif grade_sum >= 3.75:
        return 'A'
    elif grade_sum >= 3.5:
        return 'A-'
    elif grade_sum >= 3.25:
        return 'B+'
    elif grade_sum >= 3.0:
        return 'B'
    elif grade_sum >= 2.75:
        return 'B-'
    elif grade_sum >= 2.5:
        return 'C+'
    elif grade_sum >= 2.0:
        return 'C'
    elif grade_sum >= 1.75:
        return 'C-'
    elif grade_sum >= 1.5:
        return 'D+'
    elif grade_sum >= 1.0:
        return 'D'
    else:
        return 'F'


class Course(models.Model):
    COURSE_TYPE = [
        ("NR", "No Record"),
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
    course_name_cn = models.CharField(max_length=128, verbose_name="Course Chinese Name", blank=True)
    course_units = models.IntegerField(default=3, verbose_name="Course Credit")
    course_prerequisites = models.CharField(verbose_name="Course Prerequisites", default="", blank=True)
    course_exclusions = models.CharField(verbose_name="Course Exclusions", default="", blank=True)
    course_type = models.CharField(max_length=10, choices=COURSE_TYPE, default="NR")
    course_description = RichTextField(blank=True, default='')
    is_visible = models.BooleanField(default=True, verbose_name="Visibility of the course")
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course_code} {self.course_name_en}"

    @property
    def overall_grade(self):
        reviews = self.course_reviews.all()
        if not reviews:
            return {'content': 'N/A', 'teaching': 'N/A', 'grading': 'N/A', 'workload': 'N/A'}

        content_grade_sum = 0
        teaching_grade_sum = 0
        grading_grade_sum = 0
        workload_grade_sum = 0

        for review in reviews:
            content_grade_sum += MAPPING[review.content_grade]
            teaching_grade_sum += MAPPING[review.teaching_grade]
            grading_grade_sum += MAPPING[review.grading_grade]
            workload_grade_sum += MAPPING[review.workload_grade]

        content_grade_sum /= len(reviews)
        teaching_grade_sum /= len(reviews)
        grading_grade_sum /= len(reviews)
        workload_grade_sum /= len(reviews)

        return {'content': digit_grade_to_letter(content_grade_sum),
                'teaching': digit_grade_to_letter(teaching_grade_sum),
                'grading': digit_grade_to_letter(grading_grade_sum),
                'workload': digit_grade_to_letter(workload_grade_sum)}


class CourseNote(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="notes")
    note = models.CharField(max_length=500, verbose_name="Course Note")
    update_time = models.DateTimeField(auto_now=True)


class Lecturer(models.Model):
    name = models.CharField(verbose_name="Lecturer Name")
    alternative_name = models.CharField(verbose_name="Alternative Name", blank=True)
    faculties = models.CharField(verbose_name="Lecturer Faculties", blank=True)
    url = models.URLField(verbose_name="Lecturer Homepage URL", blank=True)
    is_resigned = models.BooleanField(default=False, verbose_name="The lecturer is resigned from the college")

    def __str__(self):
        return self.name


LETTER_GRADE = [
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('F', 'F')
]

SEMESTER = [
    ('NOTSPEC', 'Not Specified'),
    # ('23-24-4', '2023-2024 Summer'),
    # ('23-24-3', '2023-2024 Spring'),
    # ('23-24-2', '2023-2024 Winter'),
    ('23-24-1', '2023-2024 Fall'),
    ('22-23-4', '2022-2023 Summer'),
    ('22-23-3', '2022-2023 Spring'),
    ('22-23-2', '2022-2023 Winter'),
    ('22-23-1', '2022-2023 Fall'),
    ('21-22-4', '2021-2022 Summer'),
    ('21-22-3', '2021-2022 Spring'),
    ('21-22-2', '2021-2022 Winter'),
    ('21-22-1', '2021-2022 Fall'),
    ('20-21-4', '2020-2021 Summer'),
    ('20-21-3', '2020-2021 Spring'),
    ('20-21-2', '2020-2021 Winter'),
    ('20-21-1', '2020-2021 Fall'),
    ('19-20-4', '2019-2020 Summer'),
    ('19-20-3', '2019-2020 Spring'),
    ('19-20-2', '2019-2020 Winter'),
    ('19-20-1', '2019-2020 Fall'),
]


class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_reviews")
    semester = models.CharField(verbose_name="Semester", choices=SEMESTER, default="NOTSPEC")
    summary = models.CharField(verbose_name="Short Review Summary")
    lecturer = models.ManyToManyField(Lecturer, verbose_name="Lecturers", blank=True)
    content = models.TextField(verbose_name="Content Comment", blank=True)
    content_grade = models.CharField(verbose_name="Content Letter Grade", choices=LETTER_GRADE, default='C')
    teaching = models.TextField(verbose_name="Teaching Comment", blank=True)
    teaching_grade = models.CharField(verbose_name="Teaching Letter Grade", choices=LETTER_GRADE, default='C')
    grading = models.TextField(verbose_name="Grading Comment", blank=True)
    grading_grade = models.CharField(verbose_name="Grading Letter Grade", choices=LETTER_GRADE, default='C')
    workload = models.TextField(verbose_name="Workload Comment", blank=True)
    workload_grade = models.CharField(verbose_name="Workload Letter Grade", choices=LETTER_GRADE, default='C')
    mid_term = models.BooleanField(verbose_name="Has Mid-term", default=False)
    final_exam = models.BooleanField(verbose_name="Has Final Exam", default=True)
    quiz = models.BooleanField(verbose_name="Has Quiz", default=False)
    assignment = models.BooleanField(verbose_name="Has Assignment", default=False)
    essay = models.BooleanField(verbose_name="Has Essay", default=False)
    project = models.BooleanField(verbose_name="Has Project", default=False)
    attendance = models.BooleanField(verbose_name="Has Attendance", default=False)
    reading_material = models.BooleanField(verbose_name="Has Reading Material", default=False)
    presentation = models.BooleanField(verbose_name="Has Presentation", default=False)
    submit_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.reviewer.email} review on {self.course.course_code}'

    class Meta:
        constraints = [
            UniqueConstraint(fields=('reviewer', 'course'), name='one_review_per_course_for_an_user'),
        ]

    @property
    def overall_score_grade(self):
        grade_sum = 0

        grade_sum += MAPPING[self.content_grade]
        grade_sum += MAPPING[self.teaching_grade]
        grade_sum += MAPPING[self.grading_grade]
        grade_sum += MAPPING[self.workload_grade]
        grade_sum /= 4

        return grade_sum

    @property
    def overall_grade(self):
        return digit_grade_to_letter(self.overall_score_grade)


