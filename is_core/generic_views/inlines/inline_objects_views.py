from is_core.generic_views.inlines import InlineView
from is_core.utils import display_for_value


class DataRow(list):

    def __init__(self, values, class_names):
        super(DataRow, self).__init__(values)
        self.class_names = class_names


class InlineObjectsView(InlineView):
    """
    This inline class behaves and displays like 'InlineFormView', which is read-only. No need of any form or queryset.
    Implement method 'get_objects' and define a list of fields in the attribute 'fields'.
    """

    template_name = None

    # Tuple of tuples. The tuple consists of key and value (which will be displayed in template)
    # For eg: (('company_name', _('Company name')), ('zip', _('ZIP code')), ('...', '...'))
    fields = ()
    obj_class_names = ()

    def get_fields(self):
        return list(self.fields)

    def parse_object(self, obj):
        return obj

    def get_objects(self):
        """
        This method must return a list of models, dictionaries or any objects.

        Dictionaries must have keys defined in the attribute 'fields'. For eg: {'company_name': 'ABC', 'zip': '44455'}

        Objects / models must have attributes defined in the attribute 'fields'. Or it may have a humanizing methods
        'get_attributename_humanized', for eg: method 'get_zip_hunanized'.
        """
        raise NotImplementedError

    def get_data_list(self, fields, objects):
        out = []
        for obj in objects:
            normalized_obj = self.parse_object(obj)
            out.append(DataRow([(field_name, self.get_data_object(field_name, normalized_obj))
                                for field_name, _ in self.get_fields()],
                        self.get_obj_class_names(obj)))
        return out

    def get_obj_class_names(self, obj):
        return list(self.obj_class_names)

    def get_data_object(self, field_name, obj):
        humanize_method_name = 'get_%s_humanized' % field_name
        if hasattr(getattr(obj, humanize_method_name, None), '__call__'):
            value = getattr(obj, humanize_method_name)()
        elif hasattr(obj, field_name):
            value = getattr(obj, field_name)
        elif isinstance(obj, dict) and field_name in obj:
            value = obj.get(field_name)

        if hasattr(value, '__call__'):
            value = value()

        return display_for_value(value)

    def get_header_list(self, fields):
        return self.get_fields()

    def get_class_names(self):
        return [self.__class__.__name__.lower(), ]

    def get_context_data(self, **kwargs):
        context_data = super(InlineObjectsView, self).get_context_data(**kwargs)
        context_data.update({
            'data_list': self.get_data_list(self.get_fields(), self.get_objects()),
            'header_list': self.get_header_list(self.get_fields()),
            'class_names': self.get_class_names(),
            })
        return context_data


class TabularInlineObjectsView(InlineObjectsView):
    template_name = 'forms/tabular_inline_objects.html'


class ResponsiveInlineObjectsView(InlineObjectsView):
    template_name = 'forms/responsive_inline_objects.html'
