from django.urls import path, re_path

from courses.views import (CourseCreateView, CourseDeleteView, CourseListView, CourseUpdateView,
                           course_detail_view, CourseReviewCreateView, CourseReviewUpdateView)
from courses.autocomplete import LecturerAutoComplete

app_name = "courses"
urlpatterns = [
    # path("", CourseHomePageView.as_view(), name="courses"),
    path("", CourseListView.as_view(), name="courses"),
    path("add/", CourseCreateView.as_view(), name="course-add"),
    path("<int:pk>/~update/", CourseUpdateView.as_view(), name="course-update"),
    path("<int:pk>/", course_detail_view, name="course-detail"),
    path("<int:pk>/~delete/", CourseDeleteView.as_view(), name="course-delete"),
    path("<int:pk>/~add-review", CourseReviewCreateView.as_view(), name="create-course-review"),
    path("review/<int:pk>/~update/", CourseReviewUpdateView.as_view(), name="update-course-review"),
    re_path(r'^lecturer-autocomplete/$', LecturerAutoComplete.as_view(), name='lecturer-autocomplete',
    ),
]
