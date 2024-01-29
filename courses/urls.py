from django.urls import path

from courses.views import CourseCreateView, CourseDeleteView, CourseHomePageView, CourseUpdateView, course_detail_view

app_name = "courses"
urlpatterns = [
    path("", CourseHomePageView.as_view(), name="courses"),
    path("add/", CourseCreateView.as_view(), name="course-add"),
    path("<int:pk>/~update/", CourseUpdateView.as_view(), name="course-update"),
    path("<int:pk>/", course_detail_view, name="course-detail"),
    path("<int:pk>/~delete/", CourseDeleteView.as_view(), name="course-delete"),
]
