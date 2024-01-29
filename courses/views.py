from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView

from courses.models import Course, CourseForm


class CourseHomePageView(TemplateView):
    template_name = "pages/courses.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courses"] = Course.objects.all()[:10]
        return context


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    slug_field = "id"
    slug_url_kwarg = "id"


course_detail_view = CourseDetailView.as_view()


class CourseCreateView(LoginRequiredMixin, CreateView):
    template_name = "courses/course_form.html"
    model = Course
    success_url = reverse_lazy("home")
    form_class = CourseForm


class CourseUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "courses/course_edit_form.html"
    model = Course
    fields = "__all__"

    def get_success_url(self):
        course_id = self.kwargs["pk"]
        return reverse_lazy("courses:course-detail", kwargs={"pk": course_id})


class CourseDeleteView(DeleteView):
    model = Course
    success_url = reverse_lazy("home")


# Create your views here.
