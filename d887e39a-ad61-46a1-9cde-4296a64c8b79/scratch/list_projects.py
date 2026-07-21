import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("IBM_API_KEY")

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
    
    # List projects
    url = "https://api.dataplatform.cloud.ibm.com/v2/projects"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    resp = requests.get(url, headers=headers)
    print("List Projects Status:", resp.status_code)
    if resp.status_code == 200:
        projects = resp.json()
        print("Projects:")
        for p in projects.get("resources", []):
            print(f"- Name: {p.get('entity', {}).get('name')}")
            print(f"  ID: {p.get('metadata', {}).get('guid')}")
    else:
        print("Error listing projects:", resp.text)
else:
    print("Failed to get token:", token_resp.text)
