from flask import Flask
from lazyphoto import *
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/lazyphoto', methods=['GET', 'POST'])
def process_photo():
    upload_url = '/lazyphoto/results'
    return render_template('lazyphoto.html', uploadurl=upload_url)


@app.route('/lazyphoto/results', methods=['GET', 'POST'])
def lazyphoto_results():
    if request.method == 'POST':
        f = request.files['file']
        lazyphoto_process_main(f)

        return render_template('lazyphoto.html', ret_photos=)


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404

@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
