import json
from typing import Any, Dict
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

    def __init__(self, custom_fields: Dict[str, Any], instance: Any):
        """
        Initialize the CustomFieldRenderer with custom fields and an instance.
        :param custom_fields: Dictionary of custom fields.
        :param instance: Instance of the model to render fields for.
        """
        self.custom_fields = custom_fields
        self.instance = instance

    def render_custom_fields(self) -> Dict[str, Any]:
        """
        Render custom fields based on their types.
        :return: Dictionary of rendered custom fields.
        """
        rendered_fields = {}
        for field_name, value in self.custom_fields.items():
            try:
                field_type = self.get_field_type(field_name)
                rendered_fields[field_name] = self.render_field(field_type, value)
            except Exception as e:
                rendered_fields[field_name] = f'Error rendering field {field_name}: {e}'
        return rendered_fields

    def get_field_type(self, field_name: str) -> str:
        """
        Extract the field type from the field name.
        :param field_name: Name of the field.
        :return: Field type.
        """
        return next((field_type for field_type in self.FIELD_TYPES if field_name.startswith(f"[{field_type}]")), 'Text')

    def render_field(self, field_type: str, value: Any) -> Any:
        """
        Render individual fields based on their type.
        :param field_type: Type of the field.
        :param value: Value of the field.
        :return: Rendered field value.
        """
        try:
            field_renderer = self.FIELD_TYPES.get(field_type, str)
            rendered_value = field_renderer(value) if value is not None else field_renderer()
            
            if isinstance(rendered_value, str):
                template = Template(rendered_value)
                context = Context({'instance': self.instance})
                rendered_value = template.render(context)

            return rendered_value
        
        except Exception as e:
            raise ValueError(f'Error rendering field value for {field_type}: {e}')