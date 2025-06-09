import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLU_ENDPOINT = os.getenv("CLU_ENDPOINT")
CLU_KEY = os.getenv("CLU_KEY")
CLU_PROJECT_NAME = os.getenv("CLU_PROJECT_NAME")
CLU_DEPLOYMENT_NAME = os.getenv("CLU_DEPLOYMENT_NAME")

def query_clu(text):
    url = f"{CLU_ENDPOINT}/language/:analyze-conversations?api-version=2024-11-15-preview"
    headers = {
        "Ocp-Apim-Subscription-Key": CLU_KEY,
        "Content-Type": "application/json"
    }
    body = {
        "kind": "Conversation",
        "analysisInput": {
            "conversationItem": {
                "participantId": "user1",
                "id": "1",
                "modality": "text",
                "language": "de",
                "text": text
            }
        },
        "parameters": {
            "projectName": CLU_PROJECT_NAME,
            "deploymentName": CLU_DEPLOYMENT_NAME,
            "verbose": True
        }
    }
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()