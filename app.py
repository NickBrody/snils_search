from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename

from database import session, Document

app = Flask(__name__)


def is_valid_snils(snils):
    if len(snils) != 11:
        return False
    control_num = int(snils[-2:])
    checksum = sum(int(num) * (9 - idx) for idx, num in enumerate(snils[:9]))
    checksum %= 101
    return control_num == checksum or (checksum in (100, 101)) and control_num == 0


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')


@app.route('/post', methods=["POST"])
def search_snils():
    check_snils = request.form['inputField']
    if is_valid_snils(check_snils):
        founded = session.query(Document).filter_by(snils=check_snils).first()
        if founded:
            return render_template("ok.html")
        else:
            return render_template("fail.html")
    else:
        return render_template("error.html")


@app.route('/upload', methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file.save(filename)
        read_file(filename)
    return render_template("file_uploaded.html")


def read_file(file):
    with open(file, "r") as uploaded_file:
        lines = uploaded_file.readlines()

    with open(f"out_{file}", "w") as output_file:
        for line in lines:
            modified_line = line.replace(" ", "").replace("-", "").replace("\n", "")
            if not is_valid_snils(modified_line):
                output_file.write(modified_line + " НЕВЕРЕН\n")
            elif is_valid_snils(modified_line):
                founded = session.query(Document).filter_by(snils=modified_line).first()
                if founded:
                    output_file.write(modified_line + " НАЙДЕН\n")
                else:
                    output_file.write(modified_line + " ОТСУТСВУЕТ\n")


if __name__ == '__main__':
    app.run()
