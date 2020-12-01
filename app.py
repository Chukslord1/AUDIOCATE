#Importing Libraries
#Importing Google Text to Speech library
import os
from flask import Flask,send_from_directory,request,url_for,jsonify
from flask_restful import reqparse, abort, Api, Resource
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from gtts import gTTS
# will convert the image to text string
import pytesseract
from pdfminer.high_level import extract_text
import werkzeug
# adds image processing capabilities
from PIL import Image
import io
 # converts the text to speech
import pyttsx3


app = Flask(__name__)
api = Api(app)
pytesseract.pytesseract.tesseract_cmd ='C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
UPLOAD_FOLDER = 'files'
AUDIO_FOLDER = 'audio'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['AUDIO_FOLDER'] = AUDIO_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class ConvertToAudio(Resource):
    def get(self):
        rename=request.form.get("name")
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        file = args['file']
        try:
            if file and allowed_file(file.filename):
                # From flask uploading tutorial
                filename = secure_filename(file.filename)
                name=rename+".mp3"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                if os.path.splitext(filename)[1] in [".jpg",".jpeg",".png"]:
                    img = Image.open(file)
                    # converts the image to result and saves it into result variable
                    result = pytesseract.image_to_string(img)
                    # write text in a text file and save it to source path
                    myAudio = gTTS(text=result, lang="en", slow=False)
                    #Save as mp3 file
                    myAudio.save(os.path.join(app.config['AUDIO_FOLDER'],name))
                    url=url_for("static", filename=name)
                    return jsonify({"success": True, "url": url})
                elif  os.path.splitext(filename)[1] in [".pdf"]:
                    text = extract_text(file)
                    new_text=text.replace("(cid:10)","")
                    #Call GTTS
                    myAudio = gTTS(text=new_text, lang="en", slow=False)

                    #Save as mp3 file
                    myAudio.save(os.path.join(app.config['AUDIO_FOLDER'],name))
                    url=url_for("static", filename=name)
                    return jsonify({"success": True, "url": url})
                else:
                    return "file not supported", 204
            else:
                return "No file found", 404
        except Exception as e:
            print(e)
            return "error",404

 # opening an image from the source path

#adding resouce with route
api.add_resource(ConvertToAudio, '/convert')

if __name__ == '__main__':
    app.run(debug=True)
