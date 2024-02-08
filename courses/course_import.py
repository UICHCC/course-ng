from models import Course, Lecturer, CourseNote
import pandas as pd


def import_lecturer():
    lecturer_pd = pd.read_csv('courses/assets/lecturer.tsv', sep='\t')
    for lecturer in lecturer_pd.iterrows():
        obj = Lecturer(name=lecturer[1]['FL'], alternative_name=lecturer[1]['LF'])
        obj.save()


def import_courses():
    course_pd = pd.read_csv('courses/assets/records-2024.tsv', sep='\t')
    course_pd = course_pd.fillna('')
    for course in course_pd.iterrows():
        if Course.objects.filter(course_code=course[1]['course_code']).exists():
            Course.objects.filter(course_code=course[1]['course_code']).update(course_name_en=course[1]['course_name'],
                                                                               course_prerequisites=course[1][
                                                                                   'prerequisite'],
                                                                               course_units=course[1]['unit'])
        else:
            obj = Course(course_code=course[1]['course_code'], course_name_en=course[1]['course_name'],
                         course_prerequisites=course[1]['prerequisite'], course_units=course[1]['unit'])
            obj.save()


def import_description():
    desc_pd = pd.read_csv('courses/assets/2024_description.tsv', sep='\t')
    for course in desc_pd.iterrows():
        Course.objects.filter(course_code=course[1]['course_code']).update(
            course_description=course[1]['course_description'])


def update_courses_cn():
    course_pd = pd.read_csv('courses/assets/records-translate.tsv', sep='\t')
    for course in course_pd.iterrows():
        obj = Course.objects.filter(course_code=course[1]['course_code'])
        obj.update(course_name_cn=course[1]['course_name_cn'])


def update_course_type():
    Course.objects.filter(course_code__contains='GCAP').update(course_type='GE')
    Course.objects.filter(course_code__contains='GTSU').update(course_type='GE')
    Course.objects.filter(course_code__contains='GTSC').update(course_type='GE')
    Course.objects.filter(course_code__contains='GTCU').update(course_type='GE')
    Course.objects.filter(course_code__contains='GFHC').update(course_type='GE')
    Course.objects.filter(course_code__contains='GFQR').update(course_type='GE')
    Course.objects.filter(course_code__contains='GFVM').update(course_type='GE')
    Course.objects.filter(course_code__contains='WPEX').update(course_type='UC')
    Course.objects.filter(course_code__contains='MT1003').update(course_type='UC')
    Course.objects.filter(course_code__contains='CHI').update(course_type='UC')
    Course.objects.filter(course_code__contains='UCLC').update(course_type='UC')
    course_pd = pd.read_csv('courses/assets/course_type.tsv', sep='\t')
    for course in course_pd.iterrows():
        if Course.objects.filter(course_code=course[1]['course_code']).exists():
            Course.objects.filter(course_code=course[1]['course_code']).update(course_type=course[1]['course_type'])
        else:
            pass

def update_course_notes():
    note_pd = pd.read_csv('courses/assets/course_notes.tsv', sep='\t')
    note_pd = note_pd.fillna('')
    for course in note_pd.iterrows():
        c = Course.objects.filter(course_code=course[1]['course_code']).first()
        if course[1]['mr_message']:
            mr = CourseNote(course=c, note=course[1]['mr_message'])
            mr.save()
        if course[1]['me_message']:
            me = CourseNote(course=c, note=course[1]['me_message'])
            me.save()
        if course[1]['cr_message']:
            cr = CourseNote(course=c, note=course[1]['cr_message'])
            cr.save()


if __name__ == "__main__":
    import_courses()
