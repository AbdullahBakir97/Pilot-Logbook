import json
from django.template import Template, Context

class CustomFieldRenderer:
    FIELD_TYPES = {
        'Text': str,
        'Numeric': float,
        'Hours': float,
        'Counter': int,
        'Date': str,
        'DateTime': str,
        'Toggle': bool,
    }

    def __init__(self, custom_fields, instance):
        self.custom_fields = custom_fields
        self.instance = instance

    def render_custom_fields(self):
        """Render custom fields based on their types."""
        rendered_fields = {}
        for field_name, value in self.custom_fields.items():
            field_type = self.get_field_type(field_name)
            rendered_fields[field_name] = self.render_field(field_type, value)
        return rendered_fields

    def get_field_type(self, field_name):
        """Extract the field type from the field name."""
        for field_type in self.FIELD_TYPES.keys():
            if field_name.startswith(f"[{field_type}]"):
                return field_type
        return 'Text'  # Default field type

    def render_field(self, field_type, value):
        """Render individual fields based on their type."""
        field_renderer = self.FIELD_TYPES.get(field_type, str)
        rendered_value = field_renderer(value) if value is not None else field_renderer()
        
        # Render using template if value is a string (e.g., for Text fields)
        if isinstance(rendered_value, str):
            template = Template(rendered_value)
            context = Context({'instance': self.instance})
            rendered_value = template.render(context)

        return rendered_value
