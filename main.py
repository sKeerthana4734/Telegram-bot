from flask import Flask, session, redirect, url_for, request, jsonify
import json
import os
import quiz

app = Flask(__name__)
app.secret_key = 0
app.secret_code = 1
app.secret_count = 0
app.secret_ques = 0
app.secret_ans = 0


@app.route("/webhook", methods=['POST', 'GET'])
def webhook():
    Req = request.get_json(silent=True, force=True)
    value = (Req.get('queryResult'))
    name = value.get('parameters')
    emailid = name.get('email')
    subject = name.get('subject')
    ans = name.get('answer')
    close = name.get('close')

    if emailid is not None:
        output = quiz.getUsername(emailid)
        res = jsonify({
            "fulfillmentText": output + "\n\n" + "Python\n"+"Web Technology",
            "payload": {
                "google": {
                    "expectUserResponse": True,
                    "richResponse": {
                        "items": [
                            {
                                "simpleResponse": {
                                    "textToSpeech": output
                                }
                            }
                        ],
                        "suggestions": [
                            {
                                "title": "Python"
                            },
                            {
                                "title": "Web Technology"
                            }
                        ]
                    }
                }
            }
        })

    elif subject is not None:
        app.secret_key = subject
        output = quiz.getQuestion(subject, id=1)
        ques, count = quiz.allQuestions(subject)
        app.secret_ques = ques
        app.secret_count = count
        answers = quiz.getAnswers(subject)
        app.secret_ans = answers
        Q, op1, op2, op3, op4 = output
        res = jsonify({
            "fulfillmentText": Q,
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            Q,
                        ]
                    }
                },
                {
                    "text": {
                        "text": [
                            "The options are :\n" + op1 + "\n" + op2 + "\n" + op3 + "\n"+op4,
                        ]
                    }
                }
            ],
            "payload": {
                "google": {
                    "expectUserResponse": True,
                    "richResponse": {
                        "items": [
                            {
                                "simpleResponse": {
                                    "textToSpeech": Q,
                                }
                            },
                            {
                                "simpleResponse": {
                                    "textToSpeech": "The options are: \n"+op1+".\n"+op2+".\n"+op3+".\n"+op4
                                }
                            }
                        ],
                        "suggestions": [
                            {
                                "title": op1
                            },
                            {
                                "title": op2
                            },
                            {
                                "title": op3
                            },
                            {
                                "title": op4
                            }
                        ]
                    }
                }
            }
        })

    elif ans is not None:
        answers = app.secret_ans
        ques = app.secret_ques
        count = app.secret_count
        z = quiz.loopQuestion(ques, count)
        ans = ans.lower()
        reply, score = quiz.validation(ans, answers)
        if type(z) is not int:
            Q, op1, op2, op3, op4 = z
            Q = "".join(Q)
            op1 = "".join(op1)
            op2 = "".join(op2)
            op3 = "".join(op3)
            op4 = "".join(op4)
            score = str(score)
            res = jsonify({
                "fulfillmentText": Q,
                "fulfillmentMessages": [
                    {
                        "text": {
                            "text": [
                                reply+"your current score is "+score+". Next Question :",
                            ]
                        }
                    },
                    {
                        "text": {
                            "text": [
                                Q,
                            ]
                        }
                    },
                    {
                        "text": {
                            "text": [
                                "The options are :\n" + op1 + "\n" + op2 + "\n" + op3 + "\n"+op4,
                            ]
                        }
                    }
                ],
                "payload": {
                    "google": {
                        "expectUserResponse": True,
                        "richResponse": {
                            "items": [
                                {
                                    "simpleResponse": {
                                        "textToSpeech": reply+"your current score is "+score+". Next Question :"
                                    }
                                },
                                {
                                    "simpleResponse": {
                                        "textToSpeech":  Q+"\n"+"The options are: \n"+op1+".\n"+op2+".\n"+op3+".\n"+op4
                                    }
                                }
                            ],
                            "suggestions": [
                                {
                                    "title": op1
                                },
                                {
                                    "title": op2
                                },
                                {
                                    "title": op3
                                },
                                {
                                    "title": op4
                                }
                            ]
                        }
                    }
                }
            })
        else:
            quiz.reset()
            res = jsonify({
                "fulfillmentMessages": [
                    {
                        "text": {
                            "text": [
                                reply+"QUIZ ENDED",
                            ]
                        }
                    },
                    {
                        "text": {
                            "text": [
                                "Your total score is {} out of {}".format(
                                    score, count),
                            ]
                        }
                    },
                    {
                        "text": {
                            "text": [
                                "Do you want to take Quiz again?\n\n" + "Yes\nNo",
                            ]
                        }
                    }
                ],
                "payload": {
                    "google": {
                        "expectUserResponse": True,
                        "richResponse": {
                            "items": [
                                {
                                    "simpleResponse": {
                                        "textToSpeech": reply+"QUIZ ENDED. \n"+"Your total score is {} out of {}".format(score, count)
                                    }
                                },
                                {
                                    "simpleResponse": {
                                        "textToSpeech": "Do you want to take quiz again?"
                                    }
                                }
                            ],
                            "suggestions": [
                                {
                                    "title": "Yes"
                                },
                                {
                                    "title": "No"
                                }
                            ]
                        }
                    }
                }
            })

    elif close is not None:
        quiz.reset()
        res = jsonify({
            "fulfillmentText": "Thank You for attending the quiz. ",
            "payload": {
                "google": {
                    "expectUserResponse": False,
                    "richResponse": {
                        "items": [
                            {
                                "simpleResponse": {
                                    "textToSpeech": "Thank You for attending the quiz. "
                                }
                            }
                        ]
                    }
                }
            }
        })

    return res


if __name__ == "__main__":
    app.run(debug=True)
