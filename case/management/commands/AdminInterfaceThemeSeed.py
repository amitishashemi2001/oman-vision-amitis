from admin_interface.models import Theme
from django.core.management.base import BaseCommand
from django.db import connection
from sys import stdout


class Command(BaseCommand):
    def handle(self, *args, **options):
        flush_table(Theme)
        create_theme()

def flush_table(model):
    stdout.write('Flushing data from Admin Interface Theme table...\n')
    table_name = model._meta.db_table
    with connection.cursor() as cursor:
        cursor.execute(f'TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE')

def create_theme():
    stdout.write("Creating Admin Interface Theme....\n")
    Theme.objects.create(
        name="Default Theme",
        active=True,
        title="عمان ویژن",
        title_visible=True,
        logo="admin-interface/logo/oman-vision.png",
        logo_visible=True,
        css_header_background_color="#1B7D4B",
        title_color="#FFFFFF",
        css_header_text_color="#FFFFFF",
        css_header_link_color="#FFFFFF",
        css_header_link_hover_color="#00FFFE",
        css_module_background_color="#15613A",
        css_module_text_color="#FFFFFF",
        css_module_link_color="#FFFFFF",
        css_module_link_hover_color="#A1FFB3",
        css_module_rounded_corners=True,
        css_generic_link_color="#222222",
        css_generic_link_hover_color="#2C9962",
        css_save_button_background_color="#15613A",
        css_save_button_background_hover_color="#44B78B",
        css_save_button_text_color="#FFFFFF",
        css_delete_button_background_color="#D10620",
        css_delete_button_background_hover_color="#A41515",
        css_delete_button_text_color="#FFFFFF",
        list_filter_dropdown=True,
        related_modal_active=True,
        related_modal_background_color="#000000",
        related_modal_rounded_corners=True,
        logo_color='#FFFFFF',
        recent_actions_visible=True,
        favicon='admin-interface/favicon/oman-vision.png',
        related_modal_background_opacity="0.3",
        env_name='مدیریت',
        env_visible_in_header=True,
        env_color='#FF0000',
        env_visible_in_favicon=True,
        related_modal_close_button_visible=True,
        language_chooser_active=True,
        language_chooser_display='code',
        list_filter_sticky=True,
        form_pagination_sticky=False,
        form_submit_sticky=True,
        css_module_background_selected_color="#DAFFE6",
        css_module_link_selected_color="#FFFFFF",
        logo_max_height="48",
        logo_max_width="48",
        foldable_apps=True,
        language_chooser_control='default-select',
        list_filter_highlight=True,
        list_filter_removal_links=False,
        show_fieldsets_as_tabs=False,
        show_inlines_as_tabs=False,
        css_generic_link_active_color="#29B864",
        collapsible_stacked_inlines=False,
        collapsible_stacked_inlines_collapsed=True,
        collapsible_tabular_inlines=False,
        collapsible_tabular_inlines_collapsed=True,
    )
