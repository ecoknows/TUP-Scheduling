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

            subject_color = {}
            subject_holder = []
            no_duplicate = []
            i = 0
            for schedule in final_schedule:
                if schedule.subject not in subject_holder:
                    subject_color[schedule.subject.description] = _COLOR[i]
                    subject_holder.append(schedule.subject)

                    schedule.color = subject_color[schedule.subject.description]
                    no_duplicate.append(schedule)

                    i += 1
                schedule.color = subject_color[schedule.subject.description]

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
                    'days': _DAY,
                    'no_duplicate': no_duplicate
                },
                template="room_schedule/scheduled_room.html",
            )

    def get_context(self, request):
        context = super().get_context(request)

        context['rooms'] = Rooms.objects.all()
        

        return context

