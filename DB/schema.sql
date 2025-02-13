CREATE TABLE Patients (
                            id TEXT PRIMARY KEY,
                            name TEXT,
                            gender TEXT,
                            birth_date DATE,
                            address TEXT,
                            ssn TEXT UNIQUE
                        );
CREATE TABLE FDA_Drug_Info (
                                "drug_id"	TEXT PRIMARY KEY,
                                "brand_name"	TEXT,
                                "generic_name"	TEXT,
                                "manufacturer_name"	TEXT,
                                "product_type"	TEXT,
                                "description"	TEXT
                        );
CREATE TABLE Events    (
                            "id" TEXT	PRIMARY KEY,
                            "patient_id"	TEXT NOT NULL,
                            "status"	TEXT,
                            "start_date"	TEXT,
                            "end_date"	TEXT,
                            "event_type"	TEXT,
                            "serviceProvider"	TEXT,
                            "participant"	TEXT,
                            FOREIGN KEY("patient_id") REFERENCES "Patient"("id")
                        );
CREATE TABLE Medication_Requests    (
                                        "id"	TEXT PRIMARY KEY,
                                        "status"	TEXT,
                                        "medication_name"	TEXT,
                                        "medication_code"	TEXT,
                                        "patient_refrence"	TEXT NOT NULL,
                                        "event_refernce"	TEXT,
                                        FOREIGN KEY("medication_code") REFERENCES "FDA_Drug_Info"("medication_code"),
                                        FOREIGN KEY("patient_refrence") REFERENCES "Patient"("id")
                                    );
