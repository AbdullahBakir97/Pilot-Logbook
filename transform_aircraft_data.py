import pandas as pd
import json

# Corrected JSON data
aircraft_json_data = '''
[
    {
        "user_id": 125880,
        "table": "Aircraft",
        "guid": "00000000-0000-0000-0000-000000000367",
        "meta": {
            "Fin": "",
            "Sea": false,
            "TMG": false,
            "Efis": false,
            "FNPT": 0,
            "Make": "Cessna",
            "Run2": false,
            "Class": 5,
            "Model": "C150",
            "Power": 1,
            "Seats": 0,
            "Active": true,
            "Kg5700": false,
            "Rating": "",
            "Company": "Other",
            "Complex": false,
            "CondLog": 69,
            "FavList": false,
            "Category": 1,
            "HighPerf": false,
            "SubModel": "",
            "Aerobatic": false,
            "RefSearch": "PHALI",
            "Reference": "PH-ALI",
            "Tailwheel": false,
            "DefaultApp": 0,
            "DefaultLog": 2,
            "DefaultOps": 0,
            "DeviceCode": 1,
            "AircraftCode": "00000000-0000-0000-0000-000000000367",
            "DefaultLaunch": 0,
            "Record_Modified": 1616320991
        },
        "platform": 9,
        "_modified": 1616317613
    },
    {
        "user_id": 125880,
        "table": "Aircraft",
        "guid": "00000000-0000-0000-0000-000000000368",
        "meta": {
            "Fin": "",
            "Sea": false,
            "TMG": false,
            "Efis": false,
            "FNPT": 0,
            "Make": "Cessna",
            "Run2": false,
            "Class": 5,
            "Model": "C150",
            "Power": 1,
            "Seats": 0,
            "Active": true,
            "Kg5700": false,
            "Rating": "",
            "Company": "Other",
            "Complex": false,
            "CondLog": 69,
            "FavList": false,
            "Category": 1,
            "HighPerf": false,
            "SubModel": "",
            "Aerobatic": false,
            "RefSearch": "PHGRA",
            "Reference": "PH-GRA",
            "Tailwheel": false,
            "DefaultApp": 0,
            "DefaultLog": 2,
            "DefaultOps": 0,
            "DeviceCode": 1,
            "AircraftCode": "00000000-0000-0000-0000-000000000368",
            "DefaultLaunch": 0,
            "Record_Modified": 1616320991
        },
        "platform": 9,
        "_modified": 1616317613
    }
]
'''

# Load JSON data
aircraft_data = json.loads(aircraft_json_data)

# Create DataFrame from JSON data
df_aircraft = pd.DataFrame(aircraft_data)

# Extract the meta information into separate columns
df_meta = pd.json_normalize(df_aircraft['meta'])
df_aircraft = pd.concat([df_aircraft.drop('meta', axis=1), df_meta], axis=1)

# Map the fields to the ForeFlight import format
df_aircraft['AircraftID'] = df_aircraft['guid']
df_aircraft['Make'] = df_aircraft['Make']
df_aircraft['Model'] = df_aircraft['Model']
df_aircraft['Class'] = df_aircraft['Class']
df_aircraft['Complex'] = df_aircraft['Complex']
df_aircraft['HighPerformance'] = df_aircraft['HighPerf']
df_aircraft['Reference'] = df_aircraft['RefSearch']

# Handle custom fields with default values
df_aircraft['CustomFieldName_Text'] = ''  # Default value for text custom field
df_aircraft['CustomFieldName_Numeric'] = 0  # Default value for numeric custom field
df_aircraft['CustomFieldName_Hours'] = 0.0  # Default value for hours custom field
df_aircraft['CustomFieldName_Counter'] = 0  # Default value for counter custom field
df_aircraft['CustomFieldName_Date'] = pd.NaT  # Default value for date custom field
df_aircraft['CustomFieldName_DateTime'] = pd.NaT  # Default value for datetime custom field
df_aircraft['CustomFieldName_Toggle'] = False  # Default value for toggle custom field

# Reorder columns to match ForeFlight import format
foreflight_columns = [
    'AircraftID', 'Make', 'Model', 'Class', 'Complex', 'HighPerformance', 'Reference',
    'CustomFieldName_Text', 'CustomFieldName_Numeric', 'CustomFieldName_Hours',
    'CustomFieldName_Counter', 'CustomFieldName_Date', 'CustomFieldName_DateTime', 'CustomFieldName_Toggle'
]

df_aircraft = df_aircraft[foreflight_columns]

# Save to CSV file with header and comments
output_file = 'foreflight_aircraft_import.csv'
with open(output_file, 'w') as f:
    # Optional: Add a header comment
    f.write("# Aircraft data for ForeFlight import\n")
    f.write("# Ensure that custom fields are correctly mapped and populated\n")
    df_aircraft.to_csv(f, index=False)

print(f"Transformation complete. File saved as '{output_file}'")
