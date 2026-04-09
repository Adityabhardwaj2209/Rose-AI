import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/calendar.readonly']

class GoogleService:
    def __init__(self):
        self.creds = self._authenticate()
        self.gmail = build('gmail', 'v1', credentials=self.creds) if self.creds else None
        self.calendar = build('calendar', 'v3', credentials=self.creds) if self.creds else None

    def _authenticate(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists('credentials.json'):
                    print("Google Services: credentials.json not found. Skipping.")
                    return None
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds

    def get_unread_emails(self):
        if not self.gmail: return "Google Service not configured."
        results = self.gmail.users().messages().list(userId='me', labelIds=['UNREAD'], maxResults=5).execute()
        messages = results.get('messages', [])
        return f"You have {len(messages)} unread emails, dude."

    def get_upcoming_events(self):
        if not self.calendar: return "Google Service not configured."
        from datetime import datetime
        now = datetime.utcnow().isoformat() + 'Z'
        events_result = self.calendar.events().list(calendarId='primary', timeMin=now, maxResults=3, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])
        return f"I see {len(events)} events coming up on your calendar."

google_service = GoogleService()
