from django.db import models
from wagtail.core.models import Page
from TUPScheduling.base.models import BasePage
from TUPScheduling import _COLOR, _CLASS_SCHEDULE, _DAY


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

        context['list_of_professors'] = list_of_professors
        #context['professors'] = request.user.prof
        context['schedules'] = final_schedule
        context['class_schedule'] = _CLASS_SCHEDULE
        context['days'] = _DAY

        return context
