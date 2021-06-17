from django.db import models
from django import forms
from django.db.models.fields import Field
from django.db.models.fields.related import ForeignKey
from django.forms.widgets import ChoiceWidget, NumberInput
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.http import HttpResponseRedirect

from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.search import index
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
    FieldRowPanel,
    ObjectList,
    TabbedInterface,
    PageChooserPanel
)

import datetime

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from TUPScheduling.accounts.models import Professors


class ProfessorOrderable(Orderable):
    room_model = ParentalKey(
        "base.Departments",
        related_name="professor_parental_key",
    )
    professor = models.ForeignKey(
        "accounts.Professors",
        on_delete=models.CASCADE,
        null=True,
        related_name='professor_orderable'
    )

    panels = [
        SnippetChooserPanel("professor"),
    ]


class RoomOrderable(Orderable):
    room_model = ParentalKey(
        "base.Departments",
        related_name="room_parental_key",
    )
    room = models.ForeignKey(
        "base.Rooms",
        null=True,
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("room"),
    ]


class SubjectsOrderable(Orderable):
    professor_model = ParentalKey("accounts.Professors",
                                  related_name="professor_parental_key", null=True)
    first_year_first_sem = ParentalKey("base.CourseCurriculum",
                                       related_name="first_year_first_sem", null=True)
    first_year_second_sem = ParentalKey("base.CourseCurriculum",
                                        related_name="first_year_second_sem", null=True)
    second_year_first_sem = ParentalKey("base.CourseCurriculum",
                                        related_name="second_year_first_sem", null=True)
    second_year_second_sem = ParentalKey("base.CourseCurriculum",
                                         related_name="second_year_second_sem", null=True)
    third_year_first_sem = ParentalKey("base.CourseCurriculum",
                                       related_name="third_year_first_sem", null=True)
    third_year_second_sem = ParentalKey("base.CourseCurriculum",
                                        related_name="third_year_second_sem", null=True)
    fourth_year_first_sem = ParentalKey("base.CourseCurriculum",
                                        related_name="fourth_year_first_sem", null=True)
    fourth_year_second_sem = ParentalKey("base.CourseCurriculum",
                                         related_name="fourth_year_second_sem", null=True)

    subject = models.ForeignKey(
        "base.Subjects",
        null=True,
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("subject"),
    ]


# class CollegeOrderable(Orderable):
#     department_model = ParentalKey(
#         "base.Departments", related_name="department_parental_key", null=True)

#     college = models.ForeignKey(
#         "base.Colleges",
#         null=True,
#         on_delete=models.CASCADE,
#         blank=False,
#     )

#     panels = [
#         SnippetChooserPanel("college")
#     ]


class DepartmentOrderable(Orderable):
    college_model = ParentalKey(
        "base.Colleges", related_name="college_parental_key", null=True)

    department = models.ForeignKey(
        "base.Departments",
        null=True,
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("department")
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
        default='Lecture',
        choices=[('Laboratory', 'Laboratory'), ('Lecture', 'Lecture')],
        verbose_name='Type',
    )

    # sem = models.CharField(
    #     max_length=200,
    #     default='First',
    #     choices=[('First', 'First'), ('Second', 'Second')]
    # )

    hours = models.FloatField(default=1)

    choose_department = models.ForeignKey(
        'base.Departments',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Department'
    )

    search_fields = [
        index.SearchField('subject_code'),
    ]

    panels = [
        MultiFieldPanel([
            FieldPanel('subject_code'),
            FieldPanel('description'),
        ], heading='Primary Information'),
        MultiFieldPanel([
            FieldPanel('units'),
            FieldPanel('hours'),
            FieldPanel('lab_or_lec', widget=forms.RadioSelect),
            # FieldPanel('sem', widget=forms.RadioSelect),
        ], heading='Secondary Information'),
        SnippetChooserPanel('choose_department'),
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
class CourseCurriculum(ClusterableModel, index.Indexed):
    course_name = models.CharField(
        max_length=300,
        null=True,
        help_text='Ex. Bachelor of Science in Computer Science'
    )

    course_abbreviation = models.CharField(
        max_length=10,
        null=True,
        help_text='Ex. BSCS'
    )

    choose_department = models.ForeignKey(
        'base.Departments',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="department"
    )

    curriculum_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(3000)],
        help_text="Use the following format: <YYYY> ex: 2012",
        null=True,
    )

    search_fields = [
        index.SearchField('course_name'),
    ]

    panels = [
        MultiFieldPanel([
            FieldPanel('course_name'),
            FieldPanel('course_abbreviation'),
            SnippetChooserPanel('choose_department'),
            FieldPanel('curriculum_year'),
        ], heading='Primary Information'),
    ]

    first_year = [
        InlinePanel(
            'first_year_first_sem',
            label='Subject',
            min_num=1,
            max_num=15,
            heading="First Sem"
        ),
        InlinePanel(
            'first_year_second_sem',
            label='Subject',
            min_num=1,
            max_num=15,
            heading="Second Sem"
        ),
    ]
    second_year = [
        InlinePanel(
            'second_year_first_sem',
            label='Subject',
            min_num=1,
            max_num=15,
            heading="First Sem"
        ),
        InlinePanel(
            'second_year_second_sem',
            label='Subject',
            min_num=1,
            max_num=15,
            heading="Second Sem"
        ),
    ]

    third_year = [
        InlinePanel(
            'third_year_first_sem',
            label='Subject',
            min_num=1,
            max_num=15,
            heading="First Sem"
        ),
        InlinePanel(
            'third_year_second_sem',
            label='Subject',
            min_num=1,
            max_num=15,
            heading="Second Sem"
        ),
    ]
    fourth_year = [
        InlinePanel(
            'fourth_year_first_sem',
            label='Subject',
            min_num=1,
            max_num=15,
            heading="First Sem"
        ),
        InlinePanel(
            'fourth_year_second_sem',
            label='Subject',
            min_num=1,
            max_num=15,
            heading="Second Sem"
        ),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(panels, heading='Main'),
            ObjectList(first_year, heading='1st Year'),
            ObjectList(second_year, heading='2nd Year'),
            ObjectList(third_year, heading='3rd Year'),
            ObjectList(fourth_year, heading='4th Year'),
        ]
    )

    def __str__(self):
        return self.course_name

    class Meta:
        verbose_name = 'Course Curriculum'
        verbose_name_plural = 'Course Curriculum'
        ordering = [
            'course_name'
        ]


