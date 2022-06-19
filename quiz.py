import db
from flask import Flask, request, jsonify
app = Flask(__name__)
app.secret_key = 0
app.secret_score = 0
app.secret_code = 0


def getUsername(emailid):
    print(emailid)
    username = ''
    dbc = db.connect()
    cursor = dbc.cursor()
    qr = """select username from users where email=%s"""
    cursor.execute(qr, (emailid,))
    username = cursor.fetchone()
    if username is not None:
        user = "welcome {}. Please choose a subject".format(*username)
        print(user)
        return user
    else:
        return "Please enter a valid email id"
    dbc.close()


def getQuestion(subject, id):
    print(subject)
    subject = subject.lower()
    if subject == "python":
        qr = """select question,option1,option2,option3,option4 from pythonq where id=%s"""
        dbc = db.connect()
        cursor = dbc.cursor()
        cursor.execute(qr, (id,))
        for i in cursor:
            x = i
            print(x)
        return x
        dbc.close()


def allQuestions(subject):
    dbc = db.connect()
    cursor = dbc.cursor()
    subject = subject.lower()
    if subject == "python":
        qr = """select question,option1,option2,option3,option4 from pythonq"""
        cursor.execute(qr)
        ques = cursor.fetchall()
        count = len(ques)
    return ques, count


def loopQuestion(questions, count):
    i = 0
    app.secret_key += 1
    i = app.secret_key
    if i < count:
        ques = questions[i]
        print("Question---", ques)
        return ques
    else:
        end = app.secret_score
        return end


def getAnswers(subject):
    dbc = db.connect()
    cursor = dbc.cursor()
    subject = subject.lower()
    if subject == "python":
        qr = """select answer from pythonq"""
        cursor.execute(qr)
        ans = cursor.fetchall()
        return ans


def validation(ans, answers):
    l = len(answers)
    print(l)
    j = app.secret_code
    print(j)
    crt = ''.join(answers[j])
    crt = crt.lower()
    while j < l:
        if ans == crt:
            app.secret_score += 1
            reply = 'correct answer!. '
        else:
            app.secret_score += 0
            reply = "Incorrect answer!. the correct answer is {}. ".format(crt)
            # print(reply)
        # print(app.secret_score)
        app.secret_code += 1
        return reply, app.secret_score


def reset():
    app.secret_key = 0
    app.secret_code = 0
    app.secret_score = 0
