from django.db import models
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group

from modelcluster.models import ClusterableModel

from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.search import index 
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
    InlinePanel
)


import datetime

def timeConvert(miliTime):
    hours = miliTime.strftime('%H')
    minutes = miliTime.strftime('%M')
    hours, minutes = int(hours), int(minutes)
    setting = " A.M."
    if hours > 12:
        setting = " P.M."
        hours -= 12
    return(("%02d:%02d" + setting) % (hours, minutes))


class BaseAccount(ClusterableModel, index.Indexed):
    
    first_name = models.CharField(
        max_length=300,
        null=True,
        help_text='Ex. John'
    )
    middle_name = models.CharField(
        max_length=1,
        null=True,
        help_text='Ex. Michael'
    )
    last_name = models.CharField(
        max_length=300,
        null=True,
        help_text='Ex. Doe'
    )
    section = models.ForeignKey(
        'base.Sections',
        on_delete=models.SET_NULL,
        null=True,
    )
    
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def user_code(self, extra_count):
        user_pk = self.pk
        year = year = str(self.created_at.year - 2000)

        return 'TUPM' + '-' + year + '-' + str(user_pk + extra_count)  

    basic_info_panel = [
        MultiFieldPanel([
            FieldPanel('first_name', heading='Enter First Name here'),
            FieldPanel('middle_name', heading='Enter Middle Name here'),
            FieldPanel('last_name', heading='Enter Last Name here'),
        ], heading='FULL NAME'),
    ]

    def full_name(self):
        return self.last_name + ", " + self.first_name + " " + self.middle_name + "."

    class Meta:
        abstract = True


@register_snippet
class Students(BaseAccount):

    panels = BaseAccount.basic_info_panel + [
        SnippetChooserPanel('section', heading='Pick what section'),
    ]

    def __str__(self):
        return self.full_name()

    class Meta:
        verbose_name='Student'
        verbose_name_plural ='Students'

    
    def save(self):
        from users.models import User
        super().save()
        user = User.objects.create_user(
            username=self.user_code(extra_count=3000),
            first_name= self.first_name,
            last_name= self.last_name,
            password=self.last_name.upper(),
            student=self,
            email=self.first_name + '.' + self.last_name + '@tup.edu.ph',
        )

        
            
        group = Group.objects.get(name='Student')
        group.user_set.add(user)
        
        

@register_snippet
class Professors(BaseAccount):
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
        'base.Departments',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    scheduling_panel = [
        MultiFieldPanel(
            [
                FieldPanel('preferred_start_time',),
                FieldPanel('preferred_end_time',),
            ],
            heading='Preferred Time',
        ),
        FieldPanel('status', widget=forms.RadioSelect),
        FieldPanel('choose_department'),
    ]

    subject_panel = [
        MultiFieldPanel([
            InlinePanel('professor_parental_key',
                        label='Subject', min_num=1, max_num=4)
        ], heading='Preferred Subjects')
    ]


    edit_handler = TabbedInterface(
        [
            ObjectList(BaseAccount.basic_info_panel, heading='Profesor Info'),
            ObjectList(scheduling_panel, heading="Scheduling Requirements"),
            ObjectList(subject_panel, heading="Subjects"),
        ]
    )


    def __str__(self):
        return self.full_name()
    
    
    def save(self):
        from users.models import User
        super().save()

        user = User.objects.create_user(
            username=self.user_code(extra_count=5000),
            first_name= self.first_name,
            last_name= self.last_name,
            password=self.last_name.upper(),
            professor=self,
            email=self.first_name + '.' + self.last_name + '@tup.edu.ph',
        )

        
            
        group = Group.objects.get(name='Professor')
        group.user_set.add(user)
        

    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professors'
        ordering = [
            'last_name'
        ]
