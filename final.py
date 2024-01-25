#%%
import os
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask, request, render_template, send_from_directory
from fpdf import FPDF
from PIL import Image
import cv2

app = Flask(__name__)
modeld = load_model("model.h5")

class PDF(FPDF):
    def header(self):
        self.image('logo.png', 10, 8, 33)
        self.set_font('Arial', 'B', 20)
        self.cell(70, 80, '', 0, 0, 0)
        self.cell(80, 10, 'Skin Disease Classification', 0, ln=0, align='C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

@app.route('/')
def home():
    return render_template('check.html')

@app.route('/gettypeofdisease', methods=['POST'])
def gettypeofdisease():
    msge = ''
    name = request.form['name']
    age = request.form['age']
    phoneNumber = request.form['phno']
    Email = request.form['E-mail']
    file_pic = request.files['file']

    path = "static/temp/image.jpg"
    img = Image.open(file_pic).resize((200, 200))
    img.save(path, 'png')

    img = cv2.imread(path, 1)
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    filter_size = (3, 3)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, filter_size)
    masked_image = cv2.morphologyEx(gray_image, cv2.MORPH_BLACKHAT, kernel)
    cleared_image = cv2.inpaint(img, masked_image, 3, cv2.INPAINT_TELEA)

    X = image.img_to_array(cleared_image)
    X = X.reshape((1,) + X.shape)
    val = modeld.predict(X)

    msge = 'pigmented benign keratosis' if val == 1 else 'Vascular lesion'

    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.line(10, 50, 200, 50)
    pdf.set_font('Times', 'i', 20)
    pdf.cell(0, 30, '', 0, 1, 0)
    pdf.cell(41, 0, '', 0, 0, 0)
    pdf.cell(0, 15, 'Name:' + name, 0, 1, 0)
    pdf.cell(46, 0, '', 0, 0, 0)
    pdf.cell(0, 15, 'Age:' + age, 0, 1, 1)
    pdf.cell(39, 0, '', 0, 0, 0)
    pdf.cell(0, 15, 'E-mail:' + Email, 0, 1, 1)
    pdf.cell(17, 0, '', 0, 0, 0)
    pdf.cell(0, 15, 'PhoneNumber:' + phoneNumber, 0, 1, 0)
    pdf.cell(19, 0, '', 0, 0, 0)
    pdf.cell(0, 15, 'DiseaseName:' + msge, 0, 1, 0)

    pdf_output_path = os.path.join(app.root_path, 'static', 'userinfo', 'file.pdf')
    pdf.output(pdf_output_path, 'F')

    return render_template('second.html', msge=msge, name=name, age=age, phno=phoneNumber, email=Email)

@app.route('/downloadpdf', methods=['POST'])
def downloadpdf():
    url = "static/userinfo"
    files = os.listdir(url)
    return render_template("ex1.html", files=files, url=url)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'userinfo'), filename)

if __name__ == '__main__':
    app.run(debug=True)
# %%
