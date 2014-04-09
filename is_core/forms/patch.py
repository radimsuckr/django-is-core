from __future__ import unicode_literals

from django.forms.widgets import DateInput , DateTimeInput, TimeInput, Widget
from django.forms.fields import FileField

from is_core.forms.utils import add_class_name
from is_core.forms.widgets import DragAndDropFileInput


def build_attrs(self, extra_attrs=None, **kwargs):
    "Helper function for building an attribute dictionary."
    attrs = dict(self.attrs, **kwargs)
    if extra_attrs:
        attrs.update(extra_attrs)
    if self.class_name:
        attrs = add_class_name(attrs, self.class_name)
    if self.placeholder:
        attrs['placeholder'] = self.placeholder
    return attrs


Widget.placeholder = None
Widget.class_name = None
Widget.build_attrs = build_attrs

DateInput.class_name = 'date'
TimeInput.class_name = 'time'
DateTimeInput.class_name = 'datetime'

FileField.widget = DragAndDropFileInput
