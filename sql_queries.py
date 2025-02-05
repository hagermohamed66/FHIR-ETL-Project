# CREATE TABLES

Patients_table_create=''' CREATE TABLE IF NOT EXISTS Patients (
                            id TEXT PRIMARY KEY,
                            name TEXT,
                            gender TEXT,
                            birth_date DATE,
                            address TEXT,
                            ssn TEXT UNIQUE
                        )
                        '''


Events_table_create=''' CREATE TABLE IF NOT EXISTS "Events" (
                            "id" TEXT	PRIMARY KEY,
                            "patient_id"	TEXT NOT NULL,
                            "status"	TEXT,
                            "start_date"	Date,
                            "end_date"	Date,
                            "event_type"	TEXT,
                            "serviceProvider"	TEXT,
                            "participant"	TEXT,
                            FOREIGN KEY("patient_id") REFERENCES "Patient"("id")
                        )
                    '''

FDA_Drug_Info_table_create=''' CREATE TABLE IF NOT EXISTS "FDA_Drug_Info" (
                                "drug_id"	TEXT PRIMARY KEY,
                                "brand_name"	TEXT,
                                "generic_name"	TEXT,
                                "manufacturer_name"	TEXT,
                                "active_ingredients"	TEXT,
                                "dosage_form" TEXT,
                                "route" TEXT,
                                "warnings"	TEXT,
                                "indications_and_usage" TEXT
                        )
                     '''

Medication_Requests_table_create= ''' CREATE TABLE IF NOT EXISTS "Medication_Requests" (
                                        "id"	TEXT PRIMARY KEY,
                                        "status"	TEXT,
                                        "medication_name"	TEXT,
                                        "medication_code"	TEXT,
                                        "patient_reference"	TEXT NOT NULL,
                                        "event_reference"	TEXT,
                                        FOREIGN KEY("medication_code") REFERENCES "FDA_Drug_Info"("drug_id"),
                                        FOREIGN KEY("patient_reference") REFERENCES "Patient"("id")
                                    )
                            '''

insert_or_update_patients=''' REPLACE INTO Patients (id, name, gender, birth_date, address, ssn)
                              VALUES (?, ?, ?, ?, ?, ?);
                          '''

insert_or_update_events='''  REPLACE INTO Events (id, patient_id, status, start_date, end_date, event_type, serviceProvider, participant)
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                        '''
insert_or_update_Medication_Requests='''  REPLACE INTO Medication_Requests (id, status, medication_name, medication_code, patient_reference, event_reference)
                                          VALUES (?, ?, ?, ?, ?, ?);
                                     '''


insert_or_update_FDA_Drug_Info='''  REPLACE INTO  FDA_Drug_Info (drug_id, brand_name, generic_name , manufacturer_name, active_ingredients, dosage_form,route,warnings,indications_and_usage)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                                '''
