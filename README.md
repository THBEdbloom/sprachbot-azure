# 🧠 Sprach-Bot – Sprachgesteuerte Registrierung mit Azure & CLU

Ein sprachbasierter Bot zur Benutzerregistrierung mit **Azure Speech**, **Conversational Language Understanding (CLU)** und **SQL-Datenbankintegration**. Der Bot führt Nutzer durch eine sprachgesteuerte Eingabe von persönlichen Daten, validiert diese und speichert sie in einer SQL-Datenbank.

---

## 🚀 Features

- 🎙️ **Spracherkennung** mit Azure Speech SDK
- 🧠 **Intent & Entity-Erkennung** über Azure CLU
- 🔁 **Dialogfluss mit Validierung & Korrekturoption**
- 💾 **Persistenz in SQL Server-Datenbank** über Azure SQL
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
  - Azure SQL Server

### 2. Installation

```bash
git clone https://github.com/dein-nutzername/sprachbot.git
cd sprachbot
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

---

## ☁️ Azure-Setup-Anleitung

Diese Anleitung beschreibt, wie du alle nötigen Azure-Ressourcen für den sprachgesteuerten Registrierungsbot einrichtest – inklusive Azure Speech, CLU und Azure SQL-Datenbank.

### 📋 Voraussetzungen

- Azure-Konto: https://azure.microsoft.com
- Azure CLI: https://learn.microsoft.com/de-de/cli/azure/install-azure-cli
- Python 3.10+

---

### 1️⃣ Ressourcengruppe erstellen (optional, empfohlen)

```bash
az login
az group create --name sprachbot-rg --location westeurope
```

---

### 2️⃣ Azure Speech Service einrichten

```bash
az cognitiveservices account create \
  --name sprachbot-speech \
  --resource-group sprachbot-rg \
  --kind SpeechServices \
  --sku F0 \
  --location westeurope
```

**Zugangsdaten abrufen:**

```bash
az cognitiveservices account keys list \
  --name sprachbot-speech \
  --resource-group sprachbot-rg
```

---

### 3️⃣ Azure CLU (Conversational Language Understanding)

#### A. Language Resource erstellen

```bash
az cognitiveservices account create \
  --name sprachbot-lang \
  --resource-group sprachbot-rg \
  --kind Language \
  --sku F0 \
  --location westeurope
```

#### B. Projekt in Language Studio

1. Gehe zu: https://language.azure.com
2. Wähle **Conversational Language Understanding**
3. Lege ein Projekt an:
   - Name: `RegistrierungBot`
   - Sprache: Deutsch
   - Ziel: Intent- & Entity-Erkennung
4. Trainiere & deploye dein Projekt (Deployment-Name: `production`)

**Zugangsdaten:**

```bash
az cognitiveservices account keys list \
  --name sprachbot-lang \
  --resource-group sprachbot-rg
```

---

### 4️⃣ Azure SQL-Datenbank einrichten

#### A. SQL Server erstellen

```bash
az sql server create \
  --name sprachbot-sql \
  --resource-group sprachbot-rg \
  --location westeurope \
  --admin-user sqladmin \
  --admin-password DeinSicheresPasswort123!
```

#### B. Datenbank anlegen

```bash
az sql db create \
  --resource-group sprachbot-rg \
  --server sprachbot-sql \
  --name SprachBotDB \
  --service-objective S0
```

#### C. Firewallregel setzen

```bash
az sql server firewall-rule create \
  --resource-group sprachbot-rg \
  --server sprachbot-sql \
  --name AllowAllLocal \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 255.255.255.255
```

---

### 5️⃣ .env Datei konfigurieren

```env
# Azure Speech
SPEECH_KEY=dein_speech_key
SPEECH_REGION=westeurope

# Azure CLU
CLU_ENDPOINT=https://sprachbot-lang.cognitiveservices.azure.com
CLU_KEY=dein_clu_key
CLU_PROJECT_NAME=RegistrierungBot
CLU_DEPLOYMENT_NAME=production

# Azure SQL
SQL_SERVER=sprachbot-sql.database.windows.net
SQL_DATABASE=SprachBotDB
SQL_USERNAME=sqladmin
SQL_PASSWORD=DeinSicheresPasswort123!
```

---

### ✅ Testen

```bash
python main.py
```

---

