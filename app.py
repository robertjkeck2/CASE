import os
from flask import Flask, flash, request, redirect, send_from_directory, url_for
from werkzeug.utils import secure_filename

from case2txt import convert
from summarize import summarize

UPLOAD_FOLDER = '/code/uploads'
RESULTS_FOLDER = '/code/results'
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
    <h1>Upload a Case (PDF format)</h1>
    <form method=post enctype=multipart/form-data id=uploadform>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    <p># of sentences in summary</p>
    <select name=sentences form=uploadform>
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
    '''

@app.route('/uploads/<filename>/<sentences>')
def uploaded_file(filename, sentences):
    file = convert(filename)
    summary = summarize(filename, sentences)
    result_path = app.config['RESULTS_FOLDER'] + '/' + filename[:-4] + '/' + filename[:-3] + 'html'
    if os.path.isfile(result_path):
        return send_from_directory(app.config['RESULTS_FOLDER'],
                                    filename[:-4] + '/' + filename[:-3] + 'html')
    else:
        return send_from_directory(app.config['UPLOAD_FOLDER'],
                                    filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
