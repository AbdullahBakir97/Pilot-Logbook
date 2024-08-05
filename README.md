# Pilot Logbook Management System

## Project Overview

The Pilot Logbook Management System is a comprehensive solution designed to manage pilot logbooks effectively. The system provides various functionalities and services aimed at ensuring efficient data handling and user interaction:

1. **Extensible Data Model** 📦: Utilizes JSON fields and custom renderers to accommodate flexible data structures. This allows the system to adapt to various logbook formats and user requirements.
   - [Extensible Data Model Example](https://github.com/AbdullahBakir97/Pilot-Logbook/blob/main/pilotlog/models.py#L90)

2. **Django REST Framework (DRF) Integration** 🌐: Implements DRF viewsets and serializers to provide RESTful API endpoints for interacting with the data. This integration ensures robust and scalable web services.
   - List and create aircraft: `/api/aircraft/`
   - Retrieve, update, and delete a specific aircraft: `/api/aircraft/<id>/`
   - List and create flight logs: `/api/flightlogs/`
   - Retrieve, update, and delete a specific flight log: `/api/flightlogs/<id>/`

3. **Data Import/Export Mechanisms** 📥📤: Provides mechanisms for importing and exporting data, facilitating easy data migration and backup. This includes support for JSON and CSV formats.
   - Importer Module: Reads data from a JSON file and imports it into the database.
     - [Importer Module Example](https://github.com/AbdullahBakir97/Pilot-Logbook/blob/main/pilotlog/utils/importer.py#L6)
   - Exporter Module: Exports the data from the database to a CSV file.
     - [Exporter Module Example](https://github.com/AbdullahBakir97/Pilot-Logbook/blob/main/pilotlog/utils/exporter.py#L8)
   - Management commands for generating JSON data and handling import/export operations.
     - [Generate JSON Command](https://github.com/AbdullahBakir97/Pilot-Logbook/blob/main/pilotlog/management/commands/generate_json.py#L7)
     - [Import Logs Command](https://github.com/AbdullahBakir97/Pilot-Logbook/blob/main/pilotlog/management/commands/import_logs.py#L6)
     - [Export Logs Command](https://github.com/AbdullahBakir97/Pilot-Logbook/blob/main/pilotlog/management/commands/export_logs.py#L7)

4. **Admin Integration** 🛠️: Custom admin actions for importing and exporting data directly from the Django admin interface, streamlining workflows for administrators.
   - [Admin Integration Example](https://github.com/AbdullahBakir97/Pilot-Logbook/blob/main/pilotlog/admin.py#L81)

5. **Custom Field Rendering** 🎨: Custom rendering logic to handle dynamic and user-defined fields within the logbook data.
   - [Custom Field Renderer](https://github.com/AbdullahBakir97/Pilot-Logbook/blob/main/pilotlog/utils/custom_field_renderer.py#L5)
   
6. **Data Transformation** 🔄: Logic to transform imported data into the required format, ensuring consistency and integrity.
   - [Data Transformer](https://github.com/AbdullahBakir97/Pilot-Logbook/blob/main/pilotlog/utils/data_transformer.py#L8)

![scrnli_03_08_2024_17-08-48](https://github.com/user-attachments/assets/155c7bfe-77b4-4ffc-8856-be62ea17912d)
![2024-08-03](https://github.com/user-attachments/assets/67dc8cda-ec60-4f6f-a416-d36bc8bfe35a)
![scrnli_03_08_2024_17-07-41](https://github.com/user-attachments/assets/5e477418-eb7c-4e8b-a602-adf843db3be1)


## Installation and Setup

### Prerequisites

- Python
- Django
- PostgreSQL (or another database supported by Django ORM)

### Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Abdullahbakir97/Pilot-Logbook.git
   cd Pilot-Logbook
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Database**

   Update the `DATABASES` setting in `project/settings.py` to configure your database.

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_db_name',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

5. **Run Migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Data Directory**

   Ensure the `Data` directory exists and is writable.

7. **Load Initial Data**

   ```bash
   python manage.py import_logs Data/import-pilotlog_mcc.json
   ```

8. **Export Initial Data**

   ```bash
   python manage.py export_logs Data/import-pilotlog_mcc.json Data/export-logbook_template.csv
   ```

9. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

10. **Access the Admin Panel**

    Create a superuser to access the Django admin panel.

    ```bash
    python manage.py createsuperuser
    ```

    Then log in at `http://127.0.0.1:8000/admin`.

## Usage

### Importing Data

To import data from the JSON file, use the `PilotLogImporter` class.

```python
from pilotlog.importers import PilotLogImporter

importer = PilotLogImporter('path_to_your_json_file.json')
importer.import_logs()
```

### Exporting Data

To export data to a CSV file, use the `PilotLogExporter` class.

```python
from pilotlog.exporters import PilotLogExporter

exporter = PilotLogExporter('path_to_your_csv_file.csv')
exporter.export_logs()
```

## API Endpoints

The `pilotlog` app includes API endpoints to interact with the data. You can access the endpoints via the Django REST Framework.

### URLs

- List and create aircraft: `/api/aircraft/`
- Retrieve, update, and delete a specific aircraft: `/api/aircraft/<id>/`
- List and create flight logs: `/api/flightlogs/`
- Retrieve, update, and delete a specific flight log: `/api/flightlogs/<id>/`

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Django](https://www.djangoproject.com/) - The web framework used.
- [Django REST Framework](https://www.django-rest-framework.org/) - Powerful and flexible toolkit for building Web APIs.

---

### Additional Considerations

- **DRY Principles**: The code uses helper methods to parse time and handle defaults to avoid repetition.
- **Future Adaptability**: The models and import/export logic are designed to be flexible and easily extendable.
- **OOP Principles**: Classes and methods encapsulate functionality, making the codebase modular and maintainable.

This setup adheres to Django best practices, ensures a clean and organized project structure, and demonstrates effective use of Django components, DRY, and OOP principles.

