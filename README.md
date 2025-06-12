# 🟣 Sprach-Bot für sprachgesteuerte Registrierung

Ein intelligenter Sprachassistent, der Nutzereingaben per Sprache erfasst, mit Hilfe von Azure Cognitive Services versteht, validiert und strukturiert in einer SQL-Datenbank speichert.

---

## 📦 Funktionen

- 🎤 Sprache-zu-Text mit Azure Speech Service
- 🧠 Intent- und Entitätserkennung mit Azure CLU (Conversational Language Understanding)
- 🔄 Benutzerführung mit Validierung, Korrektur-Handling und Hilfe-Intent
- 💾 Speicherung der Benutzerdaten in einer SQL Server-Datenbank

---

## 🧱 Architektur

User → SpeechService → ConversationManager → CLU API / Validator → SQL-Datenbank


**Module:**
- `main.py` – Startpunkt
- `speech_service.py` – Spracheingabe über Azure Speech
- `conversation.py` – zentrale Steuerlogik
- `clu_client.py` – Anbindung an Azure CLU
- `validators.py` – Eingabevalidierung
- `sql_client.py` – Datenbankzugriff

---

## ⚙️ Voraussetzungen

- Python 3.8+
- Azure-Abonnements für Speech & CLU
- Microsoft SQL Server (lokal oder remote)
- `.env` Datei mit folgenden Variablen:

```env
SPEECH_KEY=...
SPEECH_REGION=...

CLU_ENDPOINT=...
CLU_KEY=...
CLU_PROJECT_NAME=...
CLU_DEPLOYMENT_NAME=...

SQL_SERVER=...
SQL_DATABASE=...
SQL_USERNAME=...
SQL_PASSWORD=...
