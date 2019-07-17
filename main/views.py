from django.shortcuts import render
from gauth.models import SessId
from django.http import HttpResponseRedirect
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from julia import settings
from django.http import JsonResponse
import base64
import quopri
import urllib, json
import urllib.request
import random 
from email.mime.text import MIMEText
from .models import Wids
from .models import Loop
from .models import Pin
from .models import Emails
def session_id(request):
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key
def EstimateDecode(num):
    ko = (num - 2)/2
    if ko<0:
        return 0
    return ko
def Game(request):
    service = builder(request)
    randomer= service.users().messages().list(userId='me',q='is:read',maxResults=20).execute()
        
    index = random.randint(0, len(randomer))
    ans = service.users().messages().get(userId='me', id=randomer['messages'][index]['id'],format='metadata',metadataHeaders=['From','Date']).execute()
    contacts = []
    snippet = []
    headers = ans['payload']['headers']
    awd = getFrom(headers,"From").split('<')[1].split('>')[0]
    filterer = '-from:'+awd+' '
    while(len(contacts)<3):
        print(len(contacts))
        service = builder(request)
        results = service.users().messages().list(userId='me',q=filterer,maxResults=1,labelIds=request.GET.get('label',None)).execute()
        if results['resultSizeEstimate']!=0:
            ida = results['messages'][0]['id']
            msg = service.users().messages().get(userId='me', id=ida,format='metadata',metadataHeaders=['From'],fields='payload').execute()
            headers = msg['payload']['headers']
            temp = getFrom(headers,"From").split('<')[1].split('>')[0]
            contacts.append(temp)
            filterer+='-from:'+temp+' '
        else:
            break
    contacts.append(awd)
    random.shuffle(contacts)
    return JsonResponse({'body':ans['snippet'],'answer':awd,'options':contacts})

def Counter(mails,request):
    ans = []
    service = builder(request)
    for mail in mails:
        
        results = service.users().messages().list(userId='me',q='from: '+mail,maxResults=20).execute()
        print(results)
        if EstimateDecode(results['resultSizeEstimate'])>10:
            ans.append('10+')
        else:
            ans.append(str(int(EstimateDecode(results['resultSizeEstimate']))))
    return ans
def logout(request):
    SessId.objects.filter(session = session_id(request)).delete()
    return HttpResponseRedirect("/")
def GetContacts(request):
    contacts = []
    filterer = ''
    chara = []
    while(len(contacts)<5):
        print(len(contacts))
        service = builder(request)
        results = service.users().messages().list(userId='me',q=filterer,maxResults=1,labelIds=request.GET.get('label',None)).execute()
        if results['resultSizeEstimate']!=0:
            ida = results['messages'][0]['id']
            msg = service.users().messages().get(userId='me', id=ida,format='metadata',metadataHeaders=['From'],fields='payload').execute()
            headers = msg['payload']['headers']
            temp = getFrom(headers,"From").split('<')[1].split('>')[0]
            chara.append(getFrom(headers,"From"))
            contacts.append(temp)
            filterer+='-from:'+temp+' '
        else:
            break
    return JsonResponse({'con':Counter(contacts,request),'mail': chara,'lb':request.GET.get('label',None)})
def GetNot(request):
    query = Emails.objects.filter(session = session_id(request))
    email = []
    counts = []
    for e in query:
        email.append(e.email)
        counts=(Counter(e.email,request))
    return JsonResponse({'emails':email,'counter':counts})
def AddNots(request):
    ses = session_id(request)
    Emails(session = ses,email = request.GET.get('id','')).save()
    return JsonResponse({'verified':True})
def Calendar(request):
    query = SessId.objects.get(session = session_id(request))
    code = SessId._meta.get_field('credential')
    coda = code.value_from_object(query)
    http = Http()
    http = coda.authorize(http)
    people_service = build('calendar','v3', http=http)
    profile = people_service.events().list(calendarId='primary',maxResults=10).execute()
    summary = []
    sDate = []
    eDate = []
    Link = []
    for event in profile['items']:
        summary.append(event['summary'])
        temp=''
        try:
            temp=(event['start']['date'])
        except:
            try:
                temp=(event['start']['dateTime'])
            except:
                temp='Wrong Date'
        sDate.append(temp)
        temp='' 
        try:
            temp=(event['end']['date'])
        except:
            try:
                temp(event['end']['dateTime'])
            except:
                temp='Not Specified'
        eDate.append(temp)
        Link.append(event['htmlLink'])
        #print(Link,eDate)
    return JsonResponse({'sum':summary,'Start':sDate,'End':eDate,'Link':Link})
