from django.db import models
from django import forms
from django.db.models.fields import Field
from django.db.models.fields.related import ForeignKey
from django.forms.widgets import NumberInput
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


class HomePage(Page):
    max_count = 1
    table_count = 5
    day = _DAY
    time = _TIME

    def get_context(self, request):
        context = super().get_context(request)

        context['section_entries'] = Sections.objects.all()
        context['professor_entries'] = Professors.objects.all()
        context['room_entries'] = Rooms.objects.all()
        return context


class ProfessorOrderable(Orderable):
    room_model = ParentalKey(
        "home.Departments",
        related_name="professor_parental_key",
    )
    professor = models.ForeignKey(
        "accounts.Professors",
        on_delete=models.CASCADE,
        null=True
    )

    panels = [
        SnippetChooserPanel("professor"),
    ]


class RoomOrderable(Orderable):
    room_model = ParentalKey(
        "home.Departments",
        related_name="room_parental_key",
    )
    room = models.ForeignKey(
        "home.Rooms",
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("room"),
    ]


class SubjectsOrderable(Orderable):
    subject_model = ParentalKey(
        "home.Subjects", related_name="subject_parental_key", null=True)
    professor_model = ParentalKey("accounts.Professors",
                                  related_name="professor_parental_key", null=True)
    course_curriculum_model1 = ParentalKey("home.CourseCurriculum",
                                           related_name="first_year_first_sem", null=True)
    course_curriculum_model2 = ParentalKey("home.CourseCurriculum",
                                           related_name="first_year_second_sem", null=True)
    course_curriculum_model3 = ParentalKey("home.CourseCurriculum",
                                           related_name="second_year_first_sem", null=True)
    course_curriculum_model4 = ParentalKey("home.CourseCurriculum",
                                           related_name="second_year_second_sem", null=True)
    course_curriculum_model5 = ParentalKey("home.CourseCurriculum",
                                           related_name="third_year_first_sem", null=True)
    course_curriculum_model6 = ParentalKey("home.CourseCurriculum",
                                           related_name="third_year_second_sem", null=True)
    course_curriculum_model7 = ParentalKey("home.CourseCurriculum",
                                           related_name="fourth_year_first_sem", null=True)
    course_curriculum_model8 = ParentalKey("home.CourseCurriculum",
                                           related_name="fourth_year_second_sem", null=True)

    subject = models.ForeignKey(
        "home.Subjects",
        null=True,
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("subject"),
    ]


# class CollegeOrderable(Orderable):
#     department_model = ParentalKey(
#         "home.Departments", related_name="department_parental_key", null=True)

#     college = models.ForeignKey(
#         "home.Colleges",
#         null=True,
#         on_delete=models.CASCADE,
#         blank=False,
#     )

#     panels = [
#         SnippetChooserPanel("college")
#     ]


