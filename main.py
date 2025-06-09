from bot.services.speech_service import SpeechService
from bot.services.conversation import ConversationManager

def main():
    print("🟣 Sprachbot gestartet. Sprich für die Registrierung oder sage 'Stopp'.")
    speech = SpeechService()
    convo = ConversationManager()

    while True:
        user_input = speech.recognize()

        if not user_input:
            print("❗ Keine Sprache erkannt. Bitte versuche es erneut.")
            continue

        print(f"✅ Erkannt: {user_input}")

        # Sofortiger Abbruch durch Schlüsselwort
        if user_input.lower().strip() in ["stopp", "stop", "abbrechen", "exit", "tschüss"]:
            print("🛑 Registrierung wurde manuell abgebrochen.")
            return

        response = convo.process_input(user_input)
        print(response)

        if convo.awaiting_confirmation is False and convo.is_complete():
            break

if __name__ == "__main__":
    main()
