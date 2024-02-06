from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from braces.views import SuperuserRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import datetime

from courses.models import Course, Review
from courses.forms import CourseForm, ReviewForm
from courses.filters import CourseFilterSet


class CourseListView(LoginRequiredMixin, ListView):
    filter_set = CourseFilterSet
    model = Course
    paginate_by = 15
    template_name = 'pages/courses_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filter_set(self.request.GET, queryset=queryset)
        # Return the filtered queryset
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter_set(self.request.GET, queryset=self.get_queryset())
        return context


class CourseHomePageView(LoginRequiredMixin, TemplateView):
    template_name = "pages/courses.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courses"] = Course.objects.all()[:10]
        return context


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    slug_field = "id"
    slug_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['current_user_reviewed'] = Review.objects.filter(course=self.object.id, reviewer=self.request.user).exists()
        return context


course_detail_view = CourseDetailView.as_view()


class CourseCreateView(SuperuserRequiredMixin, CreateView):
    template_name = "courses/course_form.html"
    model = Course
    success_url = reverse_lazy("home")
    form_class = CourseForm


class CourseUpdateView(SuperuserRequiredMixin, UpdateView):
    template_name = "courses/course_edit_form.html"
    model = Course
    fields = "__all__"

    def get_success_url(self):
        course_id = self.kwargs["pk"]
        return reverse_lazy("courses:course-detail", kwargs={"pk": course_id})


class CourseDeleteView(LoginRequiredMixin, SuperuserRequiredMixin, DeleteView):
    template_name = "courses/course_confirm_delete.html"
    model = Course
    success_url = reverse_lazy("courses:courses")


# Create your views here.
class CourseReviewCreateView(LoginRequiredMixin, CreateView):
    course_id = None
    template_name = "courses/course_review_form.html"
    model = Review
    form_class = ReviewForm

    def get_initial(self):
        return {
            'reviewer': self.request.user,
            'course': self.kwargs['pk']
        }

    def form_valid(self, form):
        form.instance.reviewer = self.request.user
        return super(CourseReviewCreateView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CourseReviewCreateView, self).get_context_data(**kwargs)
        context['review_course'] = Course.objects.get(pk=self.kwargs['pk'])
        context['course_id'] = self.kwargs['pk']
        return context

    def get_success_url(self):
        return reverse_lazy('courses:course-detail', kwargs={'pk': self.kwargs.get('pk')})


class CourseReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "courses/course_review_edit_form.html"
    model = Review
    form_class = ReviewForm

    def test_func(self):
        if self.get_object().submit_date > timezone.now() - datetime.timedelta(days=7):
            messages.add_message(self.request,
                                 messages.INFO,
                                 _("Review is allow to update within 7 days after you initial submit."))
        else:
            messages.add_message(self.request,
                                 messages.WARNING,
                                 _("Review is not allow to update after 7 days since your initial submit."))
            return False
        return self.request.user == self.get_object().reviewer

    def get_context_data(self, **kwargs):
        context = super(CourseReviewUpdateView, self).get_context_data(**kwargs)
        context['review'] = Review.objects.get(pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        review_id = self.kwargs["pk"]
        rv = Review.objects.get(pk=review_id)
        return reverse_lazy("courses:course-detail", kwargs={"pk": rv.course.id})
