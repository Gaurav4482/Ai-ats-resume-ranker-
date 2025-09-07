from flask import Flask, render_template, request
import os
from model import rank_resumes

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'resumes')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        job_desc = request.form['job_desc']
        uploaded_files = request.files.getlist('resumes')
        resume_paths = []
        for file in uploaded_files:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            resume_paths.append(filepath)
        rankings = rank_resumes(job_desc, resume_paths)
        return render_template('result.html', rankings=rankings)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
