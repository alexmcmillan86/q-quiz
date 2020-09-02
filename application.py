import os
import datetime
import random
import re

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
#app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///quiz.db")


@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    """Welcome page to all users"""

    # Forget any user_id
    session.clear()

    # Loads homepage for new user
    return render_template("/welcome.html")

@app.route("/", methods=["GET", "POST"])
@login_required
def homepage():
    """Show quiz rules and table of attempts"""

    if request.method == "GET":
        user_id = session["user_id"]

        # Find user and show attempts along with high score
        rows = db.execute("SELECT first_name, last_name, attempts, score, high_score FROM users WHERE id = :user_id",
                user_id=user_id)

        quiz_data = []     # creating an empty list

        for row in rows:
            quiz_info = {}
            quiz_info["firstname"] = row["first_name"]
            quiz_info["lastname"] = row["last_name"]
            quiz_info["attempts"] = row["attempts"]
            quiz_info["score"] = row["score"]
            quiz_info["highscore"] = row["high_score"]

            quiz_data.append(quiz_info)

        # Calculate value of stocks using current share prices
        return render_template("/homepage.html", quiz_data=quiz_data)

    else:
        return redirect("/question1")


@app.route("/question1", methods=["GET", "POST"])
@login_required
def question1():
    """Display Quiz Question"""

    user_id = session["user_id"]

    if request.method == "GET":
        # obtain answers from answers table
        answers = db.execute("SELECT answer_A, answer_B, answer_C, answer_D FROM answers WHERE qid = 1")

        # assign to mulitple choices A. B. C. D.
        for answer in answers:
            A1 = answer["answer_A"]
            B1 = answer["answer_B"]
            C1 = answer["answer_C"]
            D1 = answer["answer_D"]

        # shuffle answer values
        answers_q1 = [A1, B1, C1, D1]
        random.shuffle(answers_q1)

        A1 = answers_q1[0]
        B1 = answers_q1[1]
        C1 = answers_q1[2]
        D1 = answers_q1[3]

        # resetting score to 0 for start of new attempt
        db.execute("UPDATE users SET score = 0 WHERE id = :id",
                id=user_id)

        return render_template("/question1.html", A1=A1, B1=B1, C1=C1, D1=D1)

    else:
        # correct answer
        correct = db.execute("SELECT answer_A FROM answers WHERE qid = 1")[0]["answer_A"]
        selected = request.form["answer"].split()[1]
        result = re.match(selected, correct)

        if result:
            db.execute("UPDATE users SET score = score + 100 WHERE id = :id",
                    id=user_id)

        # generating answers for next question
        answers = db.execute("SELECT answer_A, answer_B, answer_C, answer_D FROM answers WHERE qid = 2")

        for answer in answers:
            A2 = answer["answer_A"]
            B2 = answer["answer_B"]
            C2 = answer["answer_C"]
            D2 = answer["answer_D"]

        # shuffle answer values
        answers_q2 = [A2, B2, C2, D2]
        random.shuffle(answers_q2)

        A2 = answers_q2[0]
        B2 = answers_q2[1]
        C2 = answers_q2[2]
        D2 = answers_q2[3]

        # write to SQL database with selected answer and points
        return render_template("/question2.html", A2=A2, B2=B2, C2=C2, D2=D2)

@app.route("/question2", methods=["POST"])
@login_required
def question2():
    """Display Quiz Question"""

    if request.method == "POST":
        user_id = session["user_id"]

        # correct answer
        correct = db.execute("SELECT answer_A FROM answers WHERE qid = 2")[0]["answer_A"]
        selected = request.form["answer"].split()[1]
        result = re.match(selected, correct)

        if result:
            db.execute("UPDATE users SET score = score + 100 WHERE id = :id",
                    id=user_id)

        # generating answers for next question
        answers = db.execute("SELECT answer_A, answer_B, answer_C, answer_D FROM answers WHERE qid = 3")

        for answer in answers:
            A3 = answer["answer_A"]
            B3 = answer["answer_B"]
            C3 = answer["answer_C"]
            D3 = answer["answer_D"]

        # shuffle answer values
        answers_q3 = [A3, B3, C3, D3]
        random.shuffle(answers_q3)

        A3 = answers_q3[0]
        B3 = answers_q3[1]
        C3 = answers_q3[2]
        D3 = answers_q3[3]

        return render_template("/question3.html", A3=A3, B3=B3, C3=C3, D3=D3)


