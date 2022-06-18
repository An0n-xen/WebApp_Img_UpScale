import os 

from brain import ImgUpScale
from flask import Flask, render_template,request,redirect
from flask import request, url_for, send_file, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)

#Setting upfolders 
ini_path = os.path.join(os.getcwd(),'static')
app.config['UPLOAD_FOLDER'] = os.path.join(ini_path,'results')

app.secret_key = "Project Legacy"

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def runUpScale():
    ImgUpScale.imgUPS()

def listfiles():
    return os.listdir(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/view')
def viewfile():
    path = request.args.get('pathloc')
    filepath = os.path.join(app.config['UPLOAD_FOLDER'],path)
    return send_file(filepath, mimetype='zip')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods = ['GET','POST'])
def uploadfiles():
    if request.method == 'POST':
        if 'Images' not in request.files:
            return redirect(request.url)

        files = request.files.getlist('Images')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

        runUpScale()
        return redirect('/upload_page')
    
@app.route('/upload_page')
def uploadpage():
    return render_template('upload.html',
    path = app.config['UPLOAD_FOLDER'],
    item_list = listfiles())

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=2006)