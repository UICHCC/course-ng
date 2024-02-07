from django import template
from django.urls import reverse
from courses.models import Course
from django.utils.safestring import mark_safe

import re

register = template.Library()


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Return encoded URL parameters that are the same as the current
    request's parameters, only with the specified GET parameters added or changed.

    It also removes any empty parameters to keep things neat,
    so you can remove a parm by setting it to ``""``.

    For example, if you're on the page ``/things/?with_frosting=true&page=5``,
    then

    <a href="/things/?{% param_replace page=3 %}">Page 3</a>

    would expand to

    <a href="/things/?with_frosting=true&page=3">Page 3</a>

    Based on
    https://stackoverflow.com/questions/22734695/next-and-before-links-for-a-django-paginated-query/22735278#22735278
    """
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()


@register.simple_tag
def course_link(value):
    output_string = value
    pattern = re.compile(r'([A-Z]+[0-9]{4})')
    for course_code in re.findall(pattern, value):
        course = Course.objects.filter(course_code=course_code)
        if course.exists():
            course = course.first()
            output_string = output_string.replace(course_code, f"<a href='{reverse('courses:course-detail', args=[course.id])}'>{course_code}</a>")
    output_string = output_string.replace(" or ", " <span class='text-danger'>or</span><br/>")
    output_string = output_string.replace(" and ", "<br/><span class='text-success'>and</span><br/>")
    return output_string


@register.simple_tag
def letter_grade_badge(grade):
    if grade == 'A+':
        return mark_safe(f'<span class="badge px-3 bg-ap">{grade}</span>')
    if grade == 'A':
        return mark_safe(f'<span class="badge px-3 bg-a">{grade}</span>')
    if grade == 'A-':
        return mark_safe(f'<span class="badge px-3 bg-am">{grade}</span>')
    if grade == 'B+':
        return mark_safe(f'<span class="badge px-3 bg-bp">{grade}</span>')
    if grade == 'B':
        return mark_safe(f'<span class="badge px-3 bg-b">{grade}</span>')
    if grade == 'B-':
        return mark_safe(f'<span class="badge px-3 bg-bm">{grade}</span>')
    if grade == 'C+':
        return mark_safe(f'<span class="badge px-3 bg-cp">{grade}</span>')
    if grade == 'C':
        return mark_safe(f'<span class="badge px-3 bg-c">{grade}</span>')
    if grade == 'C-':
        return mark_safe(f'<span class="badge px-3 bg-cm">{grade}</span>')
    if grade == 'D+':
        return mark_safe(f'<span class="badge px-3 bg-dp">{grade}</span>')
    if grade == 'D':
        return mark_safe(f'<span class="badge px-3 bg-d">{grade}</span>')
    if grade == 'F':
        return mark_safe(f'<span class="badge px-3 bg-f">{grade}</span>')
    return mark_safe(f'<span class="badge px-3 bg-secondary">{grade}</span>')

