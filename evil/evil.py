from flask import Flask
from flask_cors import CORS


app = Flask(__name__, static_url_path='')
CORS(app)


@app.route('/')
def homepage():
    return app.send_static_file('index.html')


@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/ping', methods = ["POST"])
def ping():
    print("ping")
    return str()


if __name__ == '__main__':
    app.run()
