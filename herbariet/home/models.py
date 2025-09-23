from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey


class HomePage(Page):
    """Homepage - the root page of the site"""
    # Allow only PlantPage children to keep things simple.
    subpage_types = ["home.PlantPage"]

    # (Optional) You could add a simple panel later if you want content.
    pass


class Link(models.Model):
    """A simple model to store links for the homepage"""
    url = models.URLField()

    def __str__(self):
        return self.url


class PlantPage(Page):
    """Simple plant page where people can fill in plant data"""
    # Restrict where this page can live (only under HomePage) and prevent children.
    parent_page_types = ["home.HomePage"]
    subpage_types = []
    
    name = models.CharField(
        max_length=200, 
        help_text='Enter the plant name'
    )
    
    description = RichTextField(
        blank=True,
        help_text='Describe the plant'
    )
    
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Upload a photo of the plant'
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('description'),
        FieldPanel('image'),
        InlinePanel('links', label='Links'),
    ]

    class Meta:
        verbose_name = 'Plant Entry'
        verbose_name_plural = 'Plant Entries'


class PlantLink(Orderable):
    """Inline link item attached to a PlantPage, gives a clean repeatable form UI."""
    page = ParentalKey('home.PlantPage', related_name='links', on_delete=models.CASCADE)
    link_text = models.CharField(max_length=255, help_text='Label shown to users')
    url = models.URLField(help_text='Target URL')

    panels = [
        FieldPanel('link_text'),
        FieldPanel('url'),
    ]

    def __str__(self):
        return f"{self.link_text} -> {self.url}"
