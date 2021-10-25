import os
import urllib.request
from flask import Flask, render_template, request, redirect, send_file
from s3_functions import list_files, upload_file, show_image
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
#BUCKET = "flasksfdfds"
BUCKET = os.environ.get('BUCKET_NAME')
instance = urllib.request.urlopen('http://169.254.169.254/latest/meta-data/instance-id').read().decode()
region = urllib.request.urlopen('http://169.254.169.254/latest/meta-data/placement/availability-zone').read().decode()

@app.route("/")
def home():
    contents = list_files(BUCKET)
    return render_template('index.html',IID=instance,REGION=region)

@app.route("/pics")
def list():
    contents = show_image(BUCKET)
    return render_template('collection.html', contents=contents)

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
        upload_file(f"uploads/{f.filename}", BUCKET)
        return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)

