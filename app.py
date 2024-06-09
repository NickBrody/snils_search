from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')


@app.route('/post', methods=["POST"])
def search_snils():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
