from wagtail.core.models import Page
from django.db import models

from wagtail.snippets.models import register_snippet
from TUPScheduling import _DAY, _TIME
from TUPScheduling.base.models import CourseCurriculum, Sections, Rooms, BasePage, Subjects, SubjectsOrderable
from TUPScheduling.accounts.models import Professors


@register_snippet
class SectionsSchedule(models.Model):
    pass


@register_snippet
class ProfessorsSchedule(models.Model):
    pass


@register_snippet
class RoomsSchedule(models.Model):
    pass


class Schedule(Page):
    max_count = 1
    table_count = 5
    day = _DAY
    time = _TIME
    parent_page_types = [BasePage]

    def get_context(self, request):
        context = super().get_context(request)
        # print(Professors.objects.all())

        department = 24
        context['professor_entries'] = Professors.objects.filter(
            choose_department_id=department)
        context['room_entries'] = Rooms.objects.filter(
            choose_department_id=department)
        context['subject_entries'] = Subjects.objects.filter(
            choose_department_id=department)

        sections = Sections.objects.filter(
            course_curriculum_id__choose_department_id=department)

        for section in sections:
            section.subjects_query = []

            if section.year_level == "1st Year" and section.sem == "First":
                section.subjects_query.append(list(SubjectsOrderable.objects.values_list('subject_id', flat=True).filter(
                    first_year_first_sem_id=section.course_curriculum_id)))

            elif section.year_level == "1st Year" and section.sem == "Second":
                section.subjects_query.append(list(SubjectsOrderable.objects.values_list('subject_id', flat=True).filter(
                    first_year_second_sem_id=section.course_curriculum_id)))

            elif section.year_level == "2nd Year" and section.sem == "First":
                section.subjects_query.append(list(SubjectsOrderable.objects.values_list('subject_id', flat=True).filter(
                    second_year_first_sem_id=section.course_curriculum_id)))

            elif section.year_level == "2nd Year" and section.sem == "Second":
                section.subjects_query.append(list(SubjectsOrderable.objects.values_list('subject_id', flat=True).filter(
                    second_year_second_sem_id=section.course_curriculum_id)))

            elif section.year_level == "3rd Year" and section.sem == "First":
                section.subjects_query.append(list(SubjectsOrderable.objects.values_list('subject_id', flat=True).filter(
                    third_year_first_sem_id=section.course_curriculum_id)))

            elif section.year_level == "3rd Year" and section.sem == "Second":
                section.subjects_query.append(list(SubjectsOrderable.objects.values_list('subject_id', flat=True).filter(
                    third_year_second_sem_id=section.course_curriculum_id)))

            elif section.year_level == "4th Year" and section.sem == "First":
                section.subjects_query.append(list(SubjectsOrderable.objects.values_list('subject_id', flat=True).filter(
                    fourth_year_first_sem_id=section.course_curriculum_id)))

            elif section.year_level == "4th Year" and section.sem == "Second":
                section.subjects_query.append(list(SubjectsOrderable.objects.values_list('subject_id', flat=True).filter(
                    fourth_year_second_sem_id=section.course_curriculum_id)))

            section.subjects_query = section.subjects_query[0]

        for section in sections:
            section.subjects = []
            for subject in section.subjects_query:
                section.subjects.append(Subjects.objects.get(id=subject))

        context['section_entries'] = sections

        return context


# import csv, io
# from django.shortcuts import render
# from django.contrib import messages
# # Create your views here.
# # one parameter named request
# def profile_upload(request):
#     # declaring template
#     template = "profile_upload.html"
#     data = Profile.objects.all()
# # prompt is a context variable that can have different values      depending on their context
#     prompt = {
#         'order': 'Order of the CSV should be name, email, address,    phone, profile',
#         'profiles': data
#               }
#     # GET request returns the value of the data with the specified key.
#     if request.method == "GET":
#         return render(request, template, prompt)
#     csv_file = request.FILES['file']
#     # let's check if it is a csv file
#     if not csv_file.name.endswith('.csv'):
#         messages.error(request, 'THIS IS NOT A CSV FILE')
#     data_set = csv_file.read().decode('UTF-8')
#     # setup a stream which is when we loop through each line we are able to handle a data in a stream
# io_string = io.StringIO(data_set)
# next(io_string)
# for column in csv.reader(io_string, delimiter=',', quotechar="|"):
#     _, created = Profile.objects.update_or_create(
#         name=column[0],
#         email=column[1],
#         address=column[2],
#         phone=column[3],
#         profile=column[4]
#     )
# context = {}
# return render(request, template, context)
