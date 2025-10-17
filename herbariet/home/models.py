from django.db import models
from django.core.exceptions import ValidationError
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

    # Add type field that can be chosen from specific options:
    # History
    # Biology
    # Research

    choices = [
        ('history', 'History'),
        ('biology', 'Biology'),
        ('research', 'Research'),
    ]
    type = models.CharField(
        max_length=20,
        choices=choices,
        default='biology',
        help_text='Select the type of plant information'
    )

    image = models.ImageField(
        upload_to='plants/',
        null=False,
        blank=False,
        help_text='Upload a photo of the plant (required)'
    )

    qrcode = models.ImageField(
        upload_to='qrcodes/',
        null=True,
        blank=True,
        max_length=255,  # Increase from default 100
        help_text='Upload a QR code image for the plant'
    )

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('type'),
        FieldPanel('description'),
        FieldPanel('image'),
        InlinePanel('links', label='Links', max_num=3),
        FieldPanel('qrcode'),
    ]

    def __str__(self):
        return self.name
    
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
