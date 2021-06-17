from django.db import models
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
from django.utils.translation import gettext as _

from modelcluster.models import ClusterableModel
from wagtail.images.edit_handlers import ImageChooserPanel


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

from TUPScheduling.users.models import User

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

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True
    )

    first_name = models.CharField(
        max_length=300,
        null=True,
        help_text='Ex. John'
    )
    middle_name = models.CharField(
        max_length=1,
        null=True,
        help_text='Ex. M',
        verbose_name='middle initial'
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
            FieldPanel('middle_name', heading='Enter Middle Initial here'),
            FieldPanel('last_name', heading='Enter Last Name here'),
        ], heading='FULL NAME'),
    ]

    def full_name(self):
        return self.last_name + ", " + self.first_name + " " + self.middle_name + "."

    def delete(self):
        if self.user:
            self.user.delete()
        return super().delete()

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
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


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

    profile_picture = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
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

    units = models.IntegerField(default=0)

    status = models.CharField(
        max_length=200,
        default='Regular',
        choices=[('Regular', 'Regular'), ('Part-time', 'Part-time')]
    )

    choose_department = models.ForeignKey(
        'base.Departments',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    BaseAccount.basic_info_panel = BaseAccount.basic_info_panel + [
        ImageChooserPanel('profile_picture')
    ]

    @property
    def profile_image(self):
        # Returns an empty string if there is no profile pic or the rendition
        # file can't be found.
        try:
            return self.profile_picture.get_rendition('fill-50x50').img_tag()
        except:  # noqa: E722 FIXME: remove bare 'except:'
            return ''

    scheduling_panel = [
        MultiFieldPanel(
            [
                FieldPanel('preferred_start_time',),
                FieldPanel('preferred_end_time',),
            ],
            heading='Preferred Time',
        ),
        FieldPanel('status', widget=forms.RadioSelect),
        SnippetChooserPanel('choose_department'),
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

    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professors'
        ordering = [
            'last_name'
        ]
