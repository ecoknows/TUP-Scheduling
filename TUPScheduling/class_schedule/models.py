from django.db import models
from wagtail.core.models import Page
from TUPScheduling.base.models import BasePage


class ClassSchedule(Page):
    max_count = 1
    parent_page_types = [BasePage]

class ClassScheduleOverview(Page):  
    max_count = 1
    parent_page_types = [ClassSchedule]