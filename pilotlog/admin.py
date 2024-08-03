import json
import csv
from django.contrib import admin
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .models import Aircraft, FlightLog, Person, Approach
from .forms import FlightLogForm
from pilotlog.importer import PilotLogImporter
from pilotlog.exporter import PilotLogExporter
from django import forms
from django.contrib import messages

@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = (
        'aircraft_id', 'equipment_type', 'type_code', 'year', 'make', 
        'model', 'category', 'aircraft_class', 'gear_type', 'engine_type', 
        'complex', 'high_performance', 'pressurized', 'taa'
    )
    search_fields = ('aircraft_id', 'make', 'model')
    list_filter = ('equipment_type', 'year', 'aircraft_class', 'gear_type', 'engine_type')
    ordering = ('make', 'model', 'year')

class ImportForm(forms.Form):
    import_file = forms.FileField()

@admin.register(FlightLog)
class FlightLogAdmin(admin.ModelAdmin):
    form = FlightLogForm
    list_display = (
        'aircraft', 'date', 'from_airport', 'to_airport', 'total_time', 
        'pic', 'sic', 'night', 'flight_review', 'checkride', 'ipc'
    )
    search_fields = ('aircraft__aircraft_id', 'from_airport', 'to_airport', 'instructor_name')
    list_filter = (
        'date', 'aircraft__make', 'aircraft__model', 
        'flight_review', 'checkride', 'ipc'
    )
    ordering = ('-date', 'aircraft')
    actions = ['import_logs', 'export_logs']

    def import_logs(self, request, queryset):
        """Import logs from a JSON file."""
        if request.method == 'POST':
            import_form = ImportForm(request.POST, request.FILES)
            if import_form.is_valid():
                import_file = import_form.cleaned_data['import_file']
                file_path = default_storage.save('import_temp.json', ContentFile(import_file.read()))
                
                try:
                    importer = PilotLogImporter(default_storage.path(file_path))
                    importer.import_logs()
                    self.message_user(request, "Pilot logs imported successfully.")
                except FileNotFoundError:
                    self.message_user(request, "File not found. Please ensure the file path is correct.", level=messages.ERROR)
                except json.JSONDecodeError:
                    self.message_user(request, "Error decoding JSON file. Please check the file format.", level=messages.ERROR)
                except Exception as e:
                    self.message_user(request, f"Error importing logs: {e}", level=messages.ERROR)
                finally:
                    # Clean up the temporary file
                    default_storage.delete(file_path)
                
                return

        else:
            import_form = ImportForm()

        return HttpResponse(
            content=(
                '<form method="post" enctype="multipart/form-data">'
                '    {csrf_token}'
                '    <label for="id_import_file">Select file:</label>'
                '    <input type="file" name="import_file" required id="id_import_file">'
                '    <button type="submit">Upload</button>'
                '</form>'
            ).format(csrf_token=request.csrf_token)
        )

    def export_logs(self, request, queryset):
        """Export logs to a CSV file using PilotLogExporter."""
        try:
            json_file_path = default_storage.path('Data/import-pilotlog_mcc.json')
            csv_file_path = default_storage.path('Data/export-logbook_template.csv')
            
            exporter = PilotLogExporter(json_file_path, csv_file_path)
            exporter.export_to_csv()
            
            with default_storage.open(csv_file_path, 'rb') as csvfile:
                response = HttpResponse(csvfile.read(), content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="export-logbook_template.csv"'
                return response
        except Exception as e:
            self.message_user(request, f"Error exporting logs: {e}", level=messages.ERROR)
            return HttpResponse(status=500)

    import_logs.short_description = "Import Pilot Logs"
    export_logs.short_description = "Export Pilot Logs"

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__username', 'role', 'user__email')
    list_filter = ('role',)
    ordering = ('user', 'role')

@admin.register(Approach)
class ApproachAdmin(admin.ModelAdmin):
    list_display = ('type', 'runway', 'airport', 'comments')
    search_fields = ('type', 'runway', 'airport', 'comments')
    list_filter = ('type', 'airport')
    ordering = ('type', 'airport', 'runway')
