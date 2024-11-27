"""
Source of code : Boutiqueado walkthrought.

Refactored for better readability, maintainability, and compliance with
Django best practices.
"""
from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _


class CustomClearableFileInput(ClearableFileInput):
    """
    A custom widget for file input, with modified labels and a custom template.

    - clear_checkbox_label: Text for the "clear" checkbox.
    - initial_text: Label for the currently uploaded file.
    - input_text: Label for the file input (left blank for simplicity).
    - template_name: Path to the custom template for rendering the widget.
    """
    clear_checkbox_label = _('Remove')
    initial_text = _('Current Image')
    input_text = _('')
    template_name = 'products/custom_widget_templates/custom_clearable_file_input.html'
