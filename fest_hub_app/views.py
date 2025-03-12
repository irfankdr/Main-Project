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
    data = event_organizer.objects.filter(LOGIN__usertype='pending')
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
    dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    fs = FileSystemStorage()
    fs.save(r"C:\Users\irfan vk\Downloads\Fest_Hub\Fest_Hub\media\image\\"+dt+'.jpg',image)
    # fs.save(r"C:\Users\irfan vk\Downloads\Fest_Hub\\",image)
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
    Latitude = request.POST['Latitude']
    Longitude = request.POST['Longitude']

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

        obj.latitude = Latitude
        obj.longitude = Longitude
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
    return render(request,"event_organiser/add_program.html")


def add_program_post(request):
    start_time = request.POST['textfield']
    end_time = request.POST['textfield2']
    name = request.POST['textfield3']
    descr = request.POST['textarea']
    category = request.POST['textfield4']
    rounds = request.POST['textfield5']
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
        obj.rounds = rounds
        obj.stage_no = stage_no
        obj.stage_latitude = stage_lati
        obj.stage_longitude = stage_longi
        obj.date = datetime.datetime.now().date()
        obj.EVENT_ORGANIZER = event_organizer.objects.get(LOGIN=request.session['lid'])
        obj.save()
        return HttpResponse("<script>alert('Updated');window.location='/add_program'</script>")

def view_program(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "view Program"
    data = program.objects.filter(EVENT_ORGANIZER__LOGIN=request.session['lid'])
    return render(request,"event_organiser/view_program.html",{"data":data})



def edit_program(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "Edit Program"
    data = program.objects.get(id=id)
    return render(request,"event_organiser/Hm.html",{"data":data,"id":id})


def edit_program_post(request,id):
    start_time = request.POST['textfield']
    end_time = request.POST['textfield2']
    name = request.POST['textfield3']
    descr = request.POST['textarea']
    category = request.POST['textfield4']
    rounds = request.POST['textfield5']
    date = request.POST['textfield6']
    stage_no = request.POST['textfield6']
    stage_lati = request.POST['textfield7']
    stage_longi = request.POST['textfield8']

    program.objects.filter(id=id).update(start_time = start_time,end_time = end_time,name = name,
                                         description = descr,category = category,rounds = rounds,date=date,stage_no=stage_no,stage_latitude=stage_lati,stage_longitude=stage_longi)
    return HttpResponse("<script>alert('Updated');window.location='/view_program'</script>")

def delete_program(request,id):
    program.objects.get(id=id).delete()
    return HttpResponse("<script>alert('Removed');window.location='/view_program'</script>")


# ---- MANAGE EVENT -----


def add_event(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "add event"
    return render(request,"event_organiser/add_event.html",{"id":id})


def add_event_post(request,id):
    start_time = request.POST['textfield']
    en_time = request.POST['textfield2']
    name = request.POST['textfield3']
    descr = request.POST['textarea']
    category = request.POST['textfield4']

    obj = event()
    obj.start_time = start_time
    obj.end_time = en_time
    obj.status = "pending"
    obj.name = name
    obj.description = descr
    obj.category = category
    obj.JUDGE_id = id
    obj.EVENT_ORGANIZER = event_organizer.objects.get(LOGIN=request.session['lid'])
    obj.save()
    return HttpResponse("<script>alert('Success');window.location='/add_event/"+id+"'</script>")

def view_event(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "view event"
    data = event.objects.filter(EVENT_ORGANIZER__LOGIN=request.session['lid'],JUDGE_id=id)
    return render(request,"event_organiser/view_event.html",{"data":data})

def edit_event(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "Edit event"
    data = event.objects.get(id=id)
    return render(request,"event_organiser/edit_event.html",{"data":data,"id":id})


def edit_event_post(request,id):
    start_time = request.POST['textfield']
    en_time = request.POST['textfield2']
    name = request.POST['textfield3']
    descr = request.POST['textarea']
    category = request.POST['textfield4']
    event.objects.filter(id=id).update(start_time = start_time,end_time = en_time,name = name,description = descr,category = category)
    return HttpResponse("<script>alert('Updated');window.location='/view_event/"+id+"'</script>")

def delete_event(request,id):
    event.objects.get(id=id).delete()
    return HttpResponse("<script>alert('Removed');window.location='/view_event/" + id + "'</script>")



def allocate_programs(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "allocate program"
    data = program.objects.filter(EVENT_ORGANIZER__LOGIN=request.session['lid'])
    return render(request,"event_organiser/allocate_program.html",{"data":data,"id":id})

def allocate_program_post(request,id):
    programs = request.POST['select']
    data = allocate_program.objects.filter(PROGRAM_id = programs,JUDGE_id = id)
    if data.exists():
        return HttpResponse("<script>alert('Program already allocated');window.location='/view_judge'</script>")
    else:
        obj = allocate_program()
        obj.PROGRAM_id = programs
        obj.JUDGE_id = id
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


def college_view_program(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "view program"
    data  = program.objects.all()
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
    data = program.objects.all()
    data1 = student.objects.all()
    return render(request,"judge/upload_result.html",{"data":data,"data1":data1})

def upload_result_post(request):
    # results = request.FILES['fileField']
    programs = request.POST['select2']
    students = request.POST['select']
    # dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    # fs = FileSystemStorage()
    # fs.save(r"C:\Users\DELL\PycharmProjects\Fest_Hub\media\\" + dt + '.pdf', results)
    # path = '/media/' + dt + '.pdf'

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

    obj = result()
    obj.STUDENT_id = students
    obj.PROGRAM_id = programs
    obj.JUDGE = judge.objects.get(LOGIN=request.session['lid'])
    obj.result = f'media/uploads/{uploaded_file.name}'
    obj.save()
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
    print("pvvvvvliddddddddddddddd",lid)
    data = student.objects.get(LOGIN=lid)
    # print("imageeeeeeeeeee",data.image)

    return JsonResponse({
        "id": data.id,
        "Name": data.name,
        "phone": data.contact,
        "year": data.year,
        "place":data.place,
        "department": data.department,
        "photo": data.image,
        "Email": data.email
    })


def student_view_event(request):
    res = event.objects.all()
    ar = []
    for i in res:
        ar.append({
            "id": i.id,
            "start_time": i.start_time,
            "end_time": i.end_time,
            "status": i.status,
            "name": i.name,
            "description": i.description,
            "category": i.category,


        })
    return JsonResponse({"status": "ok", "data": ar})



def student_view_program(request):
    res = program.objects.all()
    ar = []
    for i in res:
        ar.append({
            "id": i.id,
            "start_time": i.start_time,
            "end_time": i.end_time,
            "name": i.name,
            "description": i.description,
            "category": i.category,
            "rounds": i.rounds,
            "date": i.date,
            "stage_no":i.stage_no,
            "stage_lati":i.stage_latitude,
            "stage_longi":i.stage_longitude

        })
    return JsonResponse({"status": "ok", "data": ar})


def student_send_request(request):
    lid = request.POST['lid']
    pid = request.POST['pid']


    print("liddddddddddddd",lid)
    print("pidddddddddddddddd",pid)

    obj = program_request()
    obj.status = 'pending'
    obj.date = datetime.datetime.now().date()
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
                "result":i.result,
                "program_name":i.PROGRAM.name,
                "program_category":i.PROGRAM.category,
                "program_date":i.PROGRAM.date,
                "organiser_name":i.PROGRAM.EVENT_ORGANIZER.name
            }
        )
        print("arrrrrrrrrrrrrrrrrrrrr",ar)
    return JsonResponse({"status":"ok","data":ar})