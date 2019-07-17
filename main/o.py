from django.shortcuts import render
from gauth.models import SessId
from django.http import HttpResponseRedirect
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from julia import settings
from django.http import JsonResponse
def session_id(request):
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key

def logout(request):
    SessId.objects.filter(session = session_id(request)).delete()
    return HttpResponseRedirect("/")
def builder(request):
    query = SessId.objects.get(session = session_id(request))
    field_object = SessId._meta.get_field('access_code')#access_code
    credential = field_object.value_from_object(query)
    code = SessId._meta.get_field('credential')
    coda = code.value_from_object(query)
    http = Http()
    http = coda.authorize(http)
    service = build('gmail', 'v1', http=http)
    return service
def getLabels(request):
    print("HEllp")
    service = builder(request)
    results = service.users().labels().list(userId='me').execute()
    ids = results.get('labels',[])
    out = []
    out2 = []
    out3=[]
    out4=[]
    total1=[]
    unread1=[]
    
    total2=[]
    unread2=[]
    s = 'CATEGORY_'
    print(results)
    
    for x in ids:
       
        if s in x['id']:
            ap = x['id'][9:].lower()
            out.append(ap.capitalize())
            out3.append(x['id'])
            results = service.users().labels().get(userId='me',id=x['id']).execute()
            total1.append(int(results.get('messagesTotal',[])))
            unread1.append(int(results.get('messagesUnread',[])))
        else:
            ap = x['id'].lower()
            out4.append(x['id'])
            out2.append(ap.capitalize())
            results = service.users().labels().get(userId='me',id=x['id']).execute()
            total2.append(int(results.get('messagesTotal',[])))
            unread2.append(int(results.get('messagesUnread',[])))
       
    print(total1)
    data = {'verified':True,'categories':out,'labels':out2,'a':out3,'b':out4,'total1':total1,'unread1':unread1,'total2':total2,'unread2':unread2}
    return JsonResponse(data)
def getFrom(froma,typea):
    for x in froma:
        if x['name']==typea:
            val =str(x['value'])
    return val
def getMail(request,service,labels):
    results = service.users().messages().list(userId='me',maxResults=5,labelIds=labels).execute()
    
    messages = results.get('messages',[])
    froma = []
    fromaNOT = []
    date = []
    for x in messages:
        msg = service.users().messages().get(userId='me',id=x['id']).execute()
        pld = msg['payload']
        headers = pld['headers']
        # FROM
        froma.append(getFrom(headers,'From')) 
        froma.append(getFrom(headers,'From').split('<')[0])
        # DATE
        date.append(getFrom(headers,'Date'))
    return JsonResponse(data)
def home(request):
    service = builder(request)
    #labels = getLabels(request,service)
    #mails = getMail(request,service)
    return render(request,'test_page.html')
def mailer(request):
    service = builder(request)
    data = {'mail_list':getMail(request,service,request.GET.get('label',None)),'verified':True}
    return JsonResponse(data)
def mailList(request):
    
    labels=request.GET.get('label',None)
    service = builder(request)
    results = service.users().messages().list(userId='me',maxResults=5,labelIds=labels).execute()
    sender = []
    chara = []
    subject = []
    messages = results.get('messages',[])
    for x in messages:
        msg = service.users().messages().get(userId='me',id=x['id']).execute()
        pld = msg['payload']
        headers = pld['headers']
        n = getFrom(headers,'From')
        sender.append(n.split('<')[0])
        chara.append((n.split('<')[0])[0])
        subject.append(getFrom(headers,'Subject')[:30])
    data = {'sender':sender,'chara':chara,'subject':subject,'verified':True}
    print(sender,chara,subject)
    return JsonResponse(data)
