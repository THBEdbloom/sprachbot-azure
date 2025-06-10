from bot.services.clu_client import query_clu
from bot.database.sql_client import save_user_data

class ConversationManager:
    def __init__(self):
        self.data = {
            "Vorname": None,
            "Nachname": None,
            "Geburtsdatum": None,
            "Straße": None,
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
        self.previous_step_index = None  # Zum Speichern des vorherigen Schritts
        print("👋 Willkommen beim Registrierungsprozess.")
        print("➡️ Wie lautet dein Vorname?")

    def is_complete(self):
        return all(self.data.values())

    def user_wants_repeat(self, user_input):
        repeat_keywords = ["nochmal", "noch einmal", "bitte wiederholen", "wiederhole das bitte", "das war falsch"]
        return any(phrase in user_input.lower() for phrase in repeat_keywords)

    def user_wants_abort(self, user_input):
        abort_keywords = ["stopp", "abbrechen", "exit"]
        return any(phrase in user_input.lower() for phrase in abort_keywords)

    def user_wants_to_correct(self, user_input):
        correction_keywords = [
            "mein Vorname ist falsch", "ich möchte meinen Vorname ändern", "wiederhole meinen Vornamen",
            "mein Nachname ist falsch", "ich möchte meinen Nachnamen ändern", "wiederhole meinen Nachnamen",
            "ich möchte meine Adresse ändern", "mein Geburtsdatum ist falsch", "wiederhole mein Geburtsdatum"
        ]
        return any(phrase in user_input.lower() for phrase in correction_keywords)

    def process_input(self, user_input):
        # Benutzer möchte die Registrierung abbrechen
        if self.user_wants_abort(user_input):
            print("🛑 Registrierung wurde vom Benutzer abgebrochen.")
            exit(0)

        # Fehlerkorrektur direkt nach der Eingabe
        if self.user_wants_repeat(user_input):
            # Wenn der Benutzer sagt „Wiederhole das bitte“, dann wiederhole die Frage VOR der aktuellen Frage
            if self.current_step_index > 0:
                self.current_step_index -= 1  # Gehe zurück zur letzten Frage
            current_field = self.steps[self.current_step_index]  # Die vorherige offene Frage
            return f"🔁 Kein Problem. Bitte gib dein {current_field} erneut an."

        # Korrektur später im Prozess
        if self.user_wants_to_correct(user_input):
            current_field = self.steps[self.current_step_index]
            print(f"🔄 Du hast angegeben, dass du deinen {current_field} ändern möchtest.")
            self.data[current_field] = None
            self.previous_step_index = self.current_step_index  # Speichern der aktuellen Position
            self.current_step_index = self.steps.index("Vorname")  # Zurück zum Vorname
            return f"🔁 Bitte gib deinen Vornamen erneut an."

        response = query_clu(user_input)
        prediction = response["result"]["prediction"]
        entities = prediction.get("entities", [])
        intent = prediction.get("topIntent")

        if intent == "Abbruch":
            print("🛑 Registrierung wurde vom Benutzer abgebrochen.")
            exit(0)

        if intent == "Korrektur":
            current_field = self.steps[self.current_step_index]
            self.data[current_field] = None
            return f"🔁 Kein Problem. Bitte gib dein {current_field} erneut an."

        if self.awaiting_confirmation:
            if intent == "Bestätigung":
                if any(w in user_input.lower() for w in ["nein", "nicht", "falsch"]):
                    self.current_step_index = 0
                    for k in self.data:
                        self.data[k] = None
                    self.awaiting_confirmation = False
                    return "🔁 Okay, dann fangen wir nochmal von vorne an. Wie lautet dein Vorname?"
                else:
                    print("⏳ Registrierung wird verarbeitet...")
                    try:
                        save_user_data(self.data)
                        print("✅ Registrierung abgeschlossen.")
                    except Exception as e:
                        print("❌ Fehler beim Speichern der Daten:", e)
                        return f"❌ Fehler beim Speichern der Daten: {e}"
                    exit(0)
            else:
                return "❓ Bitte bestätige, ob die Angaben korrekt sind (Ja oder Nein)."

        current_field = self.steps[self.current_step_index]
        recognized_entity = None

        for ent in entities:
            if ent["category"] == current_field:
                recognized_entity = ent["text"]
                self.data[current_field] = recognized_entity
                break  # Nur die erste passende Entität speichern

        if not self.data[current_field]:
            return f"❓ Ich konnte keine Angabe zu {current_field} erkennen. Bitte wiederhole das."

        print(f"📌 {current_field}: {self.data[current_field]}")

        if self.returning_from_correction:
            self.returning_from_correction = False
            if self.is_complete():
                self.awaiting_confirmation = True
                daten = "\n".join([f"{k}: {v}" for k, v in self.data.items()])
                return f"🔍 Ich habe folgende Daten erfasst:\n{daten}\n➡️ Stimmen diese Angaben? (Ja oder Nein)"
            else:
                self.current_step_index += 1  # Wir erhöhen den Index, um zur nächsten Frage zu gehen
                return f"➡️ Bitte gib auch dein {self.steps[self.current_step_index]} an."

        # Überprüfen, ob der Benutzer die Frage nach dem Vornamen wiederholt hat und den Index nicht zurücksetzt
        self.current_step_index += 1  # Weiter zum nächsten Schritt (Nachname, Geburtsdatum, etc.)

        if self.current_step_index < len(self.steps):
            next_field = self.steps[self.current_step_index]
            return f"➡️ Bitte gib auch dein {next_field} an."
        else:
            self.awaiting_confirmation = True
            daten = "\n".join([f"{k}: {v}" for k, v in self.data.items()])
            return f"🔍 Ich habe folgende Daten erfasst:\n{daten}\n➡️ Stimmen diese Angaben? (Ja oder Nein)"
