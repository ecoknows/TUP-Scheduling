from django.db import models
from wagtail.core.models import Page
from TUPScheduling.base.models import BasePage, Rooms
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from TUPScheduling import _COLOR, _CLASS_SCHEDULE, _DAY

class RoomSchedule(RoutablePageMixin, Page):
    max_count = 1
    parent_page_types = [BasePage]
    
    @route(r'^(\d+)/$')
    def fetch_schedule(self, request, id=None):
        room = Rooms.objects.get(pk=id)

        if room:
            final_schedule = room.schedules.all()
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
                    
            return self.render(
                request,
                context_overrides={
                    'room': room,
                    'schedules': final_schedule,
                    'class_schedule': _CLASS_SCHEDULE,
                    'days': _DAY
                },
                template="room_schedule/scheduled_room.html",
            )

    def get_context(self, request):
        context = super().get_context(request)

        context['rooms'] = Rooms.objects.all()

        return context

