#Importing Libraries
#Importing Google Text to Speech library
import os
from flask import Flask,send_from_directory,request
from flask_restful import reqparse, abort, Api, Resource
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from gtts import gTTS
# will convert the image to text string
import pytesseract
from pdfminer.high_level import extract_text

# adds image processing capabilities
from PIL import Image
import io
 # converts the text to speech
import pyttsx3
from models import User,db

app = Flask(__name__)
api = Api(app)
pytesseract.pytesseract.tesseract_cmd ='C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
UPLOAD_FOLDER = 'files'
AUDIO_FOLDER = 'audio'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['AUDIO_FOLDER'] = AUDIO_FOLDER

#db.create_all()
#admin = User(username='ochuko', email='chukslordz1@example.com')
#admin.set_password('Godisjesus1@1')
#db.session.add(admin)
#db.session.commit()
u= User.query.filter_by(email="chukslordz1@example.com").first()
u.check_password('Godisjesus1@1')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class ConvertToAudio(Resource):
    def post(self):
        file = request.files['file']
        rename=request.form.get("name")
        if file and allowed_file(file.filename):
            # From flask uploading tutorial
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            name=rename+".mp3"
            if os.path.splitext(filename)[1] in [".jpg",".jpeg",".png"]:
                img = Image.open(file)
                # converts the image to result and saves it into result variable
                result = pytesseract.image_to_string(img)
                # write text in a text file and save it to source path
                myAudio = gTTS(text=result, lang="en", slow=False)
                #Save as mp3 file
                myAudio.save(os.path.join(app.config['AUDIO_FOLDER'],name))
                return "saved audio from image", 201
            elif  os.path.splitext(filename)[1] in [".pdf",".txt"]:
                text = extract_text(file)
                new_text=text.replace("(cid:10)","")
                #Call GTTS
                myAudio = gTTS(text=new_text, lang="en", slow=False)

                #Save as mp3 file
                myAudio.save(os.path.join(app.config['AUDIO_FOLDER'],name))
                return "saved audio from pdf",201
            else:
                return "file not supported", 204
        else:
            return "No file found", 404

 # opening an image from the source path

#adding resouce with route
api.add_resource(ConvertToAudio, '/convert')

if __name__ == '__main__':
    app.run(debug=True)
