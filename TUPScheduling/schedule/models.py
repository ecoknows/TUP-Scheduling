from wagtail.core.models import Page
from django.db import models

from wagtail.snippets.models import register_snippet
from TUPScheduling import _DAY, _TIME
from TUPScheduling.base.models import CourseCurriculum, Sections, Rooms, BasePage, Subjects, SubjectsOrderable
from TUPScheduling.accounts.models import Professors


class Schedule(models.Model):
    prof = models.ForeignKey(
        Professors,
        null=True,
        on_delete=models.CASCADE,
        related_name='schedules'
    )
    starting_time = models.CharField(
        max_length=200,
        null=True,
    )
    school_year = models.CharField(
        max_length=200,
        null=True,
    )
    room = models.ForeignKey(
        Rooms,
        null=True,
        on_delete=models.SET_NULL,
        related_name='schedules'
    )
    section = models.ForeignKey(
        Sections,
        null=True,
        on_delete=models.CASCADE,
        related_name='schedules'
    )
    subject = models.ForeignKey(
        Subjects,
        null=True,
        on_delete=models.CASCADE,
        related_name='schedules'
    )
    day = models.CharField(
        max_length=20,
        null=True,
        choices=tuple([(day, day) for day in _DAY])
    )


class SchedulePage(Page):
    max_count = 1
    table_count = 5
    day = _DAY
    time = _TIME
    parent_page_types = [BasePage]

    def serve(self, request):
        add_schedule = request.POST.get('add_schedule', None)

        if add_schedule:
            prof_pk = request.POST.get('prof_pk', None)
            room_pk = request.POST.get('room_pk', None)
            section_pk = request.POST.get('section_pk', None)
            subject = request.POST.get('subject', None)
            year = request.POST.get('year', None)
            starting_tine = request.POST.get('starting_tine', None)

            professor = Professors.objects.get(pk=prof_pk)
            room = Professors.objects.get(pk=room_pk)
            section = Professors.objects.get(pk=section_pk)
            subject = Professors.objects.get(pk=subject)

            # Schedule.objects.create(
            #     professor=professor,
            #     room=room,
            #     section=section,
            #     subject=subject,
            #     starting_time='1232134',
            #     school_year='123421'
            # )

        return super().serve(request)

    def get_context(self, request):
        context = super().get_context(request)

        department = 24
        profs = Professors.objects.filter(
            choose_department_id=department)

        for prof in profs:
            prof.units = 0

        context['professor_entries'] = profs

        temp_rooms = Rooms.objects.filter(
            choose_department_id=department)
        new_rooms = []
        for temp_room in temp_rooms:
            obj_room = {'name': temp_room.Room_Name,
                        'type': temp_room.Room_Type,
                        }
            new_rooms.append(obj_room)

        context['room_entries'] = new_rooms

        context['subject_entries'] = Subjects.objects.filter(
            choose_department_id=department)

        sections = Sections.objects.filter(
            course_curriculum_id__choose_department_id=department,
        )

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

        already_schedule_object = []

        for section in sections:
            section.subjects = []
            for subject in section.subjects_query:
                subject_object = Subjects.objects.get(id=subject)
                scheduled = False
                if len(section.schedules.all()) > 0 and subject_object.schedules.all():
                    schedule = section.schedules.all().first()
                    already_schedule_object.append(schedule)
                    scheduled = True

                section.subjects.append(
                    {
                        'subject_object': subject_object,
                        'scheduled': scheduled
                    }
                )

        context['already_schedule_object'] = already_schedule_object
        context['section_entries'] = sections

        return context
