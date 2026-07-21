import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("IBM_API_KEY")
project_id = "4e85ef54-3234-4dc3-b007-164f0675acc1"
service_url = os.getenv("IBM_SERVICE_URL", "https://us-south.ml.cloud.ibm.com")

print("API Key:", api_key[:5] + "..." if api_key else "None")
print("Project ID:", project_id)
print("Service URL:", service_url)

# Get Token
token_resp = requests.post(
    "https://iam.cloud.ibm.com/identity/token",
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    data={
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key,
    }
)
print("Token Status:", token_resp.status_code)
if token_resp.status_code == 200:
    token = token_resp.json()["access_token"]
    print("Token retrieved successfully")
    
    # Try calling generation
    url = f"{service_url}/ml/v1/text/generation?version=2023-05-29"
    payload = {
        "model_id": "ibm/granite-3-3-8b-instruct",
        "project_id": project_id,
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
    print("Generation Status:", gen_resp.status_code)
    print("Response Headers:", gen_resp.headers)
    print("Response Body:", gen_resp.text)
else:
    print("Failed to get token:", token_resp.text)
