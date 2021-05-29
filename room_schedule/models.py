from django.db import models
from wagtail.core.models import Page


class RoomSchedule(Page):
    
    parent_page_types = ["home.HomePage"]