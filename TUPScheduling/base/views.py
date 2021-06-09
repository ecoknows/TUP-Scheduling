
from wagtail.contrib.modeladmin.views import IndexView
from django.template.response import TemplateResponse
from django.http import JsonResponse
import csv, io
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from TUPScheduling.base.models import Colleges


def upload_file(request):
    print('Hello World')

# Create your views here.
# one parameter named request
def upload_file(request):
    # declaring template
    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return JsonResponse({'message': 'success'})
    csv_file = request.FILES['file']
    # let's check if it is a csv file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')

    data_set = csv_file.read().decode('UTF-8')
    # setup a stream which is when we loop through each line we are able to handle a data in a stream
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Colleges.objects.update_or_create(
            college_name=column[0],
        )
    return HttpResponseRedirect('/admin/base/colleges/')
