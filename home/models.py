from django.db import models
from django import forms
from django.db.models.fields import Field
from django.db.models.fields.related import ForeignKey
from django.forms.widgets import ChoiceWidget, NumberInput
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
    FieldRowPanel,
    ObjectList,
    TabbedInterface,
    PageChooserPanel
)

from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.search import index

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from django.core.validators import MinValueValidator, MaxValueValidator

import datetime
from .__init__ import _DAY, _TIME
from accounts.models import Professors

from django.http import HttpResponseRedirect


class HomePage(Page):
    max_count = 1

    def serve(self, request):
        return HttpResponseRedirect('/class-schedule/')