@app.route("/question3", methods=["POST"])
@login_required
def question3():
    """Display Quiz Question"""

    if request.method == "POST":
        user_id = session["user_id"]

        # correct answer
        correct = db.execute("SELECT answer_A FROM answers WHERE qid = 3")[0]["answer_A"]
        selected = request.form["answer"].split()[1]
        result = re.match(selected, correct)

        if result:
            db.execute("UPDATE users SET score = score + 100 WHERE id = :id",
                    id=user_id)

        # generating answers for next question
        answers = db.execute("SELECT answer_A, answer_B, answer_C, answer_D FROM answers WHERE qid = 4")

        for answer in answers:
            A4 = answer["answer_A"]
            B4 = answer["answer_B"]
            C4 = answer["answer_C"]
            D4 = answer["answer_D"]

        # shuffle answer values
        answers_q4 = [A4, B4, C4, D4]
        random.shuffle(answers_q4)

        A4 = answers_q4[0]
        B4 = answers_q4[1]
        C4 = answers_q4[2]
        D4 = answers_q4[3]

        return render_template("/question4.html", A4=A4, B4=B4, C4=C4, D4=D4)


@app.route("/question4", methods=["POST"])
@login_required
def question4():
    """Display Quiz Question"""

    if request.method == "POST":
        user_id = session["user_id"]

        # correct answer
        correct = db.execute("SELECT answer_A FROM answers WHERE qid = 4")[0]["answer_A"]
        selected = request.form["answer"].split()[1]
        result = re.match(selected, correct)

        if result:
            db.execute("UPDATE users SET score = score + 100 WHERE id = :id",
                    id=user_id)

        # generating answers for next question
        answers = db.execute("SELECT answer_A, answer_B, answer_C, answer_D FROM answers WHERE qid = 5")

        for answer in answers:
            A5 = answer["answer_A"]
            B5 = answer["answer_B"]
            C5 = answer["answer_C"]
            D5 = answer["answer_D"]

        # shuffle answer values
        answers_q5 = [A5, B5, C5, D5]
        random.shuffle(answers_q5)

        A5 = answers_q5[0]
        B5 = answers_q5[1]
        C5 = answers_q5[2]
        D5 = answers_q5[3]

        return render_template("/question5.html", A5=A5, B5=B5, C5=C5, D5=D5)


@app.route("/question5", methods=["POST"])
@login_required
def question5():
    """Display Quiz Question"""

    if request.method == "POST":
        user_id = session["user_id"]

        # correct answer
        correct = db.execute("SELECT answer_A FROM answers WHERE qid = 5")[0]["answer_A"]
        selected = request.form["answer"].split()[1]
        result = re.match(selected, correct)

        if result:
            db.execute("UPDATE users SET score = score + 100 WHERE id = :id",
                    id=user_id)

        # generating answers for next question
        answers = db.execute("SELECT answer_A, answer_B, answer_C, answer_D FROM answers WHERE qid = 6")

        for answer in answers:
            A6 = answer["answer_A"]
            B6 = answer["answer_B"]
            C6 = answer["answer_C"]
            D6 = answer["answer_D"]

        # shuffle answer values
        answers_q6 = [A6, B6, C6, D6]
        random.shuffle(answers_q6)

        A6 = answers_q6[0]
        B6 = answers_q6[1]
        C6 = answers_q6[2]
        D6 = answers_q6[3]

        return render_template("/question6.html", A6=A6, B6=B6, C6=C6, D6=D6)


