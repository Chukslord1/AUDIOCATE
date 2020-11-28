from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth

# Create your views here.
def index(request):
    return render(request,"homepage.html")


def login(request):
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        if User.objects.get(email=email):
            username=User.objects.get(email=email).username
        user= auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("APP:convert")
        else:
            context={"message": "invalid login details"}
            return render(request,'index.html',context)
    else:
        return render(request,"index.html")

def convert(request):
    return render(request,"webapp/Home.html")

def register(request):
    return render(request,"register.html")
