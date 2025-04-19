import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import datetime

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import *
import base64
# Create your views here.



from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from web3 import Web3, HTTPProvider, contract
import qrcode
import json
# truffle development blockchain address
blockchain_address = 'http://127.0.0.1:7545'
# Client instance to interact with the blockchain
web3 = Web3(HTTPProvider(blockchain_address))
# Set the default account (so we don't need to set the "from" for every transaction call)
web3.eth.defaultAccount = web3.eth.accounts[0]
compiled_contract_path = r"C:\BlockChain\node_modules\.bin\build\contracts\Structreq.json"
# Deployed contract address (see migrate command output: contract address)
deployed_contract_address = '0xC2e70C40bb23b55e44245FD6d650D71f68711844'








festhub_email = ""
festhub_password = ""



def log(request):
    return render(request,"login.html")

def logpost(request):
    un=request.POST['textfield']
    ps=request.POST['textfield2']
    res=login.objects.filter(username=un,password=ps)
    if res.exists():
        res=res[0]
        request.session['lid']=res.id

        request.session['lg']="lin"
        request.session['head'] = ""
        if res.usertype == 'admin':
            return HttpResponse("<script>alert('Login successful');window.location='/admin_home'</script>")
        elif res.usertype == "event_organizer":
            return HttpResponse("<script>alert('Login successful');window.location='/organizer_home'</script>")
        elif res.usertype == "college":
            return HttpResponse("<script>alert('Login successful');window.location='/college_home'</script>")
        elif res.usertype == "judge":
            return HttpResponse("<script>alert('Login successful');window.location='/judge_home'</script>")
        elif res.usertype == "staff":
            return HttpResponse("<script>alert('Login successful');window.location='/staff_home'</script>")
        else:

            return HttpResponse("<script>alert('Login Success');window.location='/'</script>")
    return HttpResponse("<script>alert('inavlid');window.location='/'</script>")


def admin_home(request):
    return render(request, "admin/admin_index.html")

def organizer_home(request):
    return render(request,"event_organiser/organiser_index.html")

def college_home(request):
    return render(request, "college/collge_index.html")

def staff_home(request):
    return render(request,"staff/staff_index.html")

def judge_home(request):
    return render(request,"judge/judge_index.html")


def logout(request):
    return HttpResponse("<script>alert('Logout success');window.location='/'</script>")


# -------------------------------- ADMIN  ----------------------------------


def viewandverifyevent(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "view event organizer"
    data = event_organizer.objects.all()
    return render(request, "admin/view_and_verify_event.html", {"data":data})


def approve_event_organizer(request,id):
    login.objects.filter(id=id).update(usertype='event_organizer')
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login(festhub_email, festhub_password)
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("FestHub  verified your account. Please Login for more details!!!")
    msg['Subject'] = 'Verification'
    msg['To'] = login.objects.filter(id=id)[0].username
    msg['From'] = festhub_email
    try:
        gmail.send_message(msg)
    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))
    return HttpResponse('<script>alert("approved..check your email");window.location="/view_verified_event_organizer#abc"</script>')

def reject_organizer(request,id):
    login.objects.filter(id=id).update(usertype='reject')
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login(festhub_email, festhub_password)
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("FestHub  verified your account. Please Login for more details!!!")
    msg['Subject'] = 'Verification'
    msg['To'] = login.objects.filter(id=id)[0].username
    msg['From'] = festhub_email
    try:
        gmail.send_message(msg)
    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))
    return HttpResponse('<script>alert("Rejected..check your email");window.location="/viewandverifyevent#abc"</script>')


