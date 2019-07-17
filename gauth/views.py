import httplib2

from googleapiclient.discovery import build
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from .models import CredentialsModel
from .models import SessId
from julia import settings
from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from django.shortcuts import render
from httplib2 import Http
from django.conf import settings
#from julia.main.views import home
def session_id(request):
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key
def home(request):
    display = False
    try:
        storage = SessId.objects.get(session = session_id(request))
    except SessId.DoesNotExist:
        return render(request, 'auth_page.html')
        
    print(storage)
    return HttpResponseRedirect("/Widgets")# render(request, 'main_index.html')
FLOW = flow_from_clientsecrets(
    settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
    scope=['https://www.googleapis.com/auth/calendar','https://www.googleapis.com/auth/userinfo.profile','https://www.googleapis.com/auth/contacts','https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.labels','https://www.googleapis.com/auth/gmail.modify'],
    redirect_uri='http://127.0.0.1:8080/oauth2callback',
    prompt='consent')
def gmail_authenticate(request):
    FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                       request.user)
    authorize_url = FLOW.step1_get_authorize_url()
    return HttpResponseRedirect(authorize_url)
def auth_return(request):
    get_state = bytes(request.GET.get('state'), 'utf8')
    if not xsrfutil.validate_token(settings.SECRET_KEY, get_state,
                                   request.user):
        return HttpResponseBadRequest()
    credential = FLOW.step2_exchange(request.GET.get('code'))
    #http = Http()
    #http = credential.authorise(http)
    new_entry = SessId(session = session_id(request),access_code=credential.access_token,credential=credential)
    new_entry.save()
    print(request.session.session_key)
    return HttpResponseRedirect("/")
def logout(request):
    SessId.objects.filter(session = session_id(request)).delete()
    return HttpResponseRedirect("/")
