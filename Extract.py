import json
import os
import requests

def extract_fhir_data(directory_path):
    """Extract FHIR data from all JSON files in the directory."""
    data = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            filepath = os.path.join(directory_path, filename)
            with open(filepath, 'r') as file:
                content = json.load(file)
                data.append(content)
    return data



