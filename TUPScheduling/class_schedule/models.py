from django.db import models
from wagtail.core.models import Page
from TUPScheduling.base.models import BasePage
from TUPScheduling import _COLOR, _CLASS_SCHEDULE, _DAY


class ClassSchedule(Page):
    max_count = 1
    parent_page_types = [BasePage]

    def get_context(self, request):
        context = super().get_context(request)

        final_schedule = request.user.students.section.schedules.all()
        i = 0
        for schedule in final_schedule:
            schedule.color = _COLOR[i]
            i += 1

            if schedule.starting_time < 7:
                schedule.new_time = str(schedule.starting_time) + " PM"
            elif schedule.starting_time == 12:
                schedule.new_time = str(schedule.starting_time) + " PM"
            else:
                schedule.new_time = str(schedule.starting_time) + " AM"

        context['student'] = request.user.students
        context['schedules'] = final_schedule
        context['class_schedule'] = _CLASS_SCHEDULE
        context['days'] = _DAY

        return context


class ClassScheduleOverview(Page):
    max_count = 1
    parent_page_types = [ClassSchedule]

    def get_context(self, request):
        context = super().get_context(request)

        total_units = 0
        total_subjects = 0
        i = 0
        final_schedule = request.user.students.section.schedules.all()
        for schedule in final_schedule:
            total_units += schedule.subject.units
            total_subjects += 1

            schedule.color = _COLOR[i]
            print("asdsada_", _COLOR[i])
            i += 1

            if((schedule.starting_time + int(schedule.subject.hours)) == 12):
                schedule.time = (
                    str(schedule.starting_time) + ':00 - ' + '12:00')
            else:
                schedule.time = (str(schedule.starting_time) + ':00 - ' +
                                 str((schedule.starting_time + int(schedule.subject.hours)) % 12) + ':00')

        context['student'] = request.user.students
        context['schedules'] = final_schedule
        context['units'] = total_units
        context['total_subjects'] = total_subjects
        context['school_year'] = request.user.students.section.schedules.all()[
            0].school_year

        return context
