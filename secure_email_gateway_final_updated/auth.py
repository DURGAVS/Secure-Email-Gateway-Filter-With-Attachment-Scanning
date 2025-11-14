import os
import json
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from config import SCOPES

def get_userinfo(access_token):
    userinfo_url = 'https://openidconnect.googleapis.com/v1/userinfo'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(userinfo_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get userinfo: {response.status_code} {response.text}")
        return {}

def get_gmail_service(user_email):
    token_file = f"token-{user_email}.json"
    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_file, 'w') as token_file_out:
            token_file_out.write(creds.to_json())
    
    # Build Gmail API service
    service = build('gmail', 'v1', credentials=creds)
    
    # Fetch userinfo to confirm email matches
    userinfo = get_userinfo(creds.token)
    email_from_token = userinfo.get('email', None)
    if email_from_token:
        print(f"Token is for email: {email_from_token}")
        if email_from_token.lower() != user_email.lower():
            print(f"⚠️  WARNING: Authenticated email ({email_from_token}) does not match the requested scan email ({user_email}).")
            print("👉 Please log in with the correct account or delete the token file and try again.")
    else:
        print("⚠️  WARNING: Could not fetch email from token. Gmail API may fail.")
    return service
