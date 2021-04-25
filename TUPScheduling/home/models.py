from django.db import models
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
    FieldRowPanel
)
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.search import index

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from django.core.validators import MinValueValidator, MaxValueValidator


import datetime

class ProfessorOrderable(Orderable):
    room_model = ParentalKey(
        "home.Departments",
        related_name="professor_parental_key",
    )
    professor = models.ForeignKey(
        "home.Professors", 
        on_delete=models.CASCADE,
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
    professor_model = ParentalKey("home.Professors",
                                  related_name="professor_parental_key", null=True)
    course_curriculum_model = ParentalKey("home.CourseCurriculum",
                                  related_name="course_curriculum_parental_key", null=True)


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
        MultiFieldPanel([
            FieldPanel('subject_code'),
            FieldPanel('description'),
        ], heading='Subject Primary Information'),
        MultiFieldPanel([
            FieldPanel('units'),
            FieldPanel('hours'),
            FieldPanel('lab_or_lec', widget=forms.RadioSelect),
            FieldPanel('sem', widget=forms.RadioSelect),
        ], heading='Subject Secondary Information'),
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

    college = models.ForeignKey(
        "home.Colleges",
        null = True,
        on_delete=models.CASCADE,
        help_text='Ex. COS or College of Science'
    )

    department = models.ForeignKey(
        "home.Departments",
        null = True,
        on_delete=models.CASCADE,
        help_text='Ex. Computer Studies'
    )
    starting_year = models.PositiveIntegerField(
            validators=[ MinValueValidator(1900), MaxValueValidator(3000)],
            help_text="Use the following format: <YYYY> ex: 2012",
            null=True,
        )
    
    ending_year = models.PositiveIntegerField(
            validators=[ MinValueValidator(1900), MaxValueValidator(3000)],
            help_text="Use the following format: <YYYY> ex: 2012",
            null=True,
        )

    search_fields = [
        index.SearchField('course_name'),
    ]

    panels = [
        MultiFieldPanel([
            FieldPanel('course_name'),
            SnippetChooserPanel('college'),
            SnippetChooserPanel('department'),
            FieldRowPanel([
                FieldPanel('starting_year'),
                FieldPanel('ending_year'),
            ], heading='YEAR'),
        ], heading='Course Curriculumn Primary Information'),
        
        MultiFieldPanel([
            InlinePanel('course_curriculum_parental_key',
                        label='Subject', min_num=0, max_num=10)
        ], heading='COURSE SUBJECT')
    ]

    def __str__(self):
        return self.course_name
    
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
class Sections(models.Model, index.Indexed):
    section_name = models.CharField(
        max_length=30,
        null=True,
        help_text='Ex. BSCS-3A-NS'
    )

    year_level = models.CharField(
        max_length=200,
        default='First',
        choices=[('1st Year', '1st Year'), ('2nd Year', '2nd Year'), ('3rd Year','3rd Year'), ('4th Year','4th Year')]
    )   

    sem = models.CharField(
        max_length=200,
        default='First',
        choices=[('First', 'First'), ('Second', 'Second')]
    )

    course_curriculum = models.ForeignKey(
        "home.CourseCurriculum",
        null = True,
        on_delete=models.CASCADE,
        help_text='Ex. Computer Science'
    )

    college = models.ForeignKey(
        "home.Colleges",
        null = True,
        on_delete=models.CASCADE,
        help_text='Ex. COS or College of Science'
    )

    department = models.ForeignKey(
        "home.Departments",
        null = True,
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
            heading="College Info",
        ),
        SnippetChooserPanel('course_curriculum'),
        SnippetChooserPanel('college'),
        SnippetChooserPanel('department'),
    ]
    
    def __str__(self):
        return self.section_name
    
    class Meta:
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'
        ordering = [
            'section_name'
        ]

@register_snippet
class Rooms(models.Model, index.Indexed):
    Room_Name = models.CharField(
        max_length=20,
        null=True,
        help_text='Ex. CS33'
    )

    Room_Type = models.CharField(
        max_length=50,
        default='Lecture',
        choices=[('Laboratory', 'Laboratory'), ('Lecture', 'Lecture')]
    )

    search_fields = [
        index.SearchField('Room_Name'),
    ]

    panels = [
        FieldPanel('Room_Name'),
        FieldPanel('Room_Type'),        
    ]

    def __str__(self): return self.Room_Name + "  " + self.Room_Type

    class Meta:
        verbose_name = 'Rooms'
        verbose_name_plural = 'Rooms'
        ordering = [
            'Room_Name'
        ]

@register_snippet
class Departments(ClusterableModel, index.Indexed):

    Department_Name = models.CharField(
        max_length=100,
        null=True,
        help_text='Department of Mathematics'
    )

    panels = [
        FieldPanel('Department_Name'),
        MultiFieldPanel([
            MultiFieldPanel(
            [
                InlinePanel("room_parental_key", label="Room", min_num=1,help_text="Add Rooms to Department")
            ],
            heading="Rooms"
            ),       
            MultiFieldPanel(
                [
                    InlinePanel("professor_parental_key", label="Professors", min_num=1,help_text="Add Professors to Department")
                ],
                heading="Professors"
            ),
        ],heading="Properties"),
        
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


@register_snippet
class Colleges(models.Model):
    college_name = models.CharField(
        max_length=300,
        null=True,
    )

    panels = [
        FieldPanel('college_name'),
        # MultiFieldPanel([
        #     InlinePanel('department_parental_key',
        #                 label='Subject', min_num=1, max_num=10)
        # ], heading='Departments under this college')
    ]

    def __str__(self):
        return self.college_name
    

    class Meta:
        verbose_name = 'College'
        verbose_name_plural = 'Colleges'
        ordering = [
            'college_name'
        ]


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
