import os 
from flask import Flask, render_template,request,redirect
from flask import request, url_for, send_file, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(),'LR')
app.secret_key = "Project Legacy"

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

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

    return redirect('/upload_page')
    
@app.route('/upload_page')
def uploadpage():
    return render_template('layout.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=2006)