@app.route("/question6", methods=["POST"])
@login_required
def question6():
    """Display Quiz Question"""

    if request.method == "POST":
        user_id = session["user_id"]

        # correct answer
        correct = db.execute("SELECT answer_A FROM answers WHERE qid = 6")[0]["answer_A"]
        selected = request.form["answer"].split()[1]
        result = re.match(selected, correct)

        if result:
            db.execute("UPDATE users SET score = score + 100 WHERE id = :id",
                    id=user_id)

        # generating answers for next question
        answers = db.execute("SELECT answer_A, answer_B, answer_C, answer_D FROM answers WHERE qid = 7")

        for answer in answers:
            A7 = answer["answer_A"]
            B7 = answer["answer_B"]
            C7 = answer["answer_C"]
            D7 = answer["answer_D"]

        # shuffle answer values
        answers_q7 = [A7, B7, C7, D7]
        random.shuffle(answers_q7)

        A7 = answers_q7[0]
        B7 = answers_q7[1]
        C7 = answers_q7[2]
        D7 = answers_q7[3]

        return render_template("/question7.html", A7=A7, B7=B7, C7=C7, D7=D7)


@app.route("/question7", methods=["POST"])
@login_required
def question7():
    """Display Quiz Question"""

    if request.method == "POST":
        user_id = session["user_id"]

        # correct answer
        correct = db.execute("SELECT answer_A FROM answers WHERE qid = 7")[0]["answer_A"]
        selected = request.form["answer"].split()[1]
        result = re.match(selected, correct)

        if result:
            db.execute("UPDATE users SET score = score + 100 WHERE id = :id",
                    id=user_id)

        # generating answers for next question
        answers = db.execute("SELECT answer_A, answer_B, answer_C, answer_D FROM answers WHERE qid = 8")

        for answer in answers:
            A8 = answer["answer_A"]
            B8 = answer["answer_B"]
            C8 = answer["answer_C"]
            D8 = answer["answer_D"]

        # shuffle answer values
        answers_q8 = [A8, B8, C8, D8]
        random.shuffle(answers_q8)

        A8 = answers_q8[0]
        B8 = answers_q8[1]
        C8 = answers_q8[2]
        D8 = answers_q8[3]

        return render_template("/question8.html", A8=A8, B8=B8, C8=C8, D8=D8)


@app.route("/question8", methods=["POST"])
@login_required
def question8():
    """Display Quiz Question"""

    if request.method == "POST":
        user_id = session["user_id"]

        # correct answer
        correct = db.execute("SELECT answer_A FROM answers WHERE qid = 8")[0]["answer_A"]
        selected = request.form["answer"].split()[1]
        result = re.match(selected, correct)

        if result:
            db.execute("UPDATE users SET score = score + 100 WHERE id = :id",
                    id=user_id)

        # generating answers for next question
        answers = db.execute("SELECT answer_A, answer_B, answer_C, answer_D FROM answers WHERE qid = 9")

        for answer in answers:
            A9 = answer["answer_A"]
            B9 = answer["answer_B"]
            C9 = answer["answer_C"]
            D9 = answer["answer_D"]

        # shuffle answer values
        answers_q9 = [A9, B9, C9, D9]
        random.shuffle(answers_q9)

        A9 = answers_q9[0]
        B9 = answers_q9[1]
        C9 = answers_q9[2]
        D9 = answers_q9[3]

        return render_template("/question9.html", A9=A9, B9=B9, C9=C9, D9=D9)


