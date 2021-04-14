from django.db import models
from django import forms

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
)
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.snippets.models import register_snippet
from wagtail.search import index

class SubjectsOrderable(Orderable):
    model = ParentalKey("home.Subjects", related_name="subject_parental_key")
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
        choices=[('Laboratory','Laboratory'),('Lecture', 'Lecture')]
    )

    sem = models.CharField(
        max_length=200,
        default='First',
        choices=[('First','First'),('Second', 'Second')]
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
            InlinePanel('subject_parental_key', label='Subject', min_num=0, max_num=4)
        ], heading = 'Prerequisite')
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
class Students(models.Model):
    pass

@register_snippet
class Professors(models.Model):
    pass

class HomePage(Page):
    max_count = 1
    pass

class LoginPage(Page):
    pass