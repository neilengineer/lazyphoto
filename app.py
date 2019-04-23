import os
import random
import string
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from lazyphoto import *

app = Flask(__name__)
WORK_DIR="workspace"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'tiff','bmp'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def random_string_generator(str_size, allowed_chars):
    return 'lazyphoto-bottomdata-com-'+''.join(random.choice(allowed_chars) for x in range(str_size))

@app.route('/', methods=['GET', 'POST'])
@app.route('/lazyphoto', methods=['GET', 'POST'])
def process_photo():
    upload_url = '/lazyphoto/results'
    return render_template('lazyphoto.html', uploadurl=upload_url)

@app.route('/workspace/<path:filename>')
def send_file(filename):
    return send_from_directory(WORK_DIR, filename)

@app.route('/lazyphoto/results', methods=['GET', 'POST'])
def lazyphoto_results():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(url_for('process_photo'))
        f = request.files['file']
        if f.filename == '':
            return redirect(url_for('process_photo'))
        w = request.form.get('width')
        h = request.form.get('height')
        if w != "" or h != "":
            w = float(w)
            h = float(h)
        else:
            return redirect(url_for('process_photo'))

        if f and allowed_file(f.filename):
            #create temp working folder
            chars = string.ascii_letters + string.digits
            size = 12
            out_folder = random_string_generator(size, chars)
            final_img_folder = os.path.join(WORK_DIR, out_folder)
            os.makedirs(final_img_folder)
            old_dir = os.getcwd()
            os.chdir(final_img_folder)

            filename = secure_filename(f.filename)
            f.save(filename)

            final_img_name, final_img_name_single, dis_string = lazyphoto_process_main(filename,w,h)
            final_img_name = os.path.join(out_folder,final_img_name)
            dis_img = url_for('send_file', filename=final_img_name)
            os.chdir(old_dir)
            return render_template('lazyphoto-result.html', img_name=dis_img,
                    dis_string=dis_string)
    return page_not_found(404)

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404

@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