@app.route("/question9", methods=["POST"])
@login_required
def question9():
    """Display Quiz Question"""

    if request.method == "POST":
        user_id = session["user_id"]

        # correct answer
        correct = db.execute("SELECT answer_A FROM answers WHERE qid = 9")[0]["answer_A"]
        selected = request.form["answer"].split()[1]
        result = re.match(selected, correct)

        if result:
            db.execute("UPDATE users SET score = score + 100 WHERE id = :id",
                    id=user_id)

        # generating answers for next question
        answers = db.execute("SELECT answer_A, answer_B, answer_C, answer_D FROM answers WHERE qid = 10")

        for answer in answers:
            A10 = answer["answer_A"]
            B10 = answer["answer_B"]
            C10 = answer["answer_C"]
            D10 = answer["answer_D"]

        # shuffle answer values
        answers_q10 = [A10, B10, C10, D10]
        random.shuffle(answers_q10)

        A10 = answers_q10[0]
        B10 = answers_q10[1]
        C10 = answers_q10[2]
        D10 = answers_q10[3]

        return render_template("/question10.html", A10=A10, B10=B10, C10=C10, D10=D10)


@app.route("/question10", methods=["POST"])
@login_required
def question10():
    """Display Quiz Question"""

    if request.method == "POST":
        user_id = session["user_id"]

        # correct answer
        correct = db.execute("SELECT answer_A FROM answers WHERE qid = 10")[0]["answer_A"]
        selected = request.form["answer"].split()[1]
        result = re.match(selected, correct)

        if result:
            db.execute("UPDATE users SET score = score + 100 WHERE id = :id",
                    id=user_id)

        # generating answers for next question
        answers = db.execute("SELECT answer_A, answer_B, answer_C, answer_D FROM answers WHERE qid = 11")

        for answer in answers:
            A11 = answer["answer_A"]
            B11 = answer["answer_B"]
            C11 = answer["answer_C"]
            D11 = answer["answer_D"]

        # shuffle answer values
        answers_q11 = [A11, B11, C11, D11]
        random.shuffle(answers_q11)

        A11 = answers_q11[0]
        B11 = answers_q11[1]
        C11 = answers_q11[2]
        D11 = answers_q11[3]

        return render_template("/question11.html", A11=A11, B11=B11, C11=C11, D11=D11)


@app.route("/question11", methods=["POST"])
@login_required
def question11():
    """Display Quiz Question"""

    if request.method == "POST":
        user_id = session["user_id"]

        # correct answer
        correct = db.execute("SELECT answer_A FROM answers WHERE qid = 11")[0]["answer_A"]
        selected = request.form["answer"].split()[1]
        result = re.match(selected, correct)

        if result:
            db.execute("UPDATE users SET score = score + 100 WHERE id = :id",
                    id=user_id)

        # generating answers for next question
        answers = db.execute("SELECT answer_A, answer_B, answer_C, answer_D FROM answers WHERE qid = 12")

        for answer in answers:
            A12 = answer["answer_A"]
            B12 = answer["answer_B"]
            C12 = answer["answer_C"]
            D12 = answer["answer_D"]

        # shuffle answer values
        answers_q12 = [A12, B12, C12, D12]
        random.shuffle(answers_q12)

        A12 = answers_q12[0]
        B12 = answers_q12[1]
        C12 = answers_q12[2]
        D12 = answers_q12[3]

        return render_template("/question12.html", A12=A12, B12=B12, C12=C12, D12=D12)


@app.route("/question12", methods=["POST"])
@login_required
def question12():
    """Display Quiz Question"""

    if request.method == "POST":
        user_id = session["user_id"]

        # correct answer
        correct = db.execute("SELECT answer_A FROM answers WHERE qid = 12")[0]["answer_A"]
        selected = request.form["answer"].split()[1]
        result = re.match(selected, correct)

        if result:
            db.execute("UPDATE users SET score = score + 100 WHERE id = :id",
                    id=user_id)

        # generating answers for next question
        answers = db.execute("SELECT answer_A, answer_B, answer_C, answer_D FROM answers WHERE qid = 13")

        for answer in answers:
            A13 = answer["answer_A"]
            B13 = answer["answer_B"]
            C13 = answer["answer_C"]
            D13 = answer["answer_D"]

        # shuffle answer values
        answers_q13 = [A13, B13, C13, D13]
        random.shuffle(answers_q13)

        A13 = answers_q13[0]
        B13 = answers_q13[1]
        C13 = answers_q13[2]
        D13 = answers_q13[3]

        return render_template("/question13.html", A13=A13, B13=B13, C13=C13, D13=D13)


