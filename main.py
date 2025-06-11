from bot.services.speech_service import SpeechService
from bot.services.conversation import ConversationManager

def main():
    print("🟣 Sprachbot gestartet. Sprich für die Registrierung.")
    speech = SpeechService()
    convo = ConversationManager()

    while True:
        user_input = speech.recognize()

        print(f"✅ Erkannt: {user_input}")

        response = convo.process_input(user_input)
        print(response)

        if convo.awaiting_confirmation is False and convo.is_complete():
            break

if __name__ == "__main__":
    main()
