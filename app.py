import os
from flask import Flask, flash, request, redirect, send_from_directory, url_for
from werkzeug.utils import secure_filename

from case2txt import convert
from summarize import summarize

UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
ALLOWED_EXTENSIONS = set(['pdf'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            sentences = request.form['sentences']
        except:
            sentences = 5
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename, sentences=sentences))
    return '''
    <!doctype html>
    <title>CaseTLDR</title>
    <div style=padding:175px;font-family:courier>
    <div style=text-align:center;margin:auto;width:450px;height:100px;>
    <div style=border:solid;>
    <h1>Upload a Case</h1>
    <p>.pdf format</p>
    <br>
    <form method=post enctype=multipart/form-data id=uploadform>
      <input type=file name=file display=hidden>
      <input type=submit value=Upload>
    </form>
    <br>
    <hr>
    <h4># of sentences in summary</h4>
    <select name=sentences form=uploadform style=margin-bottom:10px;>
      <option value="1">1</option>
      <option value="2">2</option>
      <option value="3">3</option>
      <option value="4">4</option>
      <option value="5">5</option>
      <option value="6">6</option>
      <option value="7">7</option>
      <option value="8">8</option>
      <option value="9">9</option>
      <option value="10">10</option>
    </select>
    </div>
    </div>
    </div>
    '''

@app.route('/uploads/<filename>/<sentences>')
def uploaded_file(filename, sentences):
    file = convert(filename)
    print('Conversion...Done')
    summary = summarize(filename, sentences)
    print('Summary...Done')
    result_path = app.config['RESULTS_FOLDER'] + '/' + filename[:-4] + '/' + filename[:-3] + 'html'
    if os.path.isfile(result_path):
        return send_from_directory(app.config['RESULTS_FOLDER'],
                                    filename[:-4] + '/' + filename[:-3] + 'html')
    else:
        return send_from_directory(app.config['UPLOAD_FOLDER'],
                                    filename)

if __name__ == '__main__':
    if not os.path.isdir(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
    if not os.path.isdir(RESULTS_FOLDER):
        os.mkdir(RESULTS_FOLDER)
    app.run(debug=True, host='0.0.0.0')