@app.route("/question13", methods=["POST"])
@login_required
def question13():
    """Display Quiz Question"""

    if request.method == "POST":
        user_id = session["user_id"]

        # correct answer
        correct = db.execute("SELECT answer_A FROM answers WHERE qid = 13")[0]["answer_A"]
        selected = request.form["answer"].split()[1]
        result = re.match(selected, correct)

        if result:
            db.execute("UPDATE users SET score = score + 100 WHERE id = :id",
                    id=user_id)

        # generating answers for next question
        answers = db.execute("SELECT answer_A, answer_B, answer_C, answer_D FROM answers WHERE qid = 14")

        for answer in answers:
            A14 = answer["answer_A"]
            B14 = answer["answer_B"]
            C14 = answer["answer_C"]
            D14 = answer["answer_D"]

        # shuffle answer values
        answers_q14 = [A14, B14, C14, D14]
        random.shuffle(answers_q14)

        A14 = answers_q14[0]
        B14 = answers_q14[1]
        C14 = answers_q14[2]
        D14 = answers_q14[3]

        return render_template("/question14.html", A14=A14, B14=B14, C14=C14, D14=D14)


@app.route("/question14", methods=["POST"])
@login_required
def question14():
    """Display Quiz Question"""

    if request.method == "POST":
        user_id = session["user_id"]

        # correct answer
        correct = db.execute("SELECT answer_A FROM answers WHERE qid = 14")[0]["answer_A"]
        selected = request.form["answer"].split()[1]
        result = re.match(selected, correct)

        if result:
            db.execute("UPDATE users SET score = score + 100 WHERE id = :id",
                    id=user_id)

        # generating answers for next question
        answers = db.execute("SELECT answer_A, answer_B, answer_C, answer_D FROM answers WHERE qid = 15")

        for answer in answers:
            A15 = answer["answer_A"]
            B15 = answer["answer_B"]
            C15 = answer["answer_C"]
            D15 = answer["answer_D"]

        # shuffle answer values
        answers_q15 = [A15, B15, C15, D15]
        random.shuffle(answers_q15)

        A15 = answers_q15[0]
        B15 = answers_q15[1]
        C15 = answers_q15[2]
        D15 = answers_q15[3]

        return render_template("/question15.html", A15=A15, B15=B15, C15=C15, D15=D15)


@app.route("/question15", methods=["POST"])
@login_required
def question15():
    """Display Quiz Question"""

    if request.method == "POST":
        user_id = session["user_id"]

        # correct answer
        correct = db.execute("SELECT answer_A FROM answers WHERE qid = 15")[0]["answer_A"]
        selected = request.form["answer"].split()[1]
        result = re.match(selected, correct)

        if result:
            db.execute("UPDATE users SET score = score + 100 WHERE id = :id",
                    id=user_id)

        # generating answers for next question
        answers = db.execute("SELECT answer_A, answer_B, answer_C, answer_D FROM answers WHERE qid = 16")

        for answer in answers:
            A16 = answer["answer_A"]
            B16 = answer["answer_B"]
            C16 = answer["answer_C"]
            D16 = answer["answer_D"]

        # shuffle answer values
        answers_q16 = [A16, B16, C16, D16]
        random.shuffle(answers_q16)

        A16 = answers_q16[0]
        B16 = answers_q16[1]
        C16 = answers_q16[2]
        D16 = answers_q16[3]

        return render_template("/question16.html", A16=A16, B16=B16, C16=C16, D16=D16)


