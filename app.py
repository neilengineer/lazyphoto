import os
import random
import string
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from lazyphoto import *

app = Flask(__name__)
WORK_DIR="./workspace"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'tiff','bmp'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def random_string_generator(str_size, allowed_chars):
    return 'lazyphoto-bottomdata-com-'+''.join(random.choice(allowed_chars) for x in range(str_size))

final_img_folder = ""
final_img_name = ""
@app.route('/'+final_img_folder+'<filename>')
def uploaded_file(filename):
    return send_from_directory(final_img_folder,filename)

@app.route('/', methods=['GET', 'POST'])
@app.route('/lazyphoto', methods=['GET', 'POST'])
def process_photo():
    upload_url = '/lazyphoto/results'
    return render_template('lazyphoto.html', uploadurl=upload_url)

@app.route('/lazyphoto/results', methods=['GET', 'POST'])
def lazyphoto_results():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        f = request.files['file']
        if f.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if f and allowed_file(f.filename):
            #create temp working folder
            chars = string.ascii_letters + string.digits
            size = 12
            out_folder = random_string_generator(size, chars)
            os.makedirs(WORK_DIR+"/"+out_folder)
            os.chdir(WORK_DIR+"/"+out_folder)
            final_img_folder = WORK_DIR+"/"+out_folder

            filename = secure_filename(f.filename)
            f.save(filename)
            final_img_name = lazyphoto_process_main(filename)

            return redirect(url_for(send_from_directory(final_img_folder,final_img_name)))

#            return [WORK_DIR+"/"+out_folder, final_img_name]
            return redirect(url_for('uploaded_file',
                                    filename=final_img_name))

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404

@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
