import django_filters
from .models import Course


class CourseFilterSet(django_filters.FilterSet):
    course_code = django_filters.CharFilter(lookup_expr='icontains')
    course_name_en = django_filters.CharFilter(lookup_expr='icontains')
    course_name_cn = django_filters.CharFilter(lookup_expr='icontains')
    course_units = django_filters.NumberFilter(field_name='course_units', max_value=6, min_value=0)

    class Meta:
        model = Course
        fields = ['course_code', 'course_name_en', 'course_name_cn', 'course_units', 'course_type']
