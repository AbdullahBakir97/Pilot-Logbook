import json
from typing import Any, Dict, List
from uuid import uuid4
from django.contrib.auth.models import User
from pilotlog.models import Aircraft, FlightLog, Approach, Person
from pilotlog.serializers import AircraftSerializer, FlightLogSerializer, ApproachSerializer, PersonSerializer

class DataTransformer:

    @staticmethod
    def fetch_data():
        user_data = User.objects.all()
        user_id_map = {user.id: user.id for user in user_data}

        data_map = {
            "Aircraft": AircraftSerializer(Aircraft.objects.all(), many=True).data,
            "FlightLog": FlightLogSerializer(FlightLog.objects.all(), many=True).data,
            "Approach": ApproachSerializer(Approach.objects.all(), many=True).data,
            "Person": PersonSerializer(Person.objects.all(), many=True).data,
        }

        return data_map, user_id_map

    @staticmethod
    def transform_instance_data(
        instance_data: List[Dict[str, Any]], 
        table_name: str, 
        user_id_map: Dict[int, int], 
        current_timestamp: int, 
        related_fields: List[str] = None
    ) -> List[Dict[str, Any]]:
        transformed_data = []
        if related_fields is None:
            related_fields = []

        for instance in instance_data:
            user_id = instance.get("user_id") or (instance.get("user") and instance["user"].get("id"))
            transformed_instance = {
                "user_id": user_id_map.get(user_id),
                "table": table_name,
                "guid": str(uuid4()),
                "meta": {k: v for k, v in instance.items() if k not in related_fields},
                "_modified": current_timestamp,
            }
            transformed_data.append(transformed_instance)

        return transformed_data
