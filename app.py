from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Load Model
model = joblib.load("model.pkl")

# Home Page (Login Page)
@app.route("/")
def home():
    return render_template("login.html")

# Login Validation
@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    if username == "admin" and password == "admin123":
        return render_template("index.html")

    return render_template(
        "login.html",
        error="Invalid Username or Password"
    )

# Prediction Route
@app.route("/predict", methods=["POST"])
def predict():

    cgpa = float(request.form["cgpa"])
    programming_skill = int(request.form["programming_skill"])
    communication_skill = int(request.form["communication_skill"])
    aptitude_score = int(request.form["aptitude_score"])
    projects_count = int(request.form["projects_count"])
    internships_count = int(request.form["internships_count"])
    language = request.form["language"]

    data = np.array([[
        cgpa,
        programming_skill,
        communication_skill,
        aptitude_score,
        projects_count,
        internships_count
    ]])

    probability = model.predict_proba(data)[0][1] * 100

    # Placement Status
    if probability >= 80:
        prediction = "LIKELY TO GET PLACED"
    elif probability >= 60:
        prediction = "MODERATE CHANCE"
    else:
        prediction = "NEEDS IMPROVEMENT"

    # Career Recommendation
    if language == "Python":
        career = "Machine Learning Engineer"
    elif language == "Java":
        career = "Java Developer"
    elif language == "C++":
        career = "Software Developer"
    elif language == "SQL":
        career = "Database Administrator"
    elif language == "JavaScript":
        career = "Frontend Developer"
    else:
        career = "Software Engineer"

    companies = [
        "Google",
        "Microsoft",
        "Infosys",
        "TCS",
        "IBM"
    ]

    skills = []

    if programming_skill < 8:
        skills.append("Programming Skills")

    if communication_skill < 8:
        skills.append("Communication Skills")

    if aptitude_score < 80:
        skills.append("Aptitude Skills")

    if projects_count < 3:
        skills.append("Build More Projects")

    if internships_count < 2:
        skills.append("Gain Internship Experience")

    if len(skills) == 0:
        skills.append("No Major Improvements Required")

    strengths = []

    if programming_skill >= 8:
        strengths.append("Strong Programming Skills")

    if communication_skill >= 8:
        strengths.append("Good Communication Skills")

    if aptitude_score >= 80:
        strengths.append("Strong Aptitude")

    if cgpa >= 8:
        strengths.append("Good Academic Performance")

    return render_template(
        "index.html",
        prediction=prediction,
        probability=round(probability, 2),
        career=career,
        companies=companies,
        skills=skills,
        strengths=strengths,
        cgpa=cgpa,
        programming_skill=programming_skill,
        communication_skill=communication_skill,
        aptitude_score=aptitude_score,
        projects_count=projects_count,
        internships_count=internships_count,
        language=language
    )

if __name__ == "__main__":
    app.run(debug=True)