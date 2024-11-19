from flask import Flask, render_template, request, redirect, url_for, flash
import json

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Used for flashing messages

# Dummy credentials for each role
CREDENTIALS = {
    "admin": {
        "username": "admin123",
        "password": "adminpass"
    },
    "mentor": {
        "username": "mentor123",
        "password": "mentorpass"
    },
    "intern": {
        "username": "intern123",
        "password": "internpass"
    }
}

# Load intern data from JSON file (local simulation for data)
def load_intern_data():
    with open('interns_data.json', 'r') as file:
        return json.load(file)

@app.route('/')
def home():
    return render_template('index.html')

# Route for login page
@app.route('/login/<role>', methods=['GET', 'POST'])
def login(role):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if CREDENTIALS[role]['username'] == username and CREDENTIALS[role]['password'] == password:
            flash(f"Welcome {role.capitalize()}!", "success")
            return redirect(url_for(f"{role}_dashboard"))
        else:
            flash("Invalid username or password. Please try again.", "danger")

    return render_template('login.html', role=role)

# Route to display intern dashboard
@app.route('/intern_dashboard')
def intern_dashboard():
    interns_data = load_intern_data()  # Load intern data
    intern = interns_data.get('intern_1')  # Access intern data for demo
    return render_template('intern_dashboard.html', intern=intern)

# Route to display mentor dashboard
@app.route('/mentor_dashboard')
def mentor_dashboard():
    interns_data = load_intern_data()  # Load intern data
    return render_template('mentor_dashboard.html', interns=interns_data)

# Route to display admin dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    interns_data = load_intern_data()  # Load intern data
    return render_template('admin_dashboard.html', interns=interns_data)

if __name__ == "__main__":
    app.run(debug=True)