@register_snippet
class Departments(ClusterableModel, index.Indexed):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(Department_Name='asdksajd')

    def get_context(self, request):
        context = super().get_context(request)
        colleges = Colleges.objects.all()
        college_list = []

        for college in colleges:
            college_list.append((college.college_name, college.college_name))
        self.Department_name.choices = college_list

        return context

    Department_Name = models.CharField(
        max_length=100,
        null=True,
        help_text='Department of Mathematics'
    )

    Choose_College = models.ForeignKey(
        'base.Colleges',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="College"
    )

    panels = [
        FieldPanel('Department_Name'),
        SnippetChooserPanel('Choose_College')
    ]
    search_fields = [
        index.SearchField('Department_Name'),
    ]

    def __str__(self): return self.Department_Name

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        ordering = [
            'Department_Name'
        ]


def timeConvert(miliTime):
    hours = miliTime.strftime('%H')
    minutes = miliTime.strftime('%M')
    hours, minutes = int(hours), int(minutes)
    setting = " A.M."
    if hours > 12:
        setting = " P.M."
        hours -= 12
    return(("%02d:%02d" + setting) % (hours, minutes))


class MyFieldPanel(SnippetChooserPanel):

    def on_form_bound(self) -> None:
        super().on_form_bound()


"""Single Section"""


@register_snippet
class Sections(models.Model, index.Indexed):
    section_name = models.CharField(
        max_length=30,
        null=True,
        help_text='Ex. BSCS-3A-NS'
    )

    year_level = models.CharField(
        max_length=200,
        default='First',
        choices=[('1st Year', '1st Year'), ('2nd Year', '2nd Year'),
                 ('3rd Year', '3rd Year'), ('4th Year', '4th Year')]
    )

    sem = models.CharField(
        max_length=200,
        default='First',
        choices=[('First', 'First'), ('Second', 'Second')]
    )

    course_curriculum = models.ForeignKey(
        "base.CourseCurriculum",
        null=True,
        on_delete=models.CASCADE,
        help_text='Ex. Computer Science'
    )

    search_fields = [
        index.SearchField('section_name'),
    ]

    panels = [
        FieldPanel('section_name'),
        MultiFieldPanel(
            [
                FieldPanel('year_level', widget=forms.RadioSelect),
                FieldPanel('sem', widget=forms.RadioSelect),
            ],
            heading="Section Info",
        ),
        SnippetChooserPanel('course_curriculum'),
    ]

    def __str__(self):
        return self.section_name

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)  # Call the "real" save() method.
    #     print(Sections.objects.all())

    class Meta:
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'
        ordering = [
            'section_name'
        ]


"""Bulk Section"""


