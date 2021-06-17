from django.db import models
from wagtail.core.models import Page
from TUPScheduling.base.models import BasePage, Rooms

class RoomSchedule(Page):
    max_count = 1
    parent_page_types = [BasePage]
    

    def get_context(self, request):
        context = super().get_context(request)

        context['rooms'] = Rooms.objects.all()

        return context


class ScheduledRoom(Page):
    max_count = 1
    parent_page_types = [RoomSchedule]
    
    def get_context(self, request):
        context = super().get_context(request)

        return context