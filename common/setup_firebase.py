# This module sets up firebase. Make sure the environment variables
# used below are configured. load_dotenv() simplifies this process
import os
from dotenv import load_dotenv
load_dotenv()  
import firebase_admin
from firebase_admin import credentials, auth

key = {
    'type': os.environ['type'],
    'project_id': os.environ['project_id'],
    'private_key_id': os.environ['private_key_id'],
    'private_key': os.environ['private_key'].replace('\\n', '\n'),
    'client_email': os.environ['client_email'],
    'client_id': os.environ['client_id'],
    'auth_uri': os.environ['auth_uri'],
    'token_uri': os.environ['token_uri'],
    'auth_provider_x509_cert_url': os.environ['auth_provider_x509_cert_url'],
    'client_x509_cert_url': os.environ['client_x509_cert_url']
}

cred = credentials.Certificate(key)
default_app = firebase_admin.initialize_app(cred)