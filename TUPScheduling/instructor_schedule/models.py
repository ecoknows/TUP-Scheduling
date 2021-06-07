from django.db import models
from wagtail.core.models import Page
from TUPScheduling.base.models import BasePage

class InstructorSchedule(Page):
    max_count = 1
    parent_page_types = [BasePage]