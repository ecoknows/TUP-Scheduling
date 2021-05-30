from wagtail.core.models import Page
from django.db import models

from wagtail.snippets.models import register_snippet
from TUPScheduling import _DAY, _TIME
from administrator.models import Sections, Rooms
from accounts.models import Professors

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
    table_count = 5
    day = _DAY
    time = _TIME

    
    def get_context(self, request):
        context = super().get_context(request)
        print(Professors.objects.all())
        context['section_entries'] = Sections.objects.all()
        context['professor_entries'] = Professors.objects.all()
        context['room_entries'] = Rooms.objects.all()
        return context



# import csv, io
# from django.shortcuts import render
# from django.contrib import messages
# # Create your views here.
# # one parameter named request
# def profile_upload(request):
#     # declaring template
#     template = "profile_upload.html"
#     data = Profile.objects.all()
# # prompt is a context variable that can have different values      depending on their context
#     prompt = {
#         'order': 'Order of the CSV should be name, email, address,    phone, profile',
#         'profiles': data    
#               }
#     # GET request returns the value of the data with the specified key.
#     if request.method == "GET":
#         return render(request, template, prompt)
#     csv_file = request.FILES['file']
#     # let's check if it is a csv file
#     if not csv_file.name.endswith('.csv'):
#         messages.error(request, 'THIS IS NOT A CSV FILE')
#     data_set = csv_file.read().decode('UTF-8')
#     # setup a stream which is when we loop through each line we are able to handle a data in a stream
# io_string = io.StringIO(data_set)
# next(io_string)
# for column in csv.reader(io_string, delimiter=',', quotechar="|"):
#     _, created = Profile.objects.update_or_create(
#         name=column[0],
#         email=column[1],
#         address=column[2],
#         phone=column[3],
#         profile=column[4]
#     )
# context = {}
# return render(request, template, context)