@register_snippet
class BulkSections(models.Model, index.Indexed):
    sem = models.CharField(
        max_length=200,
        default='First',
        choices=[('First', 'First'), ('Second', 'Second')]
    )

    course_curriculum = models.ForeignKey(
        "base.CourseCurriculum",
        null=True,
        on_delete=models.CASCADE,
        help_text='Ex. Computer Science'
    )

    search_fields = [
        index.SearchField('section_name'),
    ]

    panels = [
        SnippetChooserPanel('course_curriculum'),
        FieldPanel('sem', widget=forms.RadioSelect),
    ]

    first_year = models.IntegerField(
        blank=False, null=True, default=0)
    second_year = models.IntegerField(
        blank=False, null=True, default=0)
    third_year = models.IntegerField(
        blank=False, null=True, default=0)
    fourth_year = models.IntegerField(
        blank=False, null=True, default=0)

    sections = [
        FieldPanel('first_year', widget=forms.NumberInput(
            attrs={'placeholder': '1st Year'})),
        FieldPanel('second_year', widget=forms.NumberInput(
            attrs={'placeholder': '2nd Year'})),
        FieldPanel('third_year', widget=forms.NumberInput(
            attrs={'placeholder': '3rd Year'})),
        FieldPanel('fourth_year', widget=forms.NumberInput(
            attrs={'placeholder': '4th Year'})),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(panels, heading='Main'),
            ObjectList(sections, heading='Number of Sections'),
        ]
    )

    def __str__(self):
        return self.course_curriculum.course_name

    def save(self, *args, **kwargs):
        Sections.objects.filter(
            course_curriculum_id=self.course_curriculum.pk).delete()

        for i in range(self.first_year):
            section = Sections(
                section_name=self.course_curriculum.course_abbreviation + "-1" + chr(i+65), year_level="1st Year", sem=self.sem, course_curriculum_id=self.course_curriculum.pk)
            section.save()
        for i in range(self.second_year):
            section = Sections(
                section_name=self.course_curriculum.course_abbreviation + "-2" + chr(i+65), year_level="2nd Year", sem=self.sem,  course_curriculum_id=self.course_curriculum.pk)
            section.save()
        for i in range(self.third_year):
            section = Sections(
                section_name=self.course_curriculum.course_abbreviation + "-3" + chr(i+65), year_level="3rd Year", sem=self.sem,  course_curriculum_id=self.course_curriculum.pk)
            section.save()
        for i in range(self.fourth_year):
            section = Sections(
                section_name=self.course_curriculum.course_abbreviation + "-4" + chr(i+65), year_level="4th Year", sem=self.sem,  course_curriculum_id=self.course_curriculum.pk)

            section.save()

    class Meta:
        verbose_name = 'Bulk Section'
        verbose_name_plural = 'Bulk Section'
        ordering = [
            'course_curriculum__course_name'
        ]


@ register_snippet
class Rooms(models.Model, index.Indexed):
    Room_Name = models.CharField(
        max_length=20,
        null=True,
        help_text='Ex. Room101'
    )

    room_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    floor = models.IntegerField(
        choices=[
            (1,'1st Floor'),
            (2,'2nd Floor'),
            (3,'3rd Floor'),
            (4,'4th Floor'),
            (5,'5th Floor'),
        ],
        default=1
    )

    Room_Type = models.CharField(
        max_length=200,
        default='Lecture',
        choices=[('Laboratory', 'Laboratory'), ('Lecture', 'Lecture')]
    )

    choose_department = models.ForeignKey(
        'base.Departments',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="department"
    )

    search_fields = [
        index.SearchField('Room_Name'),
    ]

    panels = [
        FieldPanel('Room_Name'),
        FieldPanel('Room_Type', widget=forms.RadioSelect),
        FieldPanel('floor'),
        SnippetChooserPanel('choose_department'),
        ImageChooserPanel('room_image'),
    ]

    @property
    def room_image_display(self):
        # Returns an empty string if there is no profile pic or the rendition
        # file can't be found.
        try:
            return self.room_image.get_rendition('fill-150x150').img_tag()
        except:  # noqa: E722 FIXME: remove bare 'except:'
            return ''


    def __str__(self): return self.Room_Name + "  " + self.Room_Type

    class Meta:
        verbose_name = 'Rooms'
        verbose_name_plural = 'Rooms'
        ordering = [
            'Room_Name'
        ]


@ register_snippet
class Colleges(ClusterableModel, index.Indexed):
    college_name = models.CharField(
        max_length=300,
        null=True,
    )

    panels = [
        FieldPanel('college_name'),

    ]
    
    def acronym(self):
        return "".join(e[0] for e in self.college_name.split())

    def __str__(self):
        return self.college_name

    class Meta:
        verbose_name = 'College'
        verbose_name_plural = 'Colleges'
        ordering = [
            'college_name'
        ]

class BasePage(Page):
    max_count = 1
    def serve(self, request):
        if request.user.is_authenticated is False:
            return HttpResponseRedirect('/logout/')
        if request.user.is_superuser:
            return HttpResponseRedirect('/admin/')
        if request.user.is_student:
            return HttpResponseRedirect('/class-schedule/')
        if request.user.is_professor:
            if request.user.professors.is_scheduler:
                return HttpResponseRedirect('/schedule/')
            return HttpResponseRedirect('/class-schedule/')

        return HttpResponseRedirect('/logout/')

