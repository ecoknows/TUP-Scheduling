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
        remove_schedule = request.POST.get('remove_schedule', None)
        update_schedule = request.POST.get('update_schedule', None)
        update_remove_schedule = request.POST.get('update_remove_schedule', None)
        update_add_schedule =  request.POST.get('update_add_schedule', None)
        
        if add_schedule:
            prof_pk = request.POST.get('prof_pk', None)
            room_pk = request.POST.get('room_pk', None)
            section_pk = request.POST.get('section_pk', None)
            day = request.POST.get('day', None)
            subject_pk = request.POST.get('subject', None)
            starting_time = request.POST.get('starting_time', None)
            professor = None
            if prof_pk:
                professor = Professors.objects.get(pk=prof_pk)

            print('WALAAAAAAAAAAAAAAAAAAAAAAAAAAAAA!!!!!!!!!!!!!', room_pk, section_pk, ' ECO ', subject_pk)
            room = Rooms.objects.get(pk=room_pk)
            section = Sections.objects.get(pk=section_pk)
            subject = Subjects.objects.get(pk=subject_pk)

            Schedule.objects.update_or_create(
                prof=professor,
                room=room,
                day=day,
                section=section,
                subject=subject,
                starting_time=starting_time,
                school_year='123421',
                
            )
        if update_add_schedule:
            day = request.POST.get('day', None)
            starting_time = request.POST.get('starting_time', None)
            schedule_pk = request.POST.get('schedule_pk', None)
            schedule = Schedule.objects.get(pk=schedule_pk)
            schedule.day = day
            schedule.starting_time = starting_time
            print(schedule)
            schedule.save()
        
        if remove_schedule:
            schedule_pk = request.POST.get('schedule_pk', None)
            Schedule.objects.get(pk=schedule_pk).delete()

        if update_schedule:
            schedule_pk = request.POST.get('schedule_pk', None)

            prof_pk = request.POST.get('prof_pk', None)
            professor = Professors.objects.get(pk=prof_pk)
            
            schedule = Schedule.objects.get(pk=schedule_pk)
            schedule.prof = professor
            schedule.save()
        
        if update_remove_schedule:
            schedule_pk = request.POST.get('schedule_pk', None)

            prof_pk = request.POST.get('prof_pk', None)
            professor = Professors.objects.get(pk=prof_pk)
            
            schedule = Schedule.objects.get(pk=schedule_pk)
            schedule.prof = None
            schedule.save()

        

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
            obj_room = {
                        'pk': temp_room.pk,
                        'name': temp_room.Room_Name,
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
                    scheduled = True

                section.subjects.append(
                    {
                        'subject_object': subject_object,
                        'scheduled': scheduled
                    }
                )
        

        context['already_schedule_object'] = Schedule.objects.all()
        print(context['already_schedule_object'])
        context['section_entries'] = sections

        return context
