from django.core import serializers
from django.views.decorators.cache import cache_control
import re
import numpy as np
from django.shortcuts import render, redirect, HttpResponse
from django.template.response import TemplateResponse
from .models import User, Test, CompletedTests, CreatedTests, Result
import datetime
from gensim.models import KeyedVectors
import math
from tensorflow.keras.layers import LSTM
from tensorflow.keras.models import load_model

# Load word to vector model
model = KeyedVectors.load('C:/Users/Admin/Data/Final_yr_project/model/wordvector')
model1 = LSTM(300, return_sequences=True)  # forward LSTM
model2 = LSTM(300, go_backwards=True, return_sequences=True)  # backward LSTM
model3 = load_model('C:/Users/Admin/Data/Final_yr_project/mpsc.h5')  # mpsc model for prediction
uestions = []
modelAnswers = []
marksPerQuestion = []
print(datetime.date.today())


def getRecord(model, key):
    return model.objects.get(key)


def GetOriginalSemantics(sent):
    # Apply word to vector to every word in sentence
    vec = []
    for word in sent:
        try:
            try:

                vec.append(model[word])
            except:

                vec.append(model[word[0].upper() + word[1:]])
        except:
            pass
    extra = 300 - len(vec)
    vec = np.pad(vec, [(0, extra), (0, 0)], 'constant').reshape(1, 300, 300)
    return np.array(vec, np.float32)


def PreProcess(sent):  # tokenizing sentence into words
    sent = re.sub(r'[^\w\s]', '', sent)
    sent = np.array(sent.split())
    return sent


def GetMatchingDegree(crosscomb, outoff):  # Use CNN model here and return matching degree
    pos = model3.predict(crosscomb)
    threshold = 0.03  # current Threshold Difference between 0 and 1
    range = threshold / outoff
    val = pos[0][0] - 0.62  # 0.62 is the lower bound and 0.65 is the upper bound
    return math.floor(val / range), pos[0][0]



def userSigning(request):
    if request.method == "POST":
        if request.POST['option'] == "signup":
            if insertUser(request.POST['name'], request.POST['email'], request.POST['password']):
                print('Record Saved !!')
            else:
                print('ERROR !')
        elif request.POST['option'] == "login":
            if validateUser(request.POST['email'], request.POST['password']):
                request.session['username'] = request.POST['email']
                print('login successful')
                return redirect("dashboard/")
            else:
                print("login failed")
        return render(request, "signlog.html")
    else:
        return render(request, "signlog.html")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashBoard(request):
    print(request.session['username'])
    if request.method == "POST":
        return render(request, "dash.html", )
    else:
        tests = []
        completedTests = serializers.serialize('json', CompletedTests.objects.all())
        for i in Test.objects.all():
            tests.append(i.code)
        return render(request, "dash.html",
                      {'tests': tests, 'completedTests': completedTests, 'userName': request.session['username']})


def insertUser(name, email, password):
    try:
        user = User(email, name, password)
        user.save()
        return True
    except:
        return False


def validateUser(email, password):
    users = User.objects.all()
    print(users)
    for user in users:
        if email == user.userEmail and password == user.userPassword:
            return True

    return False


def testCreation(request):
    if request.method == "POST":

        test = Test(request.POST['code'], request.POST['name'], request.POST['subject'], request.FILES['paper'],
                    request.session['username'], datetime.date.today(), getTotalMarks(request.FILES['paper']))
        test.save()
        ctest = CreatedTests(code=Test.objects.get(code=request.POST['code']),
                             userEmail=User.objects.get(userEmail=request.session['username']))
        ctest.save()
        print("test created")
        return TemplateResponse(request, "redirectTemplate.html",{'alert1':True})
    else:
        print(Test.objects.all())
        tests = serializers.serialize('json', Test.objects.all())
        return render(request, "testCreation.html", {'tests': tests})


