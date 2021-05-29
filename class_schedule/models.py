from django.db import models
from wagtail.core.models import Page


class ClassSchedule(Page):
    parent_page_types = ["home.HomePage"]

class ClassScheduleOverview(Page):
    pass