@app.route("/question16", methods=["POST"])
@login_required
def question16():
    """Display Quiz Question"""

    if request.method == "POST":
        user_id = session["user_id"]

        # correct answer
        correct = db.execute("SELECT answer_A FROM answers WHERE qid = 16")[0]["answer_A"]
        selected = request.form["answer"].split()[1]
        result = re.match(selected, correct)

        if result:
            db.execute("UPDATE users SET score = score + 100 WHERE id = :id",
                    id=user_id)

        # generating answers for next question
        answers = db.execute("SELECT answer_A, answer_B, answer_C, answer_D FROM answers WHERE qid = 17")

        for answer in answers:
            A17 = answer["answer_A"]
            B17 = answer["answer_B"]
            C17 = answer["answer_C"]
            D17 = answer["answer_D"]

        # shuffle answer values
        answers_q17 = [A17, B17, C17, D17]
        random.shuffle(answers_q17)

        A17 = answers_q17[0]
        B17 = answers_q17[1]
        C17 = answers_q17[2]
        D17 = answers_q17[3]

        return render_template("/question17.html", A17=A17, B17=B17, C17=C17, D17=D17)


@app.route("/question17", methods=["POST"])
@login_required
def question17():
    """Display Quiz Question"""

    if request.method == "POST":
        user_id = session["user_id"]

        # correct answer
        correct = db.execute("SELECT answer_A FROM answers WHERE qid = 17")[0]["answer_A"]
        selected = request.form["answer"].split()[1]
        result = re.match(selected, correct)

        if result:
            db.execute("UPDATE users SET score = score + 100 WHERE id = :id",
                    id=user_id)

        # generating answers for next question
        answers = db.execute("SELECT answer_A, answer_B, answer_C, answer_D FROM answers WHERE qid = 18")

        for answer in answers:
            A18 = answer["answer_A"]
            B18 = answer["answer_B"]
            C18 = answer["answer_C"]
            D18 = answer["answer_D"]

        # shuffle answer values
        answers_q18 = [A18, B18, C18, D18]
        random.shuffle(answers_q18)

        A18 = answers_q18[0]
        B18 = answers_q18[1]
        C18 = answers_q18[2]
        D18 = answers_q18[3]

        return render_template("/question18.html", A18=A18, B18=B18, C18=C18, D18=D18)


@app.route("/question18", methods=["POST"])
@login_required
def question18():
    """Display Quiz Question"""

    if request.method == "POST":
        user_id = session["user_id"]

        # correct answer
        correct = db.execute("SELECT answer_A FROM answers WHERE qid = 18")[0]["answer_A"]
        selected = request.form["answer"].split()[1]
        result = re.match(selected, correct)

        if result:
            db.execute("UPDATE users SET score = score + 100 WHERE id = :id",
                    id=user_id)

        # generating answers for next question
        answers = db.execute("SELECT answer_A, answer_B, answer_C, answer_D FROM answers WHERE qid = 19")

        for answer in answers:
            A19 = answer["answer_A"]
            B19 = answer["answer_B"]
            C19 = answer["answer_C"]
            D19 = answer["answer_D"]

        # shuffle answer values
        answers_q19 = [A19, B19, C19, D19]
        random.shuffle(answers_q19)

        A19 = answers_q19[0]
        B19 = answers_q19[1]
        C19 = answers_q19[2]
        D19 = answers_q19[3]

        return render_template("/question19.html", A19=A19, B19=B19, C19=C19, D19=D19)


@app.route("/question19", methods=["POST"])
@login_required
def question19():
    """Display Quiz Question"""

    if request.method == "POST":
        user_id = session["user_id"]

        # correct answer
        correct = db.execute("SELECT answer_A FROM answers WHERE qid = 19")[0]["answer_A"]
        selected = request.form["answer"].split()[1]
        result = re.match(selected, correct)

        if result:
            db.execute("UPDATE users SET score = score + 100 WHERE id = :id",
                    id=user_id)

        # generating answers for next question
        answers = db.execute("SELECT answer_A, answer_B, answer_C, answer_D FROM answers WHERE qid = 20")

        for answer in answers:
            A20 = answer["answer_A"]
            B20 = answer["answer_B"]
            C20 = answer["answer_C"]
            D20 = answer["answer_D"]

        # shuffle answer values
        answers_q20 = [A20, B20, C20, D20]
        random.shuffle(answers_q20)

        A20 = answers_q20[0]
        B20 = answers_q20[1]
        C20 = answers_q20[2]
        D20 = answers_q20[3]

        return render_template("/question20.html", A20=A20, B20=B20, C20=C20, D20=D20)


