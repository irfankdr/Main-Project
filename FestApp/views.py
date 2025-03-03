from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from FestApp.models import *


def login(request):
    return render(request,'index.html')


def logincode(request):

        username = request.POST['username']
        password = request.POST['password']
        ob = login_table.objects.get(username=username,password=password)
        if ob.type =='admin':
             return HttpResponse('''<script>alert('welcome');window.location='/judge_home';</script>''')
        elif ob.type =='event_co':
             request.session['lid']=ob.id
             return HttpResponse('''<script>alert('welcome');window.location='/event_co_home';</script>''')
        else:
            return HttpResponse('''<script>alert('Invalid');window.location='/login';</script>''')


def event_co_home(request):
    return render(request, 'event_co_index.html')




def clgregister(request):
    return render(request, 'clgreg.html')




def judge_home(request):
    return render(request, 'judge_home/index.html')


def eventreg(request):
    return render(request,'Reg EveOrg.html')



def clgregisterpost(request):
    name=request.POST['textfield']
    place=request.POST['textfield2']
    image=request.FILES['file']
    fs=FileSystemStorage()
    fn=fs.save(image.name,image)
    email=request.POST['textfield3']
    phone=request.POST['textfield4']
    username=request.POST['textfield5']
    password=request.POST['textfield6']
    ob=login_table()
    ob.username=username
    ob.password=password
    ob.type="event_co"
    ob.save()
    ob1=eventorganizer_table()
    ob1.LOGIN=ob
    ob1.name=name
    ob1.place=place
    ob1.image=fn
    ob1.email=email
    ob1.phone=phone
    ob1.save()
    return HttpResponse('''<script>alert('Invalid');window.location='/'</script>''')


def create_event(request):
    return render(request,'EventCreate.html')

def create_program(request):
    return render(request,'PrgrmCreate.html')

def verifyeventco(request):
    ob=eventorganizer_table.objects.all()
    return render(request,'verify event.html',{"val":ob})


def addevent(request):
    return render(request,'event/Form2 Event.html')


def addevent_post(request):
    name=request.POST['textfield']
    place=request.POST['textfield2']
    phone=request.POST['textfield3']
    lati=request.POST['textfield4']
    longi=request.POST['textfield5']
    kk=event_table()
    kk. eventorganizer=eventorganizer_table.objects.get(LOGIN__id=request.session['lid'])
    kk. name=name
    kk.place=place
    kk.phone=phone
    kk.latitude=lati
    kk.longitude=longi
    kk.save()
    return HttpResponse('''<script>alert('added');window.location='/manageevent'</script>''')


def manageevent(request):
    ob=event_table.objects.filter(eventorganizer__LOGIN__id=request.session['lid'])
    return render(request,'event/form5 admin event.html',{"val":ob})