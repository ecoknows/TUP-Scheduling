from django.db import models
from wagtail.core.models import Page
from TUPScheduling.base.models import BasePage
from TUPScheduling import _COLOR, _CLASS_SCHEDULE, _DAY
from TUPScheduling.accounts.models import Professors


class InstructorSchedule(Page):
    max_count = 1
    parent_page_types = [BasePage]

    def get_context(self, request):
        context = super().get_context(request)

        final_schedule = request.user.students.section.schedules.all()

        i = 0
        list_of_professors = []
        for schedule in final_schedule:
            schedule.color = _COLOR[i]
            i += 1
            if schedule.prof not in list_of_professors:
                list_of_professors.append(schedule.prof)

            if schedule.starting_time < 7:
                schedule.new_time = str(schedule.starting_time) + " PM"
            elif schedule.starting_time == 12:
                schedule.new_time = str(schedule.starting_time) + " PM"
            else:
                schedule.new_time = str(schedule.starting_time) + " AM"

        list_of_professor_names = []
        list_of_professor_object = []
        for professor in list_of_professors:
            full_name = professor.first_name + ' ' + \
                professor.middle_name + '. ' + professor.last_name
            list_of_professor_names.append(full_name)

            list_of_professor_object.append(
                {'name': full_name, 'schedule': professor.schedules.all(), 'subjects': []})

        list_of_professor_names.append('- Select -')

        context['list_of_professors'] = list_of_professors
        context['list_of_professor_names'] = list_of_professor_names

        for professor in list_of_professor_object:
            for subject in professor['schedule']:
                if subject.subject not in professor['subjects']:
                    professor['subjects'].append(subject.subject)

        # context['professor_ojects'] = list_of_professor_object

        # context['schedules'] = final_schedule
        # context['class_schedule'] = _CLASS_SCHEDULE
        # context['days'] = _DAY

        return context
