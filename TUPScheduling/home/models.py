from django.db import models
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
)
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.search import index

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

import datetime


class SubjectsOrderable(Orderable):
    subject_model = ParentalKey(
        "home.Subjects", related_name="subject_parental_key")
    professor_model = ParentalKey("home.Professors",
                                  related_name="professor_parental_key")
    subject = models.ForeignKey(
        "home.Subjects",
        null=True,
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("subject"),
    ]


@register_snippet
class Subjects(ClusterableModel, index.Indexed):
    subject_code = models.CharField(
        max_length=200,
        null=True,
        help_text='Ex. CS33'
    )

    description = models.CharField(
        max_length=200,
        null=True,
    )
    units = models.IntegerField(default=1)

    lab_or_lec = models.CharField(
        max_length=200,
        default='Laboratory',
        choices=[('Laboratory', 'Laboratory'), ('Lecture', 'Lecture')]
    )

    sem = models.CharField(
        max_length=200,
        default='First',
        choices=[('First', 'First'), ('Second', 'Second')]
    )

    hours = models.FloatField(default=1)

    search_fields = [
        index.SearchField('subject_code'),
    ]

    panels = [
        FieldPanel('subject_code'),
        FieldPanel('description'),
        FieldPanel('units'),
        FieldPanel('lab_or_lec', widget=forms.RadioSelect),
        FieldPanel('sem', widget=forms.RadioSelect),
        FieldPanel('hours'),
        MultiFieldPanel([
            InlinePanel('subject_parental_key',
                        label='Subject', min_num=0, max_num=4)
        ], heading='Prerequisite')
    ]

    def __str__(self):
        return self.subject_code

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
        ordering = [
            'subject_code'
        ]


@register_snippet
class CourseCurriculum(ClusterableModel):
    course_name = models.CharField(
        max_length=300,
        null=True,
        help_text='Ex. CS33'
    )
    course_date = models.DateField()

    # subjects = ParentalManyToManyField(
    #     'home.Subjects',
    #     blank=True,
    # )

    panels = [
        FieldPanel('course_name'),
        FieldPanel('course_date'),
        # FieldPanel('subjects',widget=forms.CheckboxSelectMultiple),
    ]

    class Meta:
        verbose_name = 'Course Curriculum'
        verbose_name_plural = 'Course Curriculum'
        ordering = [
            'course_name'
        ]


@register_snippet
class Professors(ClusterableModel, index.Indexed):
    global start_time

    def validate_start_time(value):
        global start_time
        start_time = value
        if value < datetime.time(7, 00, 00):
            raise ValidationError(
                _('%(value)s is invalid'),
                params={'value': value},
            )

    def validate_end_time(value):
        print(start_time, value)
        if value > datetime.time(19, 00, 00):
            raise ValidationError(
                _('%(value)s is invalid'),
                params={'value': value},
            )
        elif value <= start_time:
            raise ValidationError(
                _('end time must be greater than start time'),
            )

    first_name = models.CharField(
        max_length=300,
        null=True,
        help_text='Ex. John'
    )
    middle_name = models.CharField(
        max_length=300,
        null=True,
        help_text='Ex. Michael'
    )
    last_name = models.CharField(
        max_length=300,
        null=True,
        help_text='Ex. Doe'
    )

    def full_name(self):
        return self.last_name + ", " + self.first_name + " " + self.middle_name[0] + "."

    preferred_start_time = models.TimeField(
        auto_now=False,
        auto_now_add=False,
        null=True,
        help_text='At least 7:00',
        blank=True,
        validators=[validate_start_time],
    )
    preferred_end_time = models.TimeField(
        auto_now=False,
        auto_now_add=False,
        null=True,
        help_text='At most 19:00',
        blank=True,
        validators=[validate_end_time],
    )

    def preferred_time(self):
        return str(self.preferred_start_time) + " - " + str(self.preferred_end_time)

    status = models.CharField(
        max_length=200,
        default='Regular',
        choices=[('Regular', 'Regular'), ('Part-time', 'Part-time')]
    )

    search_fields = [
        index.SearchField('subject_code'),
    ]

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('first_name'),
                FieldPanel('middle_name'),
                FieldPanel('last_name'),
            ],
            heading="Full Name",
        ),
        MultiFieldPanel(
            [
                FieldPanel('preferred_start_time',),
                FieldPanel('preferred_end_time'),
            ],
            heading='Preferred Time',
        ),
        FieldPanel('status', widget=forms.RadioSelect),
        MultiFieldPanel([
            InlinePanel('professor_parental_key',
                        label='Subject', min_num=1, max_num=4)
        ], heading='Preferred Subjects')
    ]

    def __str__(self):
        return self.last_name

    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professors'
        ordering = [
            'last_name'
        ]


@register_snippet
class Sections(models.Model):
    pass


@register_snippet
class Rooms(models.Model):
    pass


@register_snippet
class Departments(models.Model):
    pass


@register_snippet
class Colleges(models.Model):
    pass


@register_snippet
class StudentsAccount(models.Model):
    pass


@register_snippet
class ProfessorsAccount(models.Model):
    pass


@register_snippet
class AdminsAccount(models.Model):
    pass


@register_snippet
class SectionsSchedule(models.Model):
    pass


@register_snippet
class ProfessorsSchedule(models.Model):
    pass


@register_snippet
class RoomsSchedule(models.Model):
    pass


class HomePage(Page):
    max_count = 1
    pass


class LoginPage(Page):
    pass
