#Importing Libraries
#Importing Google Text to Speech library
import os
from flask import Flask,send_from_directory,request
from flask_restful import reqparse, abort, Api, Resource
from gtts import gTTS
# will convert the image to text string
import pytesseract
from pdfminer.high_level import extract_text

# adds image processing capabilities
from PIL import Image
import io
 # converts the text to speech
import pyttsx3

app = Flask(__name__)
api = Api(app)
pytesseract.pytesseract.tesseract_cmd ='C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'


class ConvertToAudio(Resource):
    def post(self):
        file=request.files.get("file")
        file_name=file.name
        rename=request.form.get("name")
        name=rename+".mp3"
        if file:
            if os.path.splitext(file_name)[1] == ["jpg","jpeg","png"]:
                file.save()
                img = Image.open(file)
                # converts the image to result and saves it into result variable
                result = pytesseract.image_to_string(img)
                # write text in a text file and save it to source path
                myAudio = gTTS(text=result, lang="en", slow=False)
                #Save as mp3 file
                myAudio.save(name)
                return "hello", 201
            elif  os.path.splitext(file_name)[1] == ["pdf","txt"]:
                file.save()
                text = extract_text(file)
                new_text=text.replace("(cid:10)","")
                print(new_text)
                #Call GTTS
                myAudio = gTTS(text=new_text, lang="en", slow=False)

                #Save as mp3 file
                myAudio.save(name)
                return send_from_directory(myAudio)
        else:
            return "No file found", 404

 # opening an image from the source path

#adding resouce with route
api.add_resource(ConvertToAudio, '/convert')

if __name__ == '__main__':
    app.run(debug=True)
