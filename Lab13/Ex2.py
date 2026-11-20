# Application that allows a user to log in with hard-coded credentials.
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
USERS = {
    "reyes": "reyes123",
    "yelena": "yelena123",
}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if USERS.get(username) == password:
            return redirect(url_for('success', username=username))
        return render_template('login.html', error="Invalid username or password.")
    return render_template('login.html')


@app.route('/success/<username>')
def success(username):
    return render_template('success.html', username=username)


if __name__ == '__main__':
    app.run(debug=True)