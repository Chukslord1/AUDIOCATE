# import the following libraries
# will convert the image to text string
import pytesseract

# adds image processing capabilities
from PIL import Image
import io
 # converts the text to speech
import pyttsx3

#translates into the mentioned language
from googletrans import Translator
from fpdf import FPDF

 # opening an image from the source path
img = Image.open('new.png')

# describes image format in the output
print(img)
# path where the tesseract module is installed
pytesseract.pytesseract.tesseract_cmd ='C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
# converts the image to result and saves it into result variable
result = pytesseract.image_to_string(img)
# write text in a text file and save it to source path
with io.open('simple.txt','w',encoding="utf-8") as file:
    file.write(result)
    print(result)

pdf = FPDF()

pdf.add_page()

pdf.set_font("Arial", size = 15)

f = open("simple.txt", "r")

for x in f:
	pdf.cell(200, 10, txt = x, ln = 1, align = 'C')

pdf.output("simple.pdf")

def result():
    return result
