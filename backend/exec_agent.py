import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/calendar.events'
]

class ExecAgent:
    def __init__(self):
        self.creds = self._authenticate()
        self.gmail_service = build('gmail', 'v1', credentials=self.creds) if self.creds else None
        self.calendar_service = build('calendar', 'v3', credentials=self.creds) if self.creds else None

    def _authenticate(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds

    def get_upcoming_events(self):
        if not self.calendar_service: return "Calendar disconnected."
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = self.calendar_service.events().list(calendarId='primary', timeMin=now, maxResults=5, singleEvents=True, orderBy='startTime').execute()
        return events_result.get('items', [])

    def get_unread_emails(self):
        if not self.gmail_service: return "Gmail disconnected."
        results = self.gmail_service.users().messages().list(userId='me', labelIds=['INBOX'], q='is:unread').execute()
        return results.get('messages', [])

exec_agent = ExecAgent()