def testHistory(request):
    completedtests = CompletedTests.objects.filter(userEmail=request.session['username'])
    createdtests = CreatedTests.objects.filter(userEmail=request.session['username'])
    return render(request, "history.html", {'createdtests': createdtests, 'completedtests': completedtests})


def testAppear(request, testId="0"):
    global modelAnswers, questions, marksPerQuestion
    try:
        if request.method == "POST":
            marks = 0
            for i in range(len(questions)):
                userAnswer = request.POST['answer' + str(i + 1)]
                c = getMarks(userAnswer, modelAnswers[i], marksPerQuestion[i])
                result = Result(code=Test.objects.get(code=int(testId)),userEmail=User.objects.get(userEmail=request.session['username']),  question=questions[i],
                                marks=c, totalMarks=marksPerQuestion[i])
                result.save()
                print("answer updated for test ", testId)
                marks += c

            ctest = CompletedTests(code=Test.objects.get(code=int(testId)),
                                   userEmail=User.objects.get(userEmail=request.session['username']),
                                   marksObtained=marks)
            ctest.save()
            print('saved')
            return TemplateResponse(request, "redirectTemplate.html",{'alert2':True})
        else:
            modelAnswers = []
            questions = []
            marksPerQuestion = []
            testId = int(testId)
            testDetails = Test.objects.get(code=testId)
            questionPaper = testDetails.questionPaper
            data = ''
            for i in questionPaper.chunks():
                data = i.decode()
            data = data.split('\n')
            data.pop(-1)
            for i in data:
                x = (i.split(','))
                questions.append(x[0])
                modelAnswers.append(x[1])
                marksPerQuestion.append(int(x[2]))

            return render(request, "studentTest.html", {"test": testDetails, "questions": questions})
    except Exception as e:
        print(e)
        pass


def loadTestDetails(request, testId, user=None):
    result = None
    print('user==>', user)
    if user == None:
        print("loading test details for ", testId, " by ", request.session['username'])
        user = request.session['username']
        result = Result.objects.filter(code=int(testId),userEmail=request.session['username'])
        print(result)
    else:
        print("loading test details for student ", testId, " by ", request.session['username'])
        result = Result.objects.filter(code=int(testId), userEmail=user)
        print(result)
    return render(request, "result.html", {'result':result, 'test':Test.objects.get(code=int(testId)), 'student':user})


def loadTestSummary(request, testId):
    print("loading test details for ", testId, " by ", request.session['username'])
    summary = CompletedTests.objects.filter(code=int(testId))
    print('summary = ', summary)
    return render(request, "performance.html", {'summary':summary, 'test':Test.objects.get(code=int(testId))})


def logOut(request):
    print(request.session['username'], request.session)
    del request.session['username']
    print('session deleted !!', request.session)
    return redirect("/")


def getMarks(userAnswer, modelAnswer, outoff): # outoff = maximum marks for this question
    sent1 = PreProcess(modelAnswer)  # Data Preprocessing
    sent2 = PreProcess(userAnswer)
    vec1 = GetOriginalSemantics(sent1)
    vec2 = GetOriginalSemantics(sent2)  # The 2 sentences are vectorized
    forwardX, backwardX = model1(vec1), model2(vec1)
    forwardY, backwardY = model1(vec2), model2(vec2)  # ofrward and backward semantic generation
    X = [vec1, forwardX, backwardX]
    Y = [vec2, forwardY, backwardY]
    semantics = []
    for i in X:
        for j in Y:
            semantics.append(np.dot(i, j))
    semantics = np.array(semantics).reshape(1, 300, 300, 9)
    print('shape of cross combination is ', semantics.shape)
    score, accuracy = GetMatchingDegree(semantics,outoff)
    return score


def getTotalMarks(file):
    total = 0
    for i in file.chunks():
        data = i.decode()
    data = data.split('\n')
    print(data[2])
    data.pop(-1)
    for i in data:
        x = (i.split(','))
        total += int(x[2])
    return total
