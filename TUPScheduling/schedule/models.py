from wagtail.core.models import Page
from django.db import models

from wagtail.snippets.models import register_snippet
from TUPScheduling import _DAY, _TIME
from TUPScheduling.base.models import Sections, Rooms, BasePage
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
        print(Professors.objects.all())
        context['section_entries'] = Sections.objects.all()
        context['professor_entries'] = Professors.objects.all()
        context['room_entries'] = Rooms.objects.all()
        return context


