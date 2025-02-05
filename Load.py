import sqlite3
from sql_queries import *


def create_tables(db_path):
    """Create tables if not exist."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    create_tables = [Patients_table_create,FDA_Drug_Info_table_create,Events_table_create,Medication_Requests_table_create]
    for query in create_tables:
        cursor.execute(query)
    conn.commit()
    conn.close()

def upsert_data(db_path, patient_df,events_df, medication_requests_df, fda_drug_info_df):
    """Insert or update data in the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for _, row in patient_df.iterrows():
        cursor.execute(insert_or_update_patients, (
            row['id'], row['name'], row['gender'],
            row['birth_date'], row['address'], row['ssn']
        ))
    print("Patients data successfully inserted into the database.")
    
    for _, row in events_df.iterrows():
        cursor.execute(insert_or_update_events, (
            row['id'], row['patient_id'], row['status'],row['start_date'],
            row['end_date'],row['event_type'], row['serviceProvider'], row['participant']
        ))
    print("Events successfully inserted into the database.")

    for _, row in fda_drug_info_df.iterrows():
        cursor.execute(insert_or_update_FDA_Drug_Info, (
            row['drug_id'], row['brand_name'], row['generic_name'],row['manufacturer_name'],
            row['active_ingredients'],row['dosage_form'],row['route'],row['warnings'],row['indications_and_usage']
        ))
    print("FDA data successfully inserted into the database.")

    for _, row in medication_requests_df.iterrows():
        cursor.execute(insert_or_update_Medication_Requests, (
            row['id'], row['status'], row['medication_name'],row['medication_code'],
            row['patient_reference'], row['event_reference']
        ))
    print("Medication Requests successfully inserted into the database.")

    

    conn.commit()
    conn.close()

    
   