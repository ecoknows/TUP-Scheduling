from django.db import models
from wagtail.core.models import Page
from TUPScheduling.base.models import BasePage


class ClassSchedule(Page):
    max_count = 1
    parent_page_types = [BasePage]

    def get_context(self, request):
        context = super().get_context(request)

        context['student'] = request.user.students
        context['schedules'] = request.user.students.section.schedules.all()

        return context


class ClassScheduleOverview(Page):
    max_count = 1
    parent_page_types = [ClassSchedule]

    def get_context(self, request):
        context = super().get_context(request)

        total_units = 0
        total_subjects = 0
        list_of_time = []
        for schedule in request.user.students.section.schedules.all():
            total_units += schedule.subject.units
            total_subjects += 1

        context['student'] = request.user.students
        context['schedules'] = request.user.students.section.schedules.all()
        context['units'] = total_units
        context['total_subjects'] = total_subjects
        context['student'] = request.user.students
        context['school_year'] = request.user.students.section.schedules.all()[
            0].school_year

        return context
