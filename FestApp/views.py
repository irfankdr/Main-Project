from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def login(request):
    return render(request,'index.html')


def logincode(request):
    #
        username = request.POST['username']
        password = request.POST['password']
        if username == 'admin' and password == 'admin@123':
             return HttpResponse('''<script>alert('welcome');window.location='/judge_home';</script>''')
        elif username == 'judge' and password == 'judge@123':
             return HttpResponse('''<script>alert('welcome');window.location='/staff_home';</script>''')
        else:
            return HttpResponse('''<script>alert('Invalid');window.location='/login';</script>''')




def clgregister(request):
    return render(request, 'clgreg.html')

def judge_home(request):
    return render(request, 'judge_home/index.html')


def staff_home(request):
    return render(request,'staff_home/index.html')