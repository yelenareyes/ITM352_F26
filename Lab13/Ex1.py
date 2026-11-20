# Create a simple Flask application that displays a welcome message.
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "Welcome to Yelena's web site!"


if __name__ == '__main__':
    app.run(debug=True)
    