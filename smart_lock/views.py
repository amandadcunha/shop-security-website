from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http.response import StreamingHttpResponse
from django.shortcuts import render, redirect
from smart_lock.models import logs
from datetime import date
from smart_lock.recognizer import FaceRecognizer

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

@login_required(login_url='login')
def restricted(request):
    return render(request, "smart_lock/restricted.html")


@login_required(login_url='login')
def dashboard(request):
    request.session['lock'] = "LOCKED"
    log = logs.objects.filter(VISIT_TIME__date=date.today()).order_by('-VISIT_TIME')[:5]
    return render(request, "smart_lock/dashboard.html", {'log': log})


def gen1(camera):
    while True:
        frame = camera.recognizer()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def recognizer_feed(request):
    return StreamingHttpResponse(gen1(FaceRecognizer()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

# LOGIN
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username or Password is incorrect')
    return render(request, 'smart_lock/login.html')


# LOGOUT
@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


# TABLE DATA
@login_required(login_url='login')
def table_data(request):
    records = logs.objects.all().order_by('-VISIT_TIME')
    count = logs.objects.count()
    lock_status = request.session['lock']
    return render(request, 'smart_lock/logs.html', {'records': records, 'count': count, 'lock_status':lock_status})