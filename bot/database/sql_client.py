import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

def save_user_data(data):
    server = os.getenv("SQL_SERVER")
    database = os.getenv("SQL_DATABASE")
    username = os.getenv("SQL_USERNAME")
    password = os.getenv("SQL_PASSWORD")
    driver = "{ODBC Driver 17 for SQL Server}"

    try:
        with pyodbc.connect(
            f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
        ) as conn:
            cursor = conn.cursor()

            # Tabelle anlegen, falls sie nicht existiert
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Benutzerdaten')
                BEGIN
                    CREATE TABLE Benutzerdaten (
                        ID INT IDENTITY(1,1) PRIMARY KEY,
                        Vorname NVARCHAR(100),
                        Nachname NVARCHAR(100),
                        Geburtsdatum NVARCHAR(50),
                        Straße NVARCHAR(200),
                        PLZ NVARCHAR(20),
                        Ort NVARCHAR(100),
                        Land NVARCHAR(100),
                        Email NVARCHAR(100),
                        Telefonnummer NVARCHAR(50)
                    )
                END
            """)

            # Datensatz einfügen
            cursor.execute("""
                INSERT INTO Benutzerdaten (
                    Vorname, Nachname, Geburtsdatum, Straße, PLZ, Ort, Land, Email, Telefonnummer
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data["Vorname"],
                data["Nachname"],
                data["Geburtsdatum"],
                data["Straße"],
                data["PLZ"],
                data["Ort"],
                data["Land"],
                data["Email"],
                data["Telefonnummer"]
            ))

            conn.commit()
            print("💾 Benutzerdaten erfolgreich gespeichert.")

    except Exception as e:
        print("❌ Fehler beim Speichern der Daten:", e)