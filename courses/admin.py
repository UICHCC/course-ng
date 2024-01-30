from django.contrib import admin

from .models import Course, CourseNote, Lecturer, Review

# Register your models here.


admin.site.register(Course)
admin.site.register(CourseNote)
admin.site.register(Lecturer)
admin.site.register(Review)
