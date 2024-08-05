import os
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Aircraft, FlightLog
from .serializers import AircraftSerializer, FlightLogSerializer
from utils.importer import PilotLogImporter
from utils.exporter import PilotLogExporter

class AircraftViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Aircraft objects.
    """
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer


class FlightLogViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing FlightLog objects.
    """
    queryset = FlightLog.objects.all()
    serializer_class = FlightLogSerializer

    @action(detail=False, methods=['post'])
    def import_logs(self, request) -> Response:
        """
        Import flight logs from a JSON file.
        :param request: HTTP request object containing 'file_path' in data.
        :return: Response indicating the result of the import operation.
        """
        file_path = request.data.get('file_path')
        if not file_path:
            return Response({"error": "file_path is required"}, status=400)

        if not os.path.exists(file_path):
            return Response({"error": "File does not exist"}, status=400)

        importer = PilotLogImporter(file_path)
        try:
            importer.import_logs()
            return Response({"status": "logs imported"})
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    @action(detail=False, methods=['get'])
    def export_logs(self, request) -> JsonResponse:
        """
        Export flight logs to a CSV file.
        :param request: HTTP request object containing 'file_path' in query params.
        :return: JsonResponse indicating the result of the export operation.
        """
        file_path = request.query_params.get('file_path')
        if not file_path:
            return JsonResponse({"error": "file_path is required"}, status=400)

        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        exporter = PilotLogExporter(file_path)
        try:
            exporter.export_logs()
            return JsonResponse({"status": "logs exported"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)