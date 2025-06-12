from bot.services.clu_client import query_clu
from bot.database.sql_client import save_user_data
from bot.services.validators import validate_field  # <-- Ausgelagert!
from datetime import datetime
import re

class ConversationManager:
    def __init__(self):
        self.data = {
            "Vorname": None,
            "Nachname": None,
            "Geburtsdatum": None,
            "Straße": None,
            "Hausnummer": None,
            "PLZ": None,
            "Ort": None,
            "Land": None,
            "Email": None,
            "Telefonnummer": None
        }
        self.steps = list(self.data.keys())
        self.current_step_index = 0
        self.awaiting_confirmation = False
        self.returning_from_correction = False
        self.previous_step_index = None
        self.correction_made = None

        print("👋 Willkommen beim Registrierungsprozess.")
        print("➡️ Wie lautet dein Vorname?")

    def is_complete(self):
        return all(self.data.values())

    def process_input(self, user_input):
        if user_input is None:
            return "❓ Ich konnte keine Angabe erkennen. Bitte wiederhole das."

        response = query_clu(user_input)
        prediction = response["result"]["prediction"]
        entities = prediction.get("entities", [])
        intent = prediction.get("topIntent")

        if intent == "Abbruch-Intent":
            print("🛑 Registrierung wurde vom Benutzer abgebrochen.")
            exit(0)

        if intent == "Hilfe-Intent":
            current_field = self.steps[self.current_step_index]
            hilfetexte = {
                "Vorname": "Bitte gib deinen Vornamen an, z. B. Laura oder Mehmet.",
                "Nachname": "Bitte gib deinen Nachnamen an, z. B. Schulz oder Yilmaz.",
                "Geburtsdatum": "Bitte gib dein Geburtsdatum im Format TT.MM.JJJJ an, z. B. 21.04.1990.",
                "Straße": "Bitte gib den Namen deiner Straße an, z. B. Hauptstraße.",
                "Hausnummer": "Bitte gib deine Hausnummer an, z. B. 5 oder 7A.",
                "PLZ": "Bitte gib deine Postleitzahl an, z. B. 10115.",
                "Ort": "Bitte nenne den Ort, in dem du wohnst.",
                "Land": "Bitte gib dein Wohnsitzland an, z. B. Deutschland oder Österreich.",
                "Email": "Bitte nenne deine E-Mail-Adresse, z. B. name@example.com.",
                "Telefonnummer": "Bitte gib deine Telefonnummer an, z. B. 0151 12345678."
            }
            hilfe = hilfetexte.get(current_field, "Bitte gib die benötigte Information an.")
            return f"ℹ️ Hilfe: {hilfe}"

        if intent == "Bestätigungs-Intent":
            user_input_lower = user_input.lower()
            if any(phrase in user_input_lower for phrase in ["ja", "richtig"]):
                try:
                    print("⏳ Registrierung in Arbeit...")
                    save_user_data(self.data)
                    self.awaiting_confirmation = False
                    return "✅ Registrierung abgeschlossen."
                except Exception as e:
                    print(f"❌ Fehler beim Speichern der Daten: {e}")
                    self.awaiting_confirmation = True
                    daten = "\n".join([f"{k}: {v}" for k, v in self.data.items()])
                    return f"🔍 Ich habe folgende Daten erfasst:\n{daten}\n➡️ Stimmen diese Angaben? (Ja oder Nein)"

            elif any(phrase in user_input_lower for phrase in ["nein", "falsch"]):
                print("❌ Du hast angegeben, dass die Daten nicht korrekt sind.")
                return "🔁 Welche Angabe möchtest du korrigieren?"

        if intent == "Korrektur-Intent":
            if entities:
                for ent in entities:
                    if "_Korrektur" in ent["category"]:
                        current_field = ent["category"].replace("_Korrektur", "")
                        self.data[current_field] = None
                        self.previous_step_index = self.current_step_index
                        self.current_step_index = self.steps.index(current_field)
                        self.correction_made = True
                        return f"🔁 Kein Problem. Bitte gib deinen {current_field} erneut an."

            elif not self.awaiting_confirmation:
                if self.current_step_index > 0:
                    self.current_step_index -= 1
                current_field = self.steps[self.current_step_index]
                return f"🔁 Kein Problem. Bitte gib dein {current_field} erneut an."
            else:
                return "❓ Ich konnte nicht festellen welche Eingabe du ändern möchtest. Bitte wiederhole das."

        current_field = self.steps[self.current_step_index]
        recognized_entity = None

        for ent in entities:
            if ent["category"] == current_field:
                recognized_entity = ent["text"]
                self.data[current_field] = recognized_entity
                break

        if not self.data[current_field]:
            return f"❓ Ich konnte keine Angabe zu {current_field} erkennen. Bitte wiederhole das."

        if not validate_field(current_field, self.data[current_field]):
            self.data[current_field] = None
            if current_field == "Geburtsdatum":
                return "⚠️ Bitte gib dein Geburtsdatum im Format TT.MM.JJJJ an, z. B. 20.02.2002."
            return f"⚠️ Die Angabe zu {current_field} scheint ungültig zu sein. Bitte versuche es erneut."

        if current_field == "Hausnummer":
            match = re.search(r"\d{1,4}[a-zA-Z]?", self.data[current_field].strip().rstrip("."))
            if match:
                self.data[current_field] = match.group(0)

        print(f"📌 {current_field}: {self.data[current_field]}")

        if self.correction_made:
            self.current_step_index = self.previous_step_index
            self.correction_made = False
        else:
            self.current_step_index += 1

        if self.current_step_index >= len(self.steps):
            self.awaiting_confirmation = True
            daten = "\n".join([f"{k}: {v}" for k, v in self.data.items()])
            return f"🔍 Ich habe folgende Daten erfasst:\n{daten}\n➡️ Stimmen diese Angaben? (Ja oder Nein)"

        if self.current_step_index < len(self.steps):
            next_field = self.steps[self.current_step_index]
            return f"➡️ Bitte gib auch dein {next_field} an."