def pbuilder(request):
    query = SessId.objects.get(session = session_id(request))
    code = SessId._meta.get_field('credential')
    coda = code.value_from_object(query)
    http = Http()
    http = coda.authorize(http)
    people_service = build(serviceName='people', version='v1', http=http)
    profile = people_service.people().get(resourceName='people/me', personFields='photos').execute()
    print(profile['photos'][0]['url'])
    return profile['photos'][0]['url']
def builder(request):
    query = SessId.objects.get(session = session_id(request))
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
    val = " "
    for x in froma:
        if x['name']==typea:
            val = str(x['value'])
    return val
def getMail(request,service,labels):
    results = service.users().messages().list(userId='me',maxResults=10,labelIds=labels).execute()
    
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
    return render(request,'test_page.html')
def Widget(request):
    return render(request,'widget.html')
def mailer(request):
    service = builder(request)
    data = {'mail_list':getMail(request,service,request.GET.get('label',None)),'verified':True}
    return JsonResponse(data)
def GetWid(request):
    query = Loop.objects.filter(session = session_id(request))
    #code = Loop._meta.get_field('div')
    #coda = code.value_from_object(query)
    div = []
    label = []
    for e in query:
        div.append(e.div)
        label.append(e.label)
    return JsonResponse({'div':div,'label':label})    
def AddWid(request):
    Loop(session = session_id(request),div=request.GET.get('div',''),label=request.GET.get('label',None)).save()
    ver = True
    return JsonResponse({'verified':ver})
def GetPin(request):
    query = Pin.objects.filter(session = session_id(request))
    #code = Loop._meta.get_field('div')
    #coda = code.value_from_object(query)
    div = []
    label = []
    for e in query:
        div.append(e.div)
        label.append(e.label)
    return JsonResponse({'div':div,'label':label})
def AddPin(request):
    Pin(session = session_id(request),div=request.GET.get('div',''),label=request.GET.get('label',None)).save()
    ver = True
    return JsonResponse({'verified':ver})
def FindFrom(request):
    repeat = request.GET.get('repeat','')
    labels=request.GET.get('label','INBOX')
    if(request.GET.get('fora','no')=='no' ):
        labels = labels[2:]
    service = builder(request)
    results = service.users().messages().list(userId='me',maxResults=10,labelIds='INBOX',q='From:'+labels).execute()
    sender = []
    subject = []
    ids=[]
    snippet = []
    date = []
    messages = results.get('messages',[])
    for x in messages:
        msg = service.users().messages().get(userId='me',id=x['id'],format='metadata',metadataHeaders=['Date','From','Subject']).execute()
        #print(msg)
        snippet.append(msg['snippet'])
        ids.append(x['id'])
        headers = msg['payload']['headers']
        sender.append(getFrom(headers,'From'))
        subject.append(getFrom(headers,'Subject')[:40])
        date.append(getFrom(headers,'Date'))
    return JsonResponse({'sender':sender,'subject':subject,'verified':True, 'id':ids,'snippet':snippet,'date':date,'lb':labels,'repeat':repeat})
def Trash(request):
    service = builder(request)
    response = service.users().messages().trash(userId='me',id=request.GET.get('id',None))
    return JsonResponse({'verified':True})
def MUNREAD(request):
    service = builder(request)
    msg_labels={"removeLabelIds": ["UNREAD"]}
    message = service.users().messages().modify(userId='me', id=request.GET.get('id',None), body=msg_labels).execute()
    return JsonResponse({'verified':True})
def STARRED(request):
    service = builder(request)
    msg_labels={"addLabelIds": ["STARRED"]}
    message = service.users().messages().modify(userId='me', id=request.GET.get('id',None), body=msg_labels).execute()
    return JsonResponse({'verified':True})
def mailList(request):
    repeat = request.GET.get('repeat','')
    labels=request.GET.get('label','SENT')
    if(request.GET.get('fora','no')=='no' ):
        labels = labels[2:]
    service = builder(request)
    results = service.users().messages().list(userId='me',maxResults=10,labelIds=labels).execute()
    read = []
    sender = []
    subject = []
    ids=[]
    lids=[]
    snippet = []
    date = []
    messages = results.get('messages',[])
    for x in messages:
        msg = service.users().messages().get(userId='me',id=x['id'],format='metadata',metadataHeaders=['Date','From','Subject']).execute()
        #print(msg)
        
        if 'UNREAD' in msg['labelIds']:
            read.append(True)
        else:
            read.append(False)
        snippet.append(msg['snippet'])
        ids.append(x['id'])
        headers = msg['payload']['headers']
        sender.append(getFrom(headers,'From'))
        subject.append(getFrom(headers,'Subject')[:40])
        date.append(getFrom(headers,'Date'))
    return JsonResponse({'sender':sender,'subject':subject,'verified':True, 'id':ids,'snippet':snippet,'date':date,'lb':labels,'repeat':repeat,'read':read})
