from django.db import models
from wagtail.core.models import Page


class ClassSchedule(Page):
    max_count = 1
    parent_page_types = ["home.HomePage"]

class ClassScheduleOverview(Page):  
    max_count = 1
    parent_page_types = ["home.HomePage"]