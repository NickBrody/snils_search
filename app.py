from flask import Flask, render_template, request

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

if __name__ == '__main__':
    app.run()
