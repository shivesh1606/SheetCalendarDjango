
from django.shortcuts import render
from django.http import HttpResponse
from .utils import get_user_profile


from django.shortcuts import render
from django.http import HttpResponse
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import os
CLIENT_SECRET_FILE = r'C:\Users\shive\Documents\GitHub\CalendarDjango\Calendar\config\credentials.json'

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly',
          'https://www.googleapis.com/auth/userinfo.profile']

def home(request):
    return render(request, 'home.html')

# def auth(request):
#     return render(request, 'auth.html')



def auth(request):
    creds = None
    if 'token.json' in os.listdir():
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                 CLIENT_SECRET_FILE, SCOPES, 
    )
            creds = flow.run_local_server(port=0, propmt='consent',include_granted_scopes="true")
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    print(creds.token)
    user_profile = get_user_profile(creds.token)
    print(user_profile)
    return HttpResponse("Authentication successful! + " + str(user_profile.get("name")))

def signup_redirect(request):
    messages.error(request, "Something wrong here, it may be that you already have account!")
    return redirect("homepage")