def Content(request):

    service=builder(request)
    message = service.users().messages().get(userId='me',id = request.GET.get('ida',[])).execute()
    """
    
    
    payld = message['payload'] 
    headr = payld['headers']
    print(headr)
    mssg_parts = payld['parts'] # fetching the message parts
    part_one  = mssg_parts[0] # fetching first element of the part 
    part_body = part_one['body'] # fetching body of the message
    part_data = part_body['data'] # fetching data from the body
    clean_one = part_data.replace("-","+") # decoding from Base64 to UTF-8
    clean_one = clean_one.replace("_","/") # decoding from Base64 to UTF-8
    clean_two = base64.b64decode (bytes(clean_one, 'UTF-8'))                           
    labels=request.GET.get('ida',None)
    service = builder(request)
    sender = []
    chara = []
    subject = []
    ids=[]
    msg = service.users().messages().get(userId='me',id=labels,format='raw').execute()
    print(msg)
    content = msg['raw']
    'sender':sender,'subject':subject,
    """
    data = {'verified':True, 'text': message}
    """
    #for x in msg['payload']['parts']:
    #    print(base64.b64decode(x['body']['data']))"""
    return JsonResponse(data)
            #print ('An error occurred: %s' % error)
def getBody(request):
    service.users().messages().get(userId='me',id=request.GET.get('label',None)).execute()
def Compose(request):
    query = SessId.objects.get(session = session_id(request))
    field_object = SessId._meta.get_field('access_code')
    access_code = field_object.value_from_object(query) 
    url = "https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token="+access_code
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    print(data)
    message = MIMEText(request.GET.get('Body',None))
    message['to'] = request.GET.get('To',None)
    message['subject'] = request.GET.get('Subject',None)
    {'raw': base64.urlsafe_b64encode(message.as_string())}
    send = (service.users().messages().send(userId='me', body=message)
               .execute())
    #Body = request.GET.get('Body',None)
    #print(To,Subject,Body)
    print(send)
    data = {'verified':True}
    return JsonResponse(data)
def Search(request):
    service=builder(request)
    message = service.users().messages().list(userId='me',q=request.GET.get('parameter','MAD'),maxResults=10).execute()
    print(message)
    try:
        o = message['messages']
    except:
        return JsonResponse({'verified':False})
    a = []
    sn = []
    for x in message['messages']:
        msg = service.users().messages().get(userId='me',id=x['id'],format='metadata',metadataHeaders=['From','Subject']).execute()
        pld = msg['payload']
        headers = pld['headers']
        a.append(getFrom(headers,'From'))
        sn.append(msg['snippet'])
    print(a)
    data= {'text':a,'verified':True,'snippet':sn}
    return JsonResponse(data)
# P FOR PINNED EMAILS
"""
def AddWid(request):
    print(request.GET.get('parameter',None))
    new_entry = Wids(session = session_id(request),widgets=request.GET.get('type',None),remarks=request.GET.get('parameter',None))
    new_entry.save()
    return JsonResponse({'verified':True})

def GetWids(request):
    query = Wids.objects.filter(session = session_id(request))
    if len(query)==0:
        return JsonResponse({'verified':False})
    wids = []
    rem = []
    for x in query:
        wids.append(x.widgets) 
        rem.append(x.remarks)
    print(wids,rem)
    return JsonResponse({'verified':True,'wids':wids,'remarks':rem})
"""
def Test(request):
    service=builder(request)
    result = service.users().messages().list(userId='me',maxResults=10, q='from:'+request.GET.get('parameter','computer.guybuilder@gmail.com'),fields='resultSizeEstimate').execute()
    return JsonResponse({'verified':True,'count':result.get('resultSizeEstimate')})
def DP(request):
    """
    service=builder(request)
    people_resource = service.people()
    people_document = people_resource.get(userId='me').execute()
    """
    return JsonResponse({'data':pbuilder(request)},safe=False)
def getEmails(request):
    service=builder(request)
    page_token = None
    a = []
    while(len(a)<11):
        messages = []
        mess = service.users().messages().list(userId='me',labelIds=['UNREAD']).execute()
        
        for x in mess['messages']:
            #print(x)
            response = service.users().messages().get(userId='me', id=x['id'],format='metadata',metadataHeaders=['From'],fields='payload').execute()
            if response['payload']['headers'][0]['value'] not in a:
                a.append(response['payload']['headers'][0]['value'])
                print('yes')
        print(a)
    return JsonResponse({'data':a})
def Widgets(request):
    service = builder(request)
    return render(request,'wids.html')
