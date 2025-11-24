from wagtail import hooks
from wagtail.admin.widgets import Button


@hooks.register('register_page_header_buttons')
def add_frontend_link_button(page, user=None, next_url=None, **kwargs):
    """Add a button in the page header to view the frontend URL"""
    # Only show for PlantPage instances that have been saved
    if page.__class__.__name__ == 'PlantPage' and page.id and page.slug:
        frontend_url = f"https://herbariet.dh.gu.se/plants/{page.slug}"
        yield Button(
            label='View on Frontend',
            url=frontend_url,
            icon_name='site',
            attrs={'target': '_blank', 'title': f'Open {frontend_url}'},
            priority=10
        )
