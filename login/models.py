from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import (
    FieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.images.edit_handlers import ImageChooserPanel

from TUPScheduling import Strings

# Create your models here.
class LoginPage(Page):
    carousel_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="For best fit, please choose a size of 772x667",
    )

    over_view = Page.content_panels + [
        ImageChooserPanel('carousel_image')
    ] 

    edit_handler = TabbedInterface(
        [
            ObjectList(over_view, heading=Strings.overview),
            # This is our custom banner_panels. It's just a list, how easy!
            ObjectList(Page.promote_panels, heading='Promote'),
            ObjectList(Page.settings_panels, heading='Settings'),
        ]
    )
