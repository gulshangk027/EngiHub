"""
EngiHub Configuration — loads all settings from .env
"""
import os
from dotenv import load_dotenv

# Load .env file relative to the location of this config file
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(os.path.dirname(basedir), '.env'))

class Config:
    # Flask
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "engihub-dev-secret-key-change-in-prod")
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"

    # IBM watsonx.ai
    IBM_API_KEY     = os.getenv("IBM_API_KEY", "")
    IBM_PROJECT_ID  = os.getenv("IBM_PROJECT_ID", "")
    IBM_SERVICE_URL = os.getenv("IBM_WATSONX_URL", os.getenv("IBM_SERVICE_URL", "https://au-syd.ml.cloud.ibm.com"))

    # AI Models
    PRIMARY_MODEL  = os.getenv("PRIMARY_MODEL",  "ibm/granite-8b-code-instruct")
    FALLBACK_MODEL = os.getenv("FALLBACK_MODEL", "mistralai/mistral-large")
