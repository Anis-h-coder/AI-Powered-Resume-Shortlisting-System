from flask import Flask, request, render_template
import os
from resume_parser import parse_resume_text
from ranker import rank_resumes

app = Flask(__name__ , static_folder='static', template_folder='templates')
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/match', methods=['POST'])
def match():
    jd_text = request.form['jobdesc']
    resume_files = request.files.getlist('resumes')

    resumes_data = []
    filenames = []

    for file in resume_files:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        text = parse_resume_text(filepath)
        resumes_data.append(text)
        filenames.append(file.filename)

    scores = rank_resumes(jd_text, resumes_data)

    ranked = sorted(zip(filenames, scores), key=lambda x: x[1], reverse=True)
    return render_template('index.html', results=ranked)

if __name__ == '__main__':
    app.run(debug=True)
