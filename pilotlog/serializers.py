import json
from rest_framework import serializers
from .models import Aircraft, FlightLog, Approach, Person
from django.template import Context, Template
from .custom_field_renderer import CustomFieldRenderer

class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = '__all__'
        
class ApproachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Approach
        fields = '__all__'

class PersonSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ['id', 'user', 'role']

    def get_user(self, obj):
        if obj.user:
            return {
                'id': obj.user.id,
                'username': obj.user.username,
                'email': obj.user.email,
            }
        return None

class FlightLogSerializer(serializers.ModelSerializer):
    aircraft = AircraftSerializer()
    approaches = ApproachSerializer(many=True, read_only=True)
    persons = PersonSerializer(many=True, read_only=True)
    custom_fields = serializers.JSONField()

    class Meta:
        model = FlightLog
        fields = '__all__'
        
        
    def to_representation(self, instance):
        """Customize the representation of the FlightLog instance."""
        attrs = super().to_representation(instance)
        
        # Use CustomFieldRenderer to handle custom fields
        custom_fields = attrs.get('custom_fields', {})
        renderer = CustomFieldRenderer(custom_fields, instance)
        attrs['custom_fields'] = renderer.render_custom_fields()
        
        return attrs
