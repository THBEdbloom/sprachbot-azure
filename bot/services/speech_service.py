import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv

load_dotenv()

class SpeechService:
    def __init__(self):
        speech_key = os.getenv("SPEECH_KEY")
        service_region = os.getenv("SPEECH_REGION")
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        speech_config.speech_recognition_language = "de-DE"

        self.recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
        self.recognizer.properties.set_property(speechsdk.PropertyId.SpeechServiceConnection_InitialSilenceTimeoutMs, "10000")
        self.recognizer.properties.set_property(speechsdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs, "2000")

    def recognize(self):
        print("🔊 Sprich jetzt...")
        result = self.recognizer.recognize_once()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("❗ Keine Sprache erkannt. Bitte versuche es erneut.")
            return None
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation = result.cancellation_details
            print(f"🔴 Erkennung abgebrochen: {cancellation.reason}")
            return None