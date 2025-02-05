import os
import pandas as pd
import time
from Extract import *
from Transform import *
from Load import *
import logging


def main():

    # Define directories and database
    fhir_data_directory = "./FHIR Data/"  # Directory for raw FHIR data
    db_file = "./DB/FHIR_DB.db"             # SQLite database file
    logging.basicConfig(filename="errors.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

    # 1. Extract: Load all FHIR JSON files
    print("Extracting data...")
    extracted_fhir_data = extract_fhir_data(fhir_data_directory)
    if not extracted_fhir_data:
        print("No data found in the directory. Exiting...")
        return
    print(f"Extracted data from {len(extracted_fhir_data)} files.")

   # 2. Transform: Process and clean data
    print("Transforming data...")
    patients_df = pd.DataFrame()
    medication_requests_df = pd.DataFrame()
    events_df = pd.DataFrame()
    patients_df, medication_requests_df, events_df = transform_fhir_data(extracted_fhir_data)
    if patients_df.empty:
        print("No patient data found. Exiting...")
        return
    else: 
        print(f"Transformed {len(patients_df)} patient records.")
        #print(patients_df.head())
        #print("----------------------------------")
        #print(medication_requests_df.head())
        #print("----------------------------------")
        #print(events_df.head())
        #print("----------------------------------")


    drug_ids= medication_requests_df['medication_code'].unique()
    fda_drug_info_df = pd.DataFrame()
    fda_drug_info_df = transform_fda_data(drug_ids)

    #print(fda_drug_info_df.head())


    # 3. Load: Insert/Update SQLite database
    print("Loading data into the database...")
    create_tables(db_file)  # Create tables if they don't exist
    upsert_data(db_file, patients_df, events_df, medication_requests_df, fda_drug_info_df) 
    print("All data successfully loaded into the database.")


if __name__ == "__main__":
    main()