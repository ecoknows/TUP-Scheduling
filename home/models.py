from wagtail.core.models import Page

from django.http import HttpResponseRedirect

class HomePage(Page):
    max_count = 1
    
    def serve(self, request):
        return HttpResponseRedirect('/class-schedule/')
        
