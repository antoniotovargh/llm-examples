'''
Authenticates google workspace for the user and sets tokens.json for the user
'''
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from streamlit_google_auth import Authenticate
import streamlit as st
from typing import Literal


SCOPES = [
    "openid", 
    "https://www.googleapis.com/auth/userinfo.profile", 
    "https://www.googleapis.com/auth/userinfo.email",
    # gmail
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    # # sheets
    # 'https://www.googleapis.com/auth/spreadsheets',
    # 'https://www.googleapis.com/auth/drive'
    # # calendar
    # 'https://www.googleapis.com/auth/calendar',
    
    ]

CREDENTIALS = os.environ.get('GOOGLE_CREDENTIALS')

class GoogleWorkspaceAuth():
    @staticmethod
    def desktop_authenticate():
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds
    
class StreamlitGoogleAuth(Authenticate):
    def login(self, color:Literal['white', 'blue']='blue', justify_content: str="center", scopes=SCOPES) -> tuple:
        if not st.session_state['connected']:
            flow = Flow.from_client_secrets_file(
                self.secret_credentials_path, # replace with you json credentials from your google auth app
                scopes=scopes,
                redirect_uri=self.redirect_uri,
            )

            authorization_url, state = flow.authorization_url(
                    access_type="offline",
                    # include_granted_scopes="true",
                )
            
            html_content = f"""
                <div style="display: flex; justify-content: {justify_content};">
                    <a href="{authorization_url}" target="_self" style="background-color: {'#fff' if color == 'white' else '#4285f4'}; color: {'#000' if color == 'white' else '#fff'}; text-decoration: none; text-align: center; font-size: 16px; margin: 4px 2px; cursor: pointer; padding: 8px 12px; border-radius: 4px; display: flex; align-items: center;">
                        <img src="https://lh3.googleusercontent.com/COxitqgJr1sJnIDe8-jiKhxDx1FrYbtRHKJ9z_hELisAlapwE9LUPh6fcXIfb5vwpbMl4xl9H9TRFPc5NOO8Sb3VSgIBrfRYvW6cUA" alt="Google logo" style="margin-right: 8px; width: 26px; height: 26px; background-color: white; border: 2px solid white; border-radius: 4px;">
                        Sign in with Google
                    </a>
                </div>
                """
            st.markdown(html_content, unsafe_allow_html=True)