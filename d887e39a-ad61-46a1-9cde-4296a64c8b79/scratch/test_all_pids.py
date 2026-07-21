import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("IBM_API_KEY")
project_ids = [
    "9d77d83f-ab8e-44f6-b361-9eca8dabc113", # Agent
    "dd226e6d-9a1e-429c-b205-b361efe07bda", # Crop
    "9e41896d-42d2-43b9-822b-91734ff9d6d5", # Simple_agent
]
service_url = "https://us-south.ml.cloud.ibm.com"

# Get Token
token_resp = requests.post(
    "https://iam.cloud.ibm.com/identity/token",
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    data={
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key,
    }
)

if token_resp.status_code == 200:
    token = token_resp.json()["access_token"]
    print("Token retrieved.")
    
    for pid in project_ids:
        print(f"\n--- Testing Project ID: {pid} ---")
        url = f"{service_url}/ml/v1/text/generation?version=2023-05-29"
        payload = {
            "model_id": "ibm/granite-3-3-8b-instruct",
            "project_id": pid,
            "input": "Explain FFT in 1 sentence.",
            "parameters": {
                "max_new_tokens": 50
            }
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        gen_resp = requests.post(url, headers=headers, json=payload)
        print("Status Code:", gen_resp.status_code)
        print("Response Body:", gen_resp.text)
else:
    print("Failed to get token:", token_resp.text)
