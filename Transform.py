import pandas as pd
import requests
import logging

def transform_fhir_data(fhir_data):
    """Transform FHIR data to extract related information."""
    patients_df = pd.DataFrame()
    medication_requests_df = pd.DataFrame()
    events_df = pd.DataFrame()
    for entry in fhir_data:
        for resource in entry.get('entry', []):
            if resource['resource']['resourceType'] == 'Patient':
                patient = {
                    'id': resource['resource'].get('id'),
                    'name': ' '.join([n['given'][0] + ' ' + n['family'] for n in resource['resource'].get('name', [])]),
                    'gender': resource['resource'].get('gender', 'Unknown'),
                    'birth_date': resource['resource'].get('birthDate', 'Unknown'),
                    'address': ', '.join([addr.get('line', [''])[0] for addr in resource['resource'].get('address', [])]),
                    'ssn': next(
                        (id['value'] for id in resource['resource'].get('identifier', [])
                         if any(c['display'] == 'Social Security Number' for c in id.get('type', {}).get('coding', []))),
                        'Unknown'
                    )
                }
                patients_df= pd.concat([patients_df, pd.DataFrame([patient])], ignore_index=True)

            if resource['resource']['resourceType'] == 'MedicationRequest':
                medication_request = {
                    'id': resource['resource'].get('id', ''),
                    'status': resource['resource'].get('status', ''),
                    'medication_name': resource['resource'].get('medicationCodeableConcept', {}).get('text', ''),
                    'medication_code': resource['resource'].get('medicationCodeableConcept', {}).get('coding', [{}])[0].get('code', ''),
                    'patient_reference': resource['resource'].get('subject', {}).get('reference', '')[9:],
                    'event_reference': resource['resource'].get('encounter', {}).get('reference', '')[9:],
                            }
                medication_requests_df = pd.concat([medication_requests_df, pd.DataFrame([medication_request])], ignore_index=True)

            if resource['resource']['resourceType'] == 'Encounter':
                event = {
                    'id': resource['resource'].get('id', 'Unknown'),
                    'patient_id': resource['resource'].get('subject', {}).get('reference', '')[9:],
                    'status': resource['resource'].get('status', 'Unknown'),
                    'start_date': resource['resource'].get('period', {}).get('start', 'Unknown'),
                    'end_date': resource['resource'].get('period', {}).get('end', 'Ongoing'),
                    'event_type': resource['resource'].get('type', [{}])[0].get('coding', [{}])[0].get('display', 'Unknown'),
                    'serviceProvider': resource['resource'].get('serviceProvider', {}).get('display', 'Unknown'),
                    'participant': resource['resource'].get('participant', [{}])[0].get('individual', {}).get('display','Unknown'),
                }
                events_df = pd.concat([events_df , pd.DataFrame([event])], ignore_index=True)

    return patients_df, medication_requests_df, events_df 


def transform_fda_data(drug_ids):
    # Define the base FDA API URL
    FDA_API_URL = "https://api.fda.gov/drug/label.json"

    # List to store fetched data
    fda_drug_info_df = pd.DataFrame(columns=["drug_id", "brand_name", "generic_name", "manufacturer_name", "product_type", "description"])

    # Loop through the codes and fetch data
    for code in drug_ids:
        try:
            if code == '' :
                continue
            else:
                # Construct the query
                query = f"{FDA_API_URL}?search=openfda.rxcui:{code}"
                
                # Make the API call
                response = requests.get(query)
                response.raise_for_status()
                
                # Parse the response
                data = response.json()
                
                # Extract relevant details (customize as per requirements)
                for result in data.get("results", []):
                    new_row = {
                        "drug_id": code,
                        "brand_name": result.get("openfda", {}).get("brand_name", ["Unknown"])[0],
                        "generic_name": result.get("openfda", {}).get("generic_name", ["Unknown"])[0],
                        "manufacturer_name": result.get("openfda", {}).get("manufacturer_name", ["Unknown"])[0],
                        "active_ingredients": ', '.join(result.get("active_ingredient", ["N/A"])),
                        "dosage_form":result.get("openfda", {}).get("dosage_form", ["N/A"])[0],
                        "route":result.get("openfda", {}).get("route", ["N/A"])[0],
                        "warnings": '; '.join(result.get("warnings", ["N/A"])),
                        "indications_and_usage": '; '.join(result.get("indications_and_usage", ["N/A"]))
                    }
                    fda_drug_info_df = pd.concat([fda_drug_info_df, pd.DataFrame([new_row])], ignore_index=True)

        except Exception as e:
            #print(f"Error fetching data for code {code}: {e}")
            #logging.error("An error occurred", exc_info=True)
            continue

    return fda_drug_info_df