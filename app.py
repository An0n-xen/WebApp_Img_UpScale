import os 
from flask import Flask, render_template,request,redirect
from flask import request, url_for, send_file, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('layout.html')




if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=2006)