from django.shortcuts import redirect
from django.conf import settings
from django.views import View
from django.http import JsonResponse
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

CLIENT_SECRETS_FILE = "client_secret.com.json"

SCOPES = ['https://www.googleapis.com/auth/calendar',
          'https://www.googleapis.com/auth/userinfo.email',
          'https://www.googleapis.com/auth/userinfo.profile',
          'openid']
REDIRECT_URL = 'http://127.0.0.1:8000/rest/v1/calendar/redirect'
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v3'

class GoogleCalendarInitView(View):
    def get(self,request):
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes = SCOPES,
            redirect_uri=REDIRECT_URL
        )
        
        auth_url, state = flow.authorization_url(prompt='consent')
        
        return redirect(auth_url)
    
class GoogleCalendarRedirectView(View):
    def get(self, request):
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URL
            )
        
        flow.fetch_token(authorization_response=request.build_absolute_uri(),
                         include_client_id=True,
                         code=request.GET.get('code'))
        
        credentials = flow.credentials
        
        service = build('calendar', 'v3', credentials=credentials)
        
        events_result = service.events().list(calendarId='primary', maxResults=10, singleEvents=True).execute()
        events = events_result.get('items',[])
        
        return JsonResponse({'events':events})
        
        