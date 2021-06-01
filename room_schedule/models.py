from django.db import models
from wagtail.core.models import Page


class RoomSchedule(Page):
    max_count = 1
    parent_page_types = ["home.HomePage"]