class DepartmentOrderable(Orderable):
    college_model = ParentalKey(
        "home.Colleges", related_name="college_parental_key", null=True)

    department = models.ForeignKey(
        "home.Departments",
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
        choices=[('Laboratory', 'Laboratory'), ('Lecture', 'Lecture')]
    )

    # sem = models.CharField(
    #     max_length=200,
    #     default='First',
    #     choices=[('First', 'First'), ('Second', 'Second')]
    # )

    hours = models.FloatField(default=1)

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
class CourseCurriculum(ClusterableModel, index.Indexed):
    course_name = models.CharField(
        max_length=300,
        null=True,
        help_text='Ex. CS33'
    )
    department = models.ForeignKey(
        "home.Departments",
        null=True,
        on_delete=models.CASCADE,
        help_text='Ex. Computer Studies'
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
            SnippetChooserPanel('department'),
            FieldPanel('curriculum_year'),
        ], heading='Primary Information'),
    ]

    first_year = [
        InlinePanel('first_year_first_sem',
                    label='Subject', min_num=1, max_num=10, heading="First Sem"),
        InlinePanel('first_year_second_sem',
                    label='Subject', min_num=1, max_num=10, heading="Second Sem"),
    ]
    second_year = [
        InlinePanel('second_year_first_sem',
                    label='Subject', min_num=1, max_num=10, heading="First Sem"),
        InlinePanel('second_year_second_sem',
                    label='Subject', min_num=1, max_num=10, heading="Second Sem"),
    ]
    third_year = [
        InlinePanel('third_year_first_sem',
                    label='Subject', min_num=1, max_num=10, heading="First Sem"),
        InlinePanel('third_year_second_sem',
                    label='Subject', min_num=1, max_num=10, heading="Second Sem"),
    ]
    fourth_year = [
        InlinePanel('fourth_year_first_sem',
                    label='Subject', min_num=1, max_num=10, heading="First Sem"),
        InlinePanel('fourth_year_second_sem',
                    label='Subject', min_num=1, max_num=10, heading="Second Sem"),
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
        'home.Colleges',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('Department_Name'),
        FieldPanel('Choose_College')
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


@register_snippet
class Professors(ClusterableModel, index.Indexed):
    global start_time

    def validate_start_time(value):
        global start_time
        start_time = value
        if value < datetime.time(7, 00, 00):
            time = timeConvert(value)
            raise ValidationError(
                _('%(time)s is invalid'),
                params={'time': time},
            )

    def validate_end_time(value):
        print(start_time, value)
        if value > datetime.time(19, 00, 00):
            time = timeConvert(value)
            raise ValidationError(
                _('%(time)s is invalid'),
                params={'time': time},
            )
        elif value <= start_time:
            raise ValidationError(
                _('End time must be greater than start time'),
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
        help_text='At least 7:00 A.M.',
        blank=True,
        validators=[validate_start_time],
        default=' 7:00 AM',
    )
    preferred_end_time = models.TimeField(
        auto_now=False,
        auto_now_add=False,
        null=True,
        help_text='At most 7:00 P.M.',
        blank=True,
        validators=[validate_end_time],
        default=' 7:00 PM',
    )

    def preferred_time(self):
        return str(timeConvert(self.preferred_start_time)) + " - " + str(timeConvert(self.preferred_end_time))

    status = models.CharField(
        max_length=200,
        default='Regular',
        choices=[('Regular', 'Regular'), ('Part-time', 'Part-time')]
    )

    choose_department = models.ForeignKey(
        'home.Departments',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+',
    )

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
                FieldPanel('preferred_end_time',),
            ],
            heading='Preferred Time',
        ),
        FieldPanel('status', widget=forms.RadioSelect),
        SnippetChooserPanel('choose_department'),
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
        "home.CourseCurriculum",
        null=True,
        on_delete=models.CASCADE,
        help_text='Ex. Computer Science'
    )

    department = models.ForeignKey(
        "home.Departments",
        null=True,
        on_delete=models.CASCADE,
        help_text='Ex. Computer Studies'
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
        SnippetChooserPanel('department'),
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
        "home.CourseCurriculum",
        null=True,
        on_delete=models.CASCADE,
        help_text='Ex. Computer Science'
    )

    search_fields = [
        index.SearchField('section_name'),
    ]

    panels = [
        FieldPanel('sem', widget=forms.RadioSelect),
        SnippetChooserPanel('course_curriculum'),
    ]

    first_year = models.IntegerField(
        blank=False, null=True, default=0)
    second_year = models.IntegerField(
        blank=False, null=True, default=0)
    third_year = models.IntegerField(
        blank=False, null=True, default=0)
    fourth_year = models.IntegerField(
        blank=False, null=True, default=0)

    ns_first_year = models.IntegerField(
        blank=False, null=True, default=0, verbose_name="First Year")
    ns_second_year = models.IntegerField(
        blank=False, null=True, default=0, verbose_name="Second Year")
    ns_third_year = models.IntegerField(
        blank=False, null=True, default=0, verbose_name="Third Year")
    ns_fourth_year = models.IntegerField(
        blank=False, null=True, default=0, verbose_name="Fourth Year")

    sections = [
        MultiFieldPanel([
            FieldPanel('first_year', widget=forms.NumberInput(
                attrs={'placeholder': '1st Year'})),
            FieldPanel('second_year', widget=forms.NumberInput(
                attrs={'placeholder': '2nd Year'})),
            FieldPanel('third_year', widget=forms.NumberInput(
                attrs={'placeholder': '3rd Year'})),
            FieldPanel('fourth_year', widget=forms.NumberInput(
                attrs={'placeholder': '4th Year'})),
        ], heading='Stem'),
        MultiFieldPanel([
            FieldPanel('ns_first_year', widget=forms.NumberInput(
                attrs={'placeholder': '1st Year'})),
            FieldPanel('ns_second_year', widget=forms.NumberInput(
                attrs={'placeholder': '2nd Year'})),
            FieldPanel('ns_third_year', widget=forms.NumberInput(
                attrs={'placeholder': '3rd Year'})),
            FieldPanel('ns_fourth_year', widget=forms.NumberInput(
                attrs={'placeholder': '4th Year'})),
        ], heading='Non-Stem'),
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
                section_name=self.course_curriculum.course_name + "-1" + chr(i+65), sem=self.sem, department_id=self.course_curriculum.department.pk, year_level="1st Year", course_curriculum_id=self.course_curriculum.pk)
            section.save()
        for i in range(self.second_year):
            section = Sections(
                section_name=self.course_curriculum.course_name + "-2" + chr(i+65), sem=self.sem, department_id=self.course_curriculum.department.pk, year_level="2nd Year", course_curriculum_id=self.course_curriculum.pk)
            section.save()
        for i in range(self.third_year):
            section = Sections(
                section_name=self.course_curriculum.course_name + "-3" + chr(i+65), sem=self.sem, department_id=self.course_curriculum.department.pk, year_level="3rd Year", course_curriculum_id=self.course_curriculum.pk)
            section.save()
        for i in range(self.fourth_year):
            section = Sections(
                section_name=self.course_curriculum.course_name + "-4" + chr(i+65), sem=self.sem, department_id=self.course_curriculum.department.pk, year_level="4th Year", course_curriculum_id=self.course_curriculum.pk)
            section.save()

        for i in range(self.ns_first_year):
            section = Sections(
                section_name=self.course_curriculum.course_name + "-NS-1" + chr(i+65), sem=self.sem, department_id=self.course_curriculum.department.pk, year_level="1st Year", course_curriculum_id=self.course_curriculum.pk)
            section.save()
        for i in range(self.ns_second_year):
            section = Sections(
                section_name=self.course_curriculum.course_name + "-NS-2" + chr(i+65), sem=self.sem, department_id=self.course_curriculum.department.pk, year_level="2nd Year", course_curriculum_id=self.course_curriculum.pk)
            section.save()
        for i in range(self.ns_third_year):
            section = Sections(
                section_name=self.course_curriculum.course_name + "-NS-3" + chr(i+65), sem=self.sem, department_id=self.course_curriculum.department.pk, year_level="3rd Year", course_curriculum_id=self.course_curriculum.pk)
            section.save()
        for i in range(self.ns_fourth_year):
            section = Sections(
                section_name=self.course_curriculum.course_name + "-NS-4" + chr(i+65), sem=self.sem, department_id=self.course_curriculum.department.pk, year_level="4th Year", course_curriculum_id=self.course_curriculum.pk)
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

    Room_Type = models.CharField(
        max_length=200,
        default='Lecture',
        choices=[('Laboratory', 'Laboratory'), ('Lecture', 'Lecture')]
    )

    search_fields = [
        index.SearchField('Room_Name'),
    ]

    panels = [
        FieldPanel('Room_Name'),
        FieldPanel('Room_Type', widget=forms.RadioSelect),
    ]

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

    def __str__(self):
        return self.college_name

    class Meta:
        verbose_name = 'College'
        verbose_name_plural = 'Colleges'
        ordering = [
            'college_name'
        ]


@ register_snippet
class StudentsAccount(models.Model):
    pass


@ register_snippet
class ProfessorsAccount(models.Model):
    pass


@ register_snippet
class AdminsAccount(models.Model):
    pass


@ register_snippet
class SectionsSchedule(models.Model):
    pass


@ register_snippet
class ProfessorsSchedule(models.Model):
    pass


@ register_snippet
class RoomsSchedule(models.Model):
    pass
