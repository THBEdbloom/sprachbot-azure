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
        self.correction_made = None
        print("👋 Willkommen beim Registrierungsprozess.")
        print("➡️ Wie lautet dein Vorname?")

    def is_complete(self):
        return all(self.data.values())

    def process_input(self, user_input):
        # Wenn keine Entitäten erkannt wurden
        if user_input == None:
            # Der Bot wartet erneut auf eine Eingabe
            return ("❓ Ich konnte keine Angabe erkennen. Bitte wiederhole das.")
        
        # Der Bot verarbeitet die Eingabe und fragt den nächsten Schritt ab
        response = query_clu(user_input)
        prediction = response["result"]["prediction"]
        entities = prediction.get("entities", [])
        intent = prediction.get("topIntent")

        # Wenn der Intent "Abbruch-Intent" ist, wird der Bot die Registrierung abbrechen
        if intent == "Abbruch-Intent":
            print("🛑 Registrierung wurde vom Benutzer abgebrochen.")
            exit(0)

        # Wenn der Intent "Bestätigung-Intent" ist, fragt der Bot nach der Bestätigung
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

        # Prüfen, ob der Benutzer nach einer Korrektur fragt
        if intent == "Korrektur-Intent":
            # Wenn eine Entität in der Korrektur erkannt wurde, zum spezifischen Feld springen
            if entities:
                for ent in entities:
                    if "_Korrektur" in ent["category"]:  # Überprüfe, ob eine Korrektur-Entität erkannt wurde
                        current_field = ent["category"].replace("_Korrektur", "")  # Entferne "_Korrektur" von der Kategorie
                        self.data[current_field] = None  # Lösche den aktuellen Wert für die Korrektur
                        self.previous_step_index = self.current_step_index
                        self.current_step_index = self.steps.index(current_field)  # Gehe zum Schritt der Entität
                        
                        next_field = self.steps[self.current_step_index]
                        self.correction_made = True
                        return f"🔁 Kein Problem. Bitte gib deinen {next_field} erneut an."
            
            # Wenn keine Entität in der Korrektur erkannt wurde, zurück zur letzten Frage
            elif not self.awaiting_confirmation:
                if self.current_step_index > 0:
                    self.current_step_index -= 1  # Gehe zurück zur letzten Frage
                current_field = self.steps[self.current_step_index]  # Die vorherige offene Frage
                return f"🔁 Kein Problem. Bitte gib dein {current_field} erneut an."
            else:
                return "❓ Ich konnte nicht festellen welche Eingabe du ändern möchtest. Bitte wiederhole das."

        # Weitere Logik für die Entitäten-Erkennung und Datenspeicherung
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

        if self.correction_made:
            self.current_step_index = self.previous_step_index
            self.correction_made = False
        else:
            # Weiter zur nächsten Frage
            self.current_step_index += 1  # Erhöhen des Index, um zur nächsten Frage zu gehen

        # Überprüfen, ob alle Felder ausgefüllt sind
        if self.current_step_index >= len(self.steps):
            self.awaiting_confirmation = True
            daten = "\n".join([f"{k}: {v}" for k, v in self.data.items()])
            return f"🔍 Ich habe folgende Daten erfasst:\n{daten}\n➡️ Stimmen diese Angaben? (Ja oder Nein)"

        if self.current_step_index < len(self.steps):
            next_field = self.steps[self.current_step_index]
            return f"➡️ Bitte gib auch dein {next_field} an."