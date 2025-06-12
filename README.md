# 🧠 Sprach-Bot – Sprachgesteuerte Registrierung mit Azure & CLU

Ein sprachbasierter Bot zur Benutzerregistrierung mit **Azure Speech**, **Conversational Language Understanding (CLU)** und **SQL-Datenbankintegration**. Der Bot führt Nutzer durch eine sprachgesteuerte Eingabe von persönlichen Daten, validiert diese und speichert sie in einer SQL-Datenbank.

---

## 🚀 Features

- 🎙️ **Spracherkennung** mit Azure Speech SDK
- 🧠 **Intent & Entity-Erkennung** über Azure CLU
- 🔁 **Dialogfluss mit Validierung & Korrekturoption**
- 💾 **Persistenz in SQL Server-Datenbank**
- ♻️ **Modularer, wartbarer Codeaufbau**

---

## 🧱 Architektur

```plaintext
+-------------------+      Spracheingabe      +--------------------+
|                   | ---------------------> |                    |
|   User (Spricht)  |                         |  SpeechService     |
|                   | <---------------------  | (Azure Speech API) |
+-------------------+     Transkribierter     +--------------------+
                             Text
                                     |
                                     v
                            +--------------------+
                            | ConversationManager|
                            | (Steuerlogik)      |
                            +--------------------+
                                     |
      +-----------------------------+------------------------------+
      |                             |                              |
      v                             v                              v
CLU API (Intent + Entity)    Validator-Logik               SQL-Datenbank
(bot.services.clu_client)    (bot.services.validators)     (bot.database.sql_client)
```

---

## 🔁 Interaktionsablauf (Sequenzdiagramm)

```plaintext
User            SpeechService        ConversationManager        CLU API             SQL DB
 |                    |                        |                    |                  |
 | Spricht            |                        |                    |                  |
 |------------------->|                        |                    |                  |
 |                    | Sprache -> Text        |                    |                  |
 |                    |----------------------->|                    |                  |
 |                    |                        | intent + entities  |                  |
 |                    |                        |------------------->|                  |
 |                    |                        |                    |                  |
 |                    |                        |<-------------------|                  |
 |                    |                        | verarbeitet intent |                  |
 |                    |                        | validiert Eingabe  |                  |
 |                    |                        | speichert ggf.     |----------------->|
 |                    |                        |                    |     INSERT       |
 |                    |                        |                    |<-----------------|
```

---

## 📂 Modulübersicht

| Datei               | Beschreibung |
|---------------------|--------------|
| `main.py`           | Einstiegspunkt, startet Sprachservice & Dialogmanager |
| `speech_service.py` | Nutzt Azure Speech SDK zur Spracheingabe |
| `conversation.py`   | Steuert gesamten Registrierungsdialog, erkennt Intents & führt Validierung durch |
| `clu_client.py`     | Schnittstelle zur Azure CLU API (Conversational Language Understanding) |
| `sql_client.py`     | Erstellt Tabelle (falls nötig) & speichert Benutzerdaten |
| `validators.py`     | Prüft Felder auf Gültigkeit (Regex, Formatlogik) |

---

## 🛠 Setup

### 1. Voraussetzungen

- Python 3.10+
- Azure Ressourcen:
  - Speech Service
  - Conversational Language Understanding (CLU)
  - SQL Server + Datenbank

### 2. Installation

```bash
git clone https://github.com/dein-nutzername/sprachbot.git
cd sprachbot
pip install -r requirements.txt
```

### 3. `.env` Datei anlegen

```env
SPEECH_KEY=
SPEECH_REGION=

CLU_ENDPOINT=
CLU_KEY=
CLU_PROJECT_NAME=
CLU_DEPLOYMENT_NAME=

SQL_SERVER=
SQL_DATABASE=
SQL_USERNAME=
SQL_PASSWORD=
```

---

## ✅ Validierungsregeln

| Feld           | Validierung                                |
|----------------|---------------------------------------------|
| Vorname        | Nur Buchstaben, ≥ 2 Zeichen                 |
| Nachname       | Nur Buchstaben, ≥ 2 Zeichen                 |
| Geburtsdatum   | Format `TT.MM.JJJJ`, Alter < 120 Jahre      |
| Straße         | ≥ 2 Zeichen                                 |
| Hausnummer     | Ziffern mit optionalem Buchstaben (z. B. 5A)|
| PLZ            | 5-stellige Zahl                             |
| E-Mail         | Muss `@` und `.` enthalten                  |
| Telefonnummer  | Mindestens 7 Ziffern                        |

---

## 💾 Datenbankstruktur

Tabelle: `Benutzerdaten`

| Spalte         | Typ            |
|----------------|----------------|
| ID             | INT (PK)       |
| Vorname        | NVARCHAR(100)  |
| Nachname       | NVARCHAR(100)  |
| Geburtsdatum   | NVARCHAR(50)   |
| Straße         | NVARCHAR(200)  |
| Hausnummer     | NVARCHAR(20)   |
| PLZ            | NVARCHAR(20)   |
| Ort            | NVARCHAR(100)  |
| Land           | NVARCHAR(100)  |
| Email          | NVARCHAR(100)  |
| Telefonnummer  | NVARCHAR(50)   |

---

## ▶️ Beispielstart

```bash
python main.py
```

---

## 🙌 Mitwirkende

- ✨ Laurin Krüger – als Ersteller
- 💬 Azure – für Sprache & KI
