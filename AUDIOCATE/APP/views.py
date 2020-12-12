from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from . models import Book, Genre
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os
from gtts import gTTS
# will convert the image to text string
import pytesseract
from pdfminer.high_level import extract_text
from PIL import Image
import io
 # converts the text to speech
import pyttsx3
# Create your views here.

pytesseract.pytesseract.tesseract_cmd ='C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'

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
            return redirect("APP:dashboard")
        else:
            context={"message": "invalid login details"}
            return render(request,'index.html',context)
    else:
        return render(request,"index.html")

def convert(request):
    context={}
    if request.method == "POST":
        file=request.FILES.get("file")
        filename = str(file)
        rename=request.POST.get("name")
        name=rename+".mp3"
        link="media/"+name
        if os.path.splitext(filename)[1] in [".jpg",".jpeg",".png"]:
            img = Image.open(file)
            # converts the image to result and saves it into result variable
            result = pytesseract.image_to_string(img)
            # write text in a text file and save it to source path
            myAudio = gTTS(text=result, lang="en", slow=False)
            #Save as mp3 file
            myAudio.save(os.path.join("media",name))
            book=Book.objects.create(name=name,link=link,user=request.user)
            book.save()
            context={"message":"audio file successfully generated","finish":"true","link":link}
            return render(request,"examples/convert.html",context)
        elif os.path.splitext(filename)[1] in [".pdf"]:
            text = extract_text(file)
            new_text=text.replace("(cid:10)","")
            #Call GTTS
            try:
                myAudio = gTTS(text=new_text, lang="en-uk", slow=False)
                myAudio.save(os.path.join("media",name))
                book=Book.objects.create(name=name,link=link,user=request.user)
                book.save()
                context={"message":"audio file successfully generated","finish":"true","link":link,"name":name}
            except:
                context={"message":"audio file successfully generated","finish":"true","link":link,"name":name}
                return render(request,"examples/convert.html",context)
            return render(request,"examples/convert.html",context)
        else:
            context={"message":"this file is not allowed"}
            return render(request,"examples/convert.html",context)
    else:
        return render(request,"examples/convert.html")

def register(request):
    return render(request,"register.html")

def dashboard(request):
    return render(request,"dashboard.html")

def mybooks(request):
    context={"Book":Book.objects.filter(user=request.user)}
    return render(request,"examples/mybooks.html")

def genre(request):
    return render(request,"examples/genre.html")
