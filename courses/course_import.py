from models import Course
import pandas as pd


def import_courses():
    course_pd = pd.read_csv('assets/records.tsv', sep='\t')
    for course in course_pd.iterrows():
        obj = Course(course_code=course[1]['course_code'], course_name_en=course[1]['course_name'],
                     course_prerequisites=course[1]['prerequisite'], course_units=course[1]['unit'])
        obj.save()


def update_courses():
    course_pd = pd.read_csv('assets/records-translate.tsv', sep='\t')
    for course in course_pd.iterrows():
        obj = Course.objects.filter(course_code=course[1]['course_code'])
        obj.update(course_name_cn=course[1]['course_name_cn'])

if __name__ == "__main__":
    import_courses()