def view_verified_event_organizer(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "view  verified event organizer"
    data = event_organizer.objects.filter(LOGIN__usertype='event_organizer')
    return render(request, "admin/view verified event.html", {"data":data})


def admin_view_program(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "view Program"
    data = program.objects.all()
    return render(request,"admin/view_program.html",{"data":data})


def admin_view_judge(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "view Judge"
    data = judge.objects.all()
    return render(request, "admin/view_judge.html", {"data": data})


def admin_view_event(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "view event"
    data = event.objects.all()
    return render(request, "admin/view_event.html", {"data": data})

def admin_view_staff(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "view staff"
    data = staff.objects.all()
    return render(request,"admin/view_staff.html",{"data":data})


#------------------------------------ EVENT ORGANIZER -----------------

def register_eventorganiser(request):
    return render(request,"event_organiser/register.html")

def register_eventorganiser_post(request):
    name = request.POST['textfield']
    email = request.POST['textfield2']
    contact = request.POST['textfield3']
    place = request.POST['textfield7']
    image = request.FILES['fileField']
    dt = datetime.now().strftime("%Y%m%d-%H%M%S")
    fs = FileSystemStorage()
    fs.save(r"C:\Users\irfan vk\PycharmProjects\Fest_Hub\media\image\\"+dt+'.jpg',image)
    #  fs.save(r"C:\Users\irfan vk\Downloads\Fest_Hub\\",image)
    path = '/media/image/'+dt+'.jpg'
    designation = request.POST['textfield4']
    password = request.POST['textfield5']
    confirm_password = request.POST['textfield6']

    data = login.objects.filter(username=email)
    if data.exists():
        return HttpResponse("<script>alert('Already Exists');window.location='/register_eventorganiser'</script>")
    elif password == confirm_password:
        obj = login()
        obj.username = email
        obj.password = password
        obj.usertype = 'pending'
        obj.save()

        obj1 = event_organizer()
        obj1.name = name
        obj1.contact = contact
        obj1.place = place
        obj1.image = path
        obj1.designation = designation
        obj1.LOGIN = obj
        obj1.save()
        return HttpResponse("<script>alert('Success');window.location='/'</script>")
    else:
        return HttpResponse("<script>alert('password mismatch');window.location='/register_eventorganiser'</script>")




# -- COLLEGE MANAGEMENT --------

def add_college(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "Add college"
    return render(request,"event_organiser/add_college.html")


def add_college_post(request):
    name = request.POST['name']
    place = request.POST['place']
    phone = request.POST['phone']
    Email = request.POST['Email']
    # Latitude = request.POST['Latitude']
    # Longitude = request.POST['Longitude']

    data = login.objects.filter(username=Email)
    if data.exists():
        return HttpResponse("<script>alert('Already Existss');window.location='/add_college'</script>")
    else:
        pwd = random.randint(0000,9999)

        obj1 = login()
        obj1.username = Email
        obj1.usertype = "college"
        obj1.password = pwd
        obj1.save()

        obj = college()
        obj.name = name
        obj.place = place
        obj.contact = phone
        obj.email = Email
        obj.EVENT_ORGANIZER = event_organizer.objects.get(LOGIN__id=request.session['lid'])

        obj.latitude = "0.0"
        obj.longitude = "0.0"
        obj.LOGIN_id = obj1.id
        obj.save()

        # import smtplib
        # s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        # s.starttls()
        # s.login("demo@gmail.com", "smart@789")
        # msg = MIMEMultipart()  # create a message.........."
        # msg['From'] = "demo@gmail.com"
        # msg['To'] = Email
        # msg['Subject'] = "Your Password for College registering.."
        # body = "Your Password is:- - " + str(pwd)
        # msg.attach(MIMEText(body, 'plain'))
        # s.send_message(msg)

        return HttpResponse("<script>alert('Success');window.location='/add_college'</script>")



def view_college(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "view College"
    data = college.objects.filter(EVENT_ORGANIZER__LOGIN=request.session['lid'])
    return render(request,"event_organiser/view_college.html",{"data":data})


def edit_college(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "Edit College"
    data = college.objects.get(id=id)
    return render(request,"event_organiser/edit_college.html",{"data":data,"id":id})


def edit_college_post(request,id):
    name = request.POST['name']
    place = request.POST['place']
    phone = request.POST['phone']
    Email = request.POST['Email']
    Latitude = request.POST['Latitude']
    Longitude = request.POST['Longitude']
    college.objects.filter(id=id).update(name = name,place = place,contact = phone,email = Email,latitude = Latitude,longitude = Longitude)

    return HttpResponse("<script>alert('Updated');window.location='/view_college'</script>")



def delete_college(request,id):
    college.objects.get(id=id).delete()
    return HttpResponse("<script>alert('Removed');window.location='/view_college'</script>")



#----- MANAGE JUDGE ---------


def add_judge(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "Add Judge"
    return render(request,"event_organiser/add_judge.html")


def add_judge_post(request):
    name = request.POST['textfield3']
    email = request.POST['textfield4']
    contact = request.POST['textfield5']
    expertise = request.POST['textfield6']
    designation = request.POST['textfield7']

    data = login.objects.filter(username=email)
    if data.exists():
        return HttpResponse("<script>alert('Already Added');window.location='/add_judge'</script>")
    else:

        obj = login()
        obj.username = email
        obj.password = random.randint(0000,9999)
        obj.usertype = 'judge'
        obj.save()

        obj1 = judge()
        obj1.name = name
        obj1.email = email
        obj1.contact = contact
        obj1.expertise = expertise
        obj1.designation = designation
        obj1.EVENT_ORGANIZER = event_organizer.objects.get(LOGIN=request.session['lid'])
        obj1.LOGIN = obj
        obj1.save()

        # import smtplib
        # s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        # s.starttls()
        # s.login("demo@gmail.com", "smart@789")
        # msg = MIMEMultipart()  # create a message.........."
        # msg['From'] = "demo@gmail.com"
        # msg['To'] = Email
        # msg['Subject'] = "Your Password for College registering.."
        # body = "Your Password is:- - " + str(pwd)
        # msg.attach(MIMEText(body, 'plain'))
        # s.send_message(msg)
        return HttpResponse("<script>alert('Success');window.location='/add_judge'</script>")


def view_judge(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "view Judge"
    data = judge.objects.filter(EVENT_ORGANIZER__LOGIN=request.session['lid'])
    return render(request,"event_organiser/view_judge.html",{"data":data})


def edit_judge(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "Edit Judge"
    data = judge.objects.get(id=id)
    return render(request,"event_organiser/edit_judge.html",{"data":data,"id":id})

def edit_judge_post(request,id):
    name = request.POST['textfield3']
    email = request.POST['textfield4']
    contact = request.POST['textfield5']
    expertise = request.POST['textfield6']
    designation = request.POST['textfield7']

    judge.objects.filter(id=id).update(name = name,email = email,contact = contact,expertise = expertise,designation = designation)
    return HttpResponse("<script>alert('Updated');window.location='/view_judge'</script>")


def delete_judge(request,id):
    judge.objects.get(id=id).delete()
    return HttpResponse("<script>alert('Updated');window.location='/view_judge'</script>")



# ---- MANAGE PROGRAM ----------

def add_program(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "Add Program"
    ev = event.objects.get(id=request.session['eid'])
    fdate=ev.start_date
    tdate=ev.end_date
    return render(request,"event_organiser/add_program.html",{"fdate":str(fdate),"tdate":str(tdate)})





def add_program_post(request):
    start_time = request.POST['textfield']
    end_time = request.POST['textfield2']
    name = request.POST['textfield3']
    date = request.POST['date']
    descr = request.POST['textarea']
    category = request.POST['textfield4']
    stage_no = request.POST['textfield6']
    stage_lati = request.POST['textfield7']
    stage_longi = request.POST['textfield8']

    data = program.objects.filter(start_time = start_time,end_time = end_time,name = name)
    if data.exists():
        return HttpResponse("<script>alert('Already Added');window.location='/add_program'</script>")
    else:

        obj = program()
        obj.start_time = start_time
        obj.end_time = end_time
        obj.name = name
        obj.description = descr
        obj.category = category
        # obj.rounds = rounds
        obj.stage_no = stage_no
        obj.stage_latitude = stage_lati
        obj.stage_longitude = stage_longi
        obj.date = date
        obj.EVENT_ORGANIZER = event.objects.get(id=request.session['eid'])
        obj.save()
        return HttpResponse("<script>alert('Updated');window.location='/add_program'</script>")

def view_program(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    data = program.objects.filter(EVENT_ORGANIZER__id=id)
    request.session["eid"]=id
    return render(request,"event_organiser/view_program.html",{"data":data})



def edit_program(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "Edit Program"
    data = program.objects.get(id=id)
    return render(request,"event_organiser/edit_program.html",{"data":data,"id":id})


def edit_program_post(request,id):
    start_time = request.POST['textfield']
    end_time = request.POST['textfield2']
    name = request.POST['textfield3']
    descr = request.POST['textarea']
    category = request.POST['textfield4']

    date = request.POST['date']
    stage_no = request.POST['textfield6']
    stage_lati = request.POST['textfield7']
    stage_longi = request.POST['textfield8']

    program.objects.filter(id=id).update(start_time = start_time,end_time = end_time,name = name,
                                         description = descr,category = category,date=date,stage_no=stage_no,stage_latitude=stage_lati,stage_longitude=stage_longi)
    return HttpResponse("<script>alert('Updated');window.location='/view_program'</script>")

def delete_program(request,id):
    program.objects.get(id=id).delete()
    return HttpResponse("<script>alert('Removed');window.location='/view_program'</script>")


# ---- MANAGE EVENT -----


def add_event(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "add event"
    a=judge.objects.all()
    return render(request,"event_organiser/add_event.html",{"data":a})


def add_event_post(request):
    start_date = request.POST['sdate']
    end_date = request.POST['edate']
    start_time = request.POST['textfield']
    end_time = request.POST['textfield2']
    name = request.POST['textfield3']
    descr = request.POST['textarea']
    category = request.POST['textfield4']
    v = request.POST['v']

    obj = event()
    obj.start_date =start_date
    obj.end_date = end_date
    obj.start_time = start_time
    obj.end_time = end_time
    obj.status = "pending"
    obj.name = name
    obj.description = descr
    obj.category = category
    obj.venue = v
    # obj.JUDGE_id = id
    obj.EVENT_ORGANIZER = event_organizer.objects.get(LOGIN=request.session['lid'])
    obj.save()
    return HttpResponse("<script>alert('Success');window.location='/add_event'</script>")

def view_event(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "view event"
    data = event.objects.filter(EVENT_ORGANIZER__LOGIN=request.session['lid'])
    return render(request,"event_organiser/view_event.html",{"data":data})


def view_event_allocation(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['jud_id'] =id
    request.session['head'] = "view event"
    data = event.objects.all()
    return render(request,"event_organiser/allocate_judge.html",{"data":data})




def edit_event(request,id):
    request.session['eid']=id
    a=event.objects.get(id=id)
    return render(request,"event_organiser/edit_event.html",{"data":a})


def edit_event_post(request):
    start_time = request.POST['textfield']
    end_time = request.POST['textfield2']
    name = request.POST['textfield3']
    descr = request.POST['textarea']
    category = request.POST['textfield4']

    obj = event.objects.get(id= request.session['eid'])
    obj.start_time = start_time
    obj.end_time = end_time
    obj.status = "pending"
    obj.name = name
    obj.description = descr
    obj.category = category
    # obj.JUDGE_id = id
    obj.EVENT_ORGANIZER = event_organizer.objects.get(LOGIN=request.session['lid'])
    obj.save()
    return HttpResponse("<script>alert('Success');window.location='/add_event'</script>")


def delete_event(request,id):
    event.objects.get(id=id).delete()
    return HttpResponse("<script>alert('Removed');window.location='/view_event'</script>")



def allocate_programs(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "allocate program"
    data = program.objects.filter(EVENT_ORGANIZER__EVENT_ORGANIZER__LOGIN=request.session['lid'],EVENT_ORGANIZER__id=id)
    return render(request,"event_organiser/allocate_program.html",{"data":data,"id":id})

def allocate_program_post(request):
    programs = request.POST['select']
    print(request.session['jud_id'],"jjjjjjjjjjjjjjjjj")
    data = allocate_program.objects.filter(PROGRAM_id = programs,JUDGE_id = request.session['jud_id'])
    if data.exists():
        return HttpResponse("<script>alert('Program already allocated');window.location='/view_judge'</script>")
    else:
        obj = allocate_program()
        obj.PROGRAM_id = programs
        obj.JUDGE = judge.objects.get(id=request.session['jud_id'])
        obj.save()
        return HttpResponse("<script>alert('Program allocated');window.location='/view_judge'</script>")



# ---------- COLLEGE MODULE  ------------------------#

def view_and_update_profile(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "manage profile"
    data = college.objects.get(LOGIN = request.session['lid'])
    return render(request,"college/view_and_edit_profile.html",{"data":data})

def view_and_update_profile_post(request):
    name = request.POST['name']
    place = request.POST['place']
    phone = request.POST['phone']
    Email = request.POST['Email']
    Latitude = request.POST['Latitude']
    Longitude = request.POST['Longitude']
    college.objects.filter(LOGIN= request.session['lid']).update(name=name,email=Email,contact=phone,latitude=Latitude,longitude=Longitude,place=place)
    return HttpResponse("<script>alert('Profile Updated');window.location='/view_and_update_profile'</script>")


# --- STAFF MANAGEMENT ----


def add_staff(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "add staff"
    return render(request,"college/add_staff.html")

def add_staff_post(request):
    name = request.POST['textfield']
    email = request.POST['textfield2']
    contact = request.POST['textfield3']
    place = request.POST['textfield7']
    designation = request.POST['textfield4']

    data = login.objects.filter(username=email)
    if data.exists():
        return HttpResponse("<script>alert('Staff already Exists');window.location='/add_staff'</script>")
    else:
        pwd = random.randint(0000,9999)

        obj = login()
        obj.username  = email
        obj.password = pwd
        obj.usertype = 'staff'
        obj.save()


        obj1 = staff()
        obj1.name = name
        obj1.email = email
        obj1.contact = contact
        obj1.place = place
        obj1.designation = designation
        obj1.LOGIN = obj
        obj1.COLLEGE = college.objects.get(LOGIN=request.session['lid'])
        obj1.save()

        # import smtplib
        # s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        # s.starttls()
        # s.login("demo@gmail.com", "smart@789")
        # msg = MIMEMultipart()  # create a message.........."
        # msg['From'] = "demo@gmail.com"
        # msg['To'] = Email
        # msg['Subject'] = "Your Password for College registering.."
        # body = "Your Password is:- - " + str(pwd)
        # msg.attach(MIMEText(body, 'plain'))
        # s.send_message(msg)
        return HttpResponse("<script>alert('Success');window.location='/add_staff'</script>")


def view_staff(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "view staff"
    data = staff.objects.filter(COLLEGE__LOGIN=request.session['lid'])
    return render(request,"college/view_staff.html",{"data":data})


def edit_staff(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "Edit staff"
    data = staff.objects.get(id=id)
    return render(request,"college/edit_staff.html",{"data":data,"id":id})


def edit_staff_post(request,id):
    name = request.POST['textfield']
    email = request.POST['textfield2']
    contact = request.POST['textfield3']
    place = request.POST['textfield7']
    designation = request.POST['textfield4']
    staff.objects.filter(id=id).update(name=name,email=email,contact=contact,place=place,designation=designation)
    return HttpResponse("<script>alert('Updated');window.location='/view_staff'</script>")


def delete_staff(request,id):
    staff.objects.get(id=id).delete()
    return HttpResponse("<script>alert('Deleted');window.location='/view_staff'</script>")


def college_view_event(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "view event"
    data  = event.objects.all()
    return render(request,"college/view_event.html",{"data":data})





def college_view_program(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "view program"
    data  = program.objects.filter(EVENT_ORGANIZER__id=id)
    return render(request,"college/view_program.html",{"data":data})





def view_result(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "view result"
    data = result.objects.filter(PROGRAM_id=id)
    return render(request,"college/view_result.html",{"data":data})


def assign_works(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "Assign work"
    return render(request,"college/assign_work.html",{"id":id})

def assign_work_post(request,id):
    works = request.POST['textfield']
    data = assign_work.objects.filter(works=works,STAFF_id=id)
    if data.exists():
        return HttpResponse("<script>alert('Work already  assigned');window.location='/view_staff'</script>")
    else:
        obj = assign_work()
        obj.works = works
        obj.status = 'pending'
        obj.STAFF_id = id
        obj.COLLEGE = college.objects.get(LOGIN=request.session['lid'])
        obj.save()
        return HttpResponse("<script>alert('Work assigned');window.location='/view_staff'</script>")


def view_staff_work_status(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "view staff work status"
    data = assign_work.objects.filter(status='completed',STAFF_id=id)
    return render(request,"college/view_staff_work_status.html",{"data":data})




# ---------------------------- STAFF ----------------------------------------


def staff_view_and_edit_profile(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "Manage Profile"
    data = staff.objects.get(LOGIN=request.session['lid'])
    return render(request,"staff/view_and_edit_profile.html",{"data":data})


def staff_view_and_edit_profile_post(request):
    name = request.POST['textfield']
    email = request.POST['textfield2']
    contact = request.POST['textfield3']
    place = request.POST['textfield7']
    designation = request.POST['textfield4']
    staff.objects.filter(LOGIN=request.session['lid']).update(name=name,email=email,contact=contact,place=place,designation=designation)
    return HttpResponse("<script>alert('Profile Updated');window.location='/staff_view_and_edit_profile'</script>")



#- STUDENT MANAGEMENT ---


def add_student(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "Add student"
    return render(request, "staff/add_student.html")


def add_student_post(request):
    name = request.POST['name']
    place = request.POST['place']
    phone = request.POST['phone']
    email = request.POST['Email']
    dept = request.POST['dept']
    year = request.POST['year']


    uploaded_file = request.FILES.get('fileField')
    print(uploaded_file, "pppppppppppppppppp")
    if uploaded_file:
        try:
            # Save the file in the MEDIA_ROOT directory
            with open(f'media/uploads/{uploaded_file.name}', 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
        except Exception as e:
            pass

    data =login.objects.filter(username=email)
    if data.exists():
        return HttpResponse("<script>alert('Already Exists');window.location='/add_student'</script>")
    else:
        pwd = random.randint(0000,9999)

        obj1 = login()
        obj1.username = email
        obj1.password = pwd
        obj1.usertype = 'student'
        obj1.save()

        obj = student()
        obj.name = name
        obj.email = email
        obj.contact = phone
        obj.department = dept
        obj.year = year
        obj.place = place
        obj.image = f'media/uploads/{uploaded_file.name}'
        obj.LOGIN = obj1
        obj.STAFF = staff.objects.get(LOGIN=request.session['lid'])
        obj.save()
        return HttpResponse("<script>alert('Success');window.location='/add_student'</script>")

def view_student(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "view student"
    data = student.objects.filter(STAFF__LOGIN=request.session['lid'])
    return render(request, "staff/view_student.html", {"data":data})


def add_result(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['pid']=id
    ob=program_request.objects.filter(PROGRAM__id=id)

    return render(request, "judge/upload_result1.html", {"data":ob})


def edit_student(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "Edit Student"
    data = student.objects.get(id=id)
    return render(request, "staff/edit_student.html", {"data":data, "id":id})

def edit_student_post(request,id):
    name = request.POST['name']
    place = request.POST['place']
    phone = request.POST['phone']
    email = request.POST['Email']
    dept = request.POST['dept']
    year = request.POST['year']
    uploaded_file = request.FILES.get('fileField')
    print(uploaded_file, "pppppppppppppppppp")
    if uploaded_file:
        try:
            # Save the file in the MEDIA_ROOT directory
            with open(f'media/uploads/{uploaded_file.name}', 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
        except Exception as e:
            pass


    student.objects.filter(id=id).update(name = name,email = email,contact = phone,department = dept,year = year,place = place,image=f'media/uploads/{uploaded_file.name}')
    return HttpResponse("<script>alert('Updated');window.location='/view_student'</script>")


def delete_student(request,id):
    student.objects.get(id=id).delete()
    return HttpResponse("<script>alert('Removed');window.location='/view_student'</script>")




def view_program_request(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "view program request"
    data = program_request.objects.filter(STUDENT_id=id,status='pending')
    return render(request,"staff/view_program_request.html",{"data":data})


def update_student_request(request,id):
    program_request.objects.filter(id=id).update(status='updated')
    return HttpResponse("<script>alert('Updated');window.location='/view_program_request/"+id+"'</script>")



def staff_view_assigned_work(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "view assigned work"
    data = assign_work.objects.filter(STAFF__LOGIN=request.session['lid'])
    return render(request,"staff/view_assigned_work.html",{"data":data})


def update_work_status(request,id):
    assign_work.objects.filter(id=id).update(status='completed')
    return HttpResponse("<script>alert('Work completed');window.location='/staff_view_assigned_work'</script>")



def staff_view_result(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "view result"
    data = result.objects.filter(STUDENT_id=id)
    return render(request,"staff/view_result.html",{"data":data})


def staff_view_point(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "view point"
    data = point.objects.filter(STUDENT_id=id)
    return render(request,"staff/view_points.html",{"data":data})


def send_notification(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "send notification"
    return render(request,"staff/send_notification.html")

def send_notification_post(request):
    notifications = request.POST['textarea']
    obj = notification()
    obj.notifications = notifications
    obj.date = datetime.datetime.now().date()
    obj.STAFF = staff.objects.get(LOGIN=request.session['lid'])
    obj.save()
    return HttpResponse("<script>alert('Sended');window.location='/staff_home'</script>")



# ------------------------------------- JUDGE -------------------

def judge_view_and_edit_profile(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "manage profile"
    data = judge.objects.get(LOGIN=request.session['lid'])
    return render(request,"judge/view_and_edit_profile.html",{"data":data})

def judge_view_and_edit_profile_post(request):
    name = request.POST['textfield3']
    email = request.POST['textfield4']
    contact = request.POST['textfield5']
    expertise = request.POST['textfield6']
    designation = request.POST['textfield7']
    judge.objects.filter(LOGIN=request.session['lid']).update(name=name,email=email,contact=contact,expertise=expertise,designation=designation)
    return HttpResponse("<script>alert('Profile updated');window.location='/judge_view_and_edit_profile'</script>")


def judge_view_assigned_work(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "Assigned work"
    data = allocate_program.objects.filter(JUDGE__LOGIN=request.session['lid'])
    return render(request,"judge/view_assigned_work.html",{"data":data})

def upload_result(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "Upload result"
    data = allocate_program.objects.filter(JUDGE__LOGIN__id=request.session['lid'])

    return render(request,"judge/upload_result.html",{"data":data})

def upload_result_post(request):
    id=request.session['pid']
    ob = program_request.objects.filter(PROGRAM__id=id)
    for i in ob:
        obj = result()
        obj.STUDENT_id =i.STUDENT.id
        obj.PROGRAM_id = id
        obj.JUDGE = judge.objects.get(LOGIN=request.session['lid'])
        obj.result =  request.POST["p"+str(i.STUDENT.id)]
        obj.grade =  request.POST[str(i.STUDENT.id)]
        obj.save()
        # blocknumber = web3.eth.get_block_number()
        # # try:
        # message2 = contract.functions.addreq(blocknumber + 1,
        #                                      str(obj.result), str(obj.grade), str(obj.PROGRAM_id.id), str(obj.STUDENT_id.id), str(obj.JUDGE.id),
        #                                      str(obj.id), 'shop request'
        #                                      ).transact({'from': web3.eth.accounts[0]})
        # # except Exception as e:
        # #     print(e, "========================================")
        # #     print(e, "========================================")
        # #     print(e, "")
        # #
        k=obj.PROGRAM_id
        s=obj.STUDENT_id
        j=obj.JUDGE.id
        with open(
                r'C:\BlockChain\node_modules\.bin\build\contracts\Structreq.json') as file:
            contract_json = json.load(file)  # load contract info as JSON
            contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
        contract = web3.eth.contract(address='0xC2e70C40bb23b55e44245FD6d650D71f68711844', abi=contract_abi)
        blocknumber = web3.eth.get_block_number()
        message2 = contract.functions.addreq(blocknumber + 1,
                                             str(obj.result), str(obj.grade), str(k), str(s), str(j),
                                             ).transact({"from": web3.eth.accounts[0]})

        # data = {'task': 'success'}
        # r = json.dumps(data)
        # return HttpResponse(r)

    return HttpResponse("<script>alert('result uploaded');window.location='/upload_result'</script>")





# ------------------------------ STUDENT(Flutter) -----------------------------------------------

def student_login(request):
    un=request.POST['user_name']
    pass3=request.POST['password']
    res=login.objects.filter(username=un,password=pass3,usertype="student")
    if res.exists():
        res=res[0]
        return JsonResponse({"status":"ok","lid":res.id})
    return JsonResponse({"status":"no"})

def student_view_profile(request):
    lid=request.POST['lid']
    data = student.objects.get(LOGIN=lid)


    return JsonResponse({
        "id": str(data.id),
        "Name": str(data.name),
        "phone": str(data.contact),
        "year": str(data.year),
        "place":str(data.place),
        "department": str(data.department),
        "photo": str(data.image),
        "Email": str(data.email)
    })


def student_view_event(request):
    res = event.objects.all()
    ar = []
    for i in res:
        ar.append({
            "id": i.id,
            "start_time": i.start_time,
            "end_time": i.end_time,
            "date": i.start_date,
            "status": i.status,
            "name": i.name,
            "description": i.description,
            "category": i.category,


        })
    return JsonResponse({"status": "ok", "data": ar})



def student_view_program(request):
    eid=request.POST["eid"]
    res = program.objects.filter(EVENT_ORGANIZER__id=eid)
    ar = []
    for i in res:
        # start_time = models.CharField(max_length=100)
        # end_time = models.CharField(max_length=100)
        # name = models.CharField(max_length=100)
        # description = models.CharField(max_length=100)
        # category = models.CharField(max_length=100)
        # # rounds = models.CharField(max_length=100)
        # date = models.CharField(max_length=100)
        # stage_latitude = models.CharField(max_length=100)
        # stage_longitude = models.CharField(max_length=100)
        # stage_no = models.CharField(max_length=100)
        ar.append({
            "id": i.id,
            "start_time": i.start_time,
            "end_time": i.end_time,
            "name": i.name,
            "description": i.description,
            "category": i.category,
            "rounds": "",
            "date": i.date,
            "stage_no":i.stage_no,
            "stage_lati":i.stage_latitude,
            "stage_longi":i.stage_longitude

        })
    print(ar)
    return JsonResponse({"status": "ok", "data": ar})


def student_view_program_req(request):
    eid=request.POST["lid"]
    res = program_request.objects.filter(STUDENT__LOGIN__id=eid)
    ar = []
    for i in res:

        ar.append({
            "id": i.id,
            "start_time": i.PROGRAM.start_time,
            "end_time": i.PROGRAM.end_time,
            "name": i.PROGRAM.name,
            "description": i.PROGRAM.description,
            "category": i.PROGRAM.category,
            "rounds": "",
            "date": i.PROGRAM.date,
            "stage_no":i.PROGRAM.stage_no,
            "stage_lati":i.PROGRAM.stage_latitude,
            "stage_longi":i.status

        })
    return JsonResponse({"status": "ok", "data": ar})


def student_send_request(request):
    lid = request.POST['lid']
    pid = request.POST['pid']


    print("liddddddddddddd",lid)
    print("pidddddddddddddddd",pid)

    obj = program_request()
    obj.status = 'pending'
    obj.date = datetime.now().date()
    obj.PROGRAM_id = pid
    obj.STUDENT = student.objects.get(LOGIN=lid)
    obj.save()
    return JsonResponse({"status":"ok"})

def student_view_notification(request):
    res = notification.objects.all()
    ar = []
    for i in res:
        ar.append(
            {
                "id":i.id,
                "notification":i.notifications,
                "date":i.date
            }
        )
    return JsonResponse({"status":"ok","data":ar})


def student_view_result(request):
    lid = request.POST['lid']
    data = result.objects.filter(STUDENT__LOGIN=lid)
    ar = []
    for i in data:
        ar.append(
            {
                "id":i.id,
                "result":i.result+ " - "+i.grade,
                "program_name":i.PROGRAM.name,
                "program_category":i.JUDGE.name,
                "program_date":i.PROGRAM.date,
                "organiser_name":i.PROGRAM.EVENT_ORGANIZER.name
            }
        )
        print("arrrrrrrrrrrrrrrrrrrrr",ar)
    return JsonResponse({"status":"ok","data":ar})

def updatelocation(request):
    lid = request.POST['lid']
    res=get_upcoming_programs_for_user(lid)
    print(res)
    if len(res)>0:
        return JsonResponse({"task":"ok","data":"Sample"})
    return JsonResponse({"task":"na","data":"Sample"})



from .models import program, program_request
import pytz

# Set your local timezone (replace 'Your/Timezone' with the actual timezone)

def get_upcoming_programs_for_user(user):
    from django.utils import timezone
    from datetime import timedelta
    local_tz = pytz.timezone('Asia/Kolkata')
    # Get the current time
    current_time = timezone.now()
    current_time_utc = timezone.now()

    # Convert the current time to local timezone
    current_time_local = current_time_utc.astimezone(local_tz)

    # Calculate the time 5 minutes from now in local timezone
    five_minutes_later = current_time_local + timedelta(minutes=5)
    # Calculate the time 5 minutes from now
    # five_minutes_later = current_time + timedelta(minutes=5)
    four_minutes_later = current_time + timedelta(minutes=4)
    print(five_minutes_later)
    print(four_minutes_later)

    # Filter programs that start within the next 5 minutes for the given user
    upcoming_programs = program.objects.filter(
        date=datetime.now().strftime("%Y-%m-%d"),
        start_time__hour=five_minutes_later.hour,
        start_time__minute=five_minutes_later.minute,

        program_request__STUDENT__LOGIN__id=user
    )

    return upcoming_programs