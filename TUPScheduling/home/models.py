from django.db import models
from django import forms

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import (
    FieldPanel,
)
from modelcluster.fields import ParentalManyToManyField
from modelcluster.models import ClusterableModel


class Subjects(ClusterableModel):
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
        choices=[('Laboratory','Laboratory'),('Lecture', 'Lecture')]
    )

    sem = models.CharField(
        max_length=200,
        default='First',
        choices=[('First','First'),('Second', 'Second')]
    )

    prerequisites = ParentalManyToManyField(
        'home.Subjects',
        blank=True,
    )

    hours = models.FloatField(default=1)


    panels = [
        FieldPanel('subject_code'),
        FieldPanel('description'),
        FieldPanel('units'),
        FieldPanel('lab_or_lec', widget=forms.RadioSelect),
        FieldPanel('sem', widget=forms.RadioSelect),
        FieldPanel('hours'),
        FieldPanel('prerequisites',widget=forms.CheckboxSelectMultiple),
    ]

    def __str__(self):
        return self.subject_code

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
        ordering = [
            'subject_code'
        ]
    


class CourseCurriculum(ClusterableModel):
    course_name = models.CharField(
        max_length=300,
        null=True,
        help_text='Ex. CS33'
    )
    course_date = models.DateField()

    subjects = ParentalManyToManyField(
        'home.Subjects',
        blank=True,
    )

    panels = [
        FieldPanel('course_name'),
        FieldPanel('course_date'),
        FieldPanel('subjects',widget=forms.CheckboxSelectMultiple),
    ]

    class Meta:
        verbose_name = 'Course Curriculum'
        verbose_name_plural = 'Course Curriculum'
        ordering = [
            'course_name'
        ]



class HomePage(Page):
    pass
