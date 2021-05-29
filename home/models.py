from wagtail.core.models import Page

from django.http import HttpResponseRedirect

class HomePage(Page):
    max_count = 1
    
    def serve(self, request):
        print(request.user.groups.all(), 'asdsad')
        if request.user.is_authenticated == False:
            return HttpResponseRedirect('/login/')
        for group in request.user.groups.all():
            if str(group) != 'Scheduler':
                return HttpResponseRedirect('/class-schedule/')
        return HttpResponseRedirect('/logout/')
    # table_count = 5
    # day = _DAY
    # time = _TIME

    # def get_context(self, request):
    #     context = super().get_context(request)
    #     print(Professors.objects.all())
    #     context['section_entries'] = Sections.objects.all()
    #     context['professor_entries'] = Professors.objects.all()
    #     context['room_entries'] = Rooms.objects.all()
    #     return context