@app.route("/question20", methods=["GET", "POST"])
@login_required
def question20():
    """Display Quiz Question"""

    if request.method == "POST":
        user_id = session["user_id"]

        # correct answer
        correct = db.execute("SELECT answer_A FROM answers WHERE qid = 20")[0]["answer_A"]
        selected = request.form["answer"].split()[1]
        result = re.match(selected, correct)

        if result:
            db.execute("UPDATE users SET score = score + 100 WHERE id = :id",
                    id=user_id)

        # calculate final score
        final_score = db.execute("SELECT score FROM users WHERE id = :id",
                    id=user_id)[0]["score"]

        # update number of attempts
        db.execute("UPDATE users SET attempts = attempts + 1 WHERE id = :id",
                    id=user_id)

        # check attempt number and update the leaderboard table
        attempts = db.execute("SELECT attempts FROM users WHERE id = :id",
                    id=user_id)[0]["attempts"]

        if attempts == 1:   # completed first attempt at quiz
            first_score = final_score
            dt = datetime.datetime.now()    # generating timestamp
            firstname = db.execute("SELECT first_name FROM users WHERE id = :id",
                        id=user_id)[0]["first_name"]
            lastname = db.execute("SELECT last_name FROM users WHERE id = :id",
                        id=user_id)[0]["last_name"]
            db.execute("INSERT INTO leaderboard (first_name, last_name, high_score, timestamp) VALUES (:firstname, :lastname, :first_score, :dt)",
                        firstname=firstname, lastname=lastname, first_score=first_score, dt=dt)
            db.execute("UPDATE users SET score = :score, high_score = :first_score WHERE id = :id",
                        score=first_score, first_score=first_score, id=user_id)
        else:
            sub_score = final_score
            db.execute("UPDATE users SET score = :sub_score WHERE id = :id",
                        sub_score=sub_score, id=user_id)

        flash(f'Your Score: {final_score}')     # displays users score after last question is answered
        return redirect("/leaderboard")


@app.route("/leaderboard")
@login_required
def leaderboard():
    """Show leaderboard"""

    if request.method == "GET":
        data = []
        count = 0
        rows = db.execute("SELECT * FROM leaderboard ORDER BY high_score DESC, timestamp DESC")

        for row in rows:
            count += 1
            temp_data = {}

            temp_data["position"] = count
            temp_data["firstname"] = row["first_name"]
            temp_data["lastname"] = row["last_name"]
            temp_data["highscore"] = row["high_score"]
            temp_data["timestamp"] = row["timestamp"]

            data.append(temp_data)

        return render_template("/leaderboard.html", data=data)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # User reached route via GET
    if request.method == "GET":
        return render_template("/login.html")
    else:
        # Ensure username was submitted
        username = request.form.get("username")
        if not username:
            flash ("Must provide a username")
            return redirect("/login")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash ("Must provide a password")
            return redirect("/login")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 401)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/welcome")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "GET":
        return render_template("/register.html")
    else:
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("username not provided", 401)

        # Ensure first name was submitted
        elif not firstname:
            return apology("first name not provided", 401)

        # Ensure last name was submitted
        elif not lastname:
            return apology("last name not provided", 401)

        # Ensure password was submitted
        elif not password:
            return apology("password not provided", 401)

        # Checking that same password has been typed twice
        if password != confirm:
            return apology("password does not match", 400)
        else:
            # Check if username already exists in database
            rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)
            if len(rows) == 0:
                password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
                db.execute("INSERT INTO users (first_name, last_name, username, hash) VALUES (:firstname, :lastname, :username, :password)",
                            firstname=firstname, lastname=lastname, username=username, password=password)
                return redirect("/login")
            else:
                return apology("Username already exists", 403)


def errorhandler(e):
    """Handle error"""

    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
