from django.core import serializers
from django.views.decorators.cache import cache_control
import re
import numpy as np
from django.shortcuts import render, redirect, HttpResponse
from django.template.response import TemplateResponse
from .models import User, Test, CompletedTests, CreatedTests

from gensim.models import KeyedVectors

# from tensorflow.keras.layers import LSTM
# from tensorflow.keras.models import load_model

# Load word to vector model
# model = KeyedVectors.load('Models/wordvector')
# model1 = LSTM(300, return_sequences=True)  # forward LSTM
# model2 = LSTM(300, go_backwards=True, return_sequences=True)  # backward LSTM
# model3 = load_model('C:/Users/Admin/Data/Final_yr_project/mpsc.h5')  # mpsc model for prediction
questions = []
modelAnswers = []


def getRecord(model, key):
    return model.objects.get(key)


def GetOriginalSemantics(sent):
    # Apply word to vector to every word in sentence
    vec = []
    for word in sent:
        try:
            try:
                ''
                # vec.append(model[word])
            except:
                ''
                # vec.append(model[word[0].upper() + word[1:]])
        except:
            pass
    extra = 300 - len(vec)
    vec = np.pad(vec, [(0, extra), (0, 0)], 'constant').reshape(1, 300, 300)
    return np.array(vec, np.float32)


def PreProcess(sent):  # tokenizing sentence into words
    sent = re.sub(r'[^\w\s]', '', sent)
    sent = np.array(sent.split())
    return sent


def GetMatchingDegree(crosscomb, outoff=5):  # Use CNN model here and return matching degree
    """pos = model3.predict(crosscomb)
    threshold = 0.03  # current Threshold Difference between 0 and 1
    range = threshold / outoff
    val = pos[0][0] - 0.62  # 0.62 is the lower bound and 0.65 is the upper bound
    return math.floor(val / range), pos[0][0]
    """
    return 0


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
    for user in users:
        if email == user.userEmail and password == user.userPassword:
            return True

    return False


def testCreation(request):
    if request.method == "POST":
        test = Test(request.POST['code'], request.POST['name'], request.POST['subject'], request.FILES['paper'])
        test.save()
        ctest = CreatedTests(code=Test.objects.get(code=request.POST['code']),
                             userEmail=User.objects.get(userEmail=request.session['username']))
        ctest.save()
        print("test created")
        return TemplateResponse(request, "redirectTemplate.html")
    else:
        tests = serializers.serialize('json', Test.objects.all())
        return render(request, "testCreation.html", {'tests': tests})


def testHistory(request):
    completedtests = CompletedTests.objects.filter(userEmail=request.session['username'])
    createdtests = CreatedTests.objects.filter(userEmail=request.session['username'])
    return render(request, "history.html", {'createdtests': createdtests, 'completedtests': completedtests})


def testAppear(request, testId="0"):
    global modelAnswers, questions
    try:
        if request.method == "POST":
            marks = 0
            for i in range(len(questions)):
                userAnswer = request.POST['answer' + str(i + 1)]
                marks += getMarks(userAnswer, modelAnswers[i])

            ctest = CompletedTests(code=Test.objects.get(code=int(testId)),
                                   userEmail=User.objects.get(userEmail=request.session['username']),
                                   marksObtained=marks)
            ctest.save()
            print('saved')
            return TemplateResponse(request, "redirectTemplate.html")
        else:
            modelAnswers = []
            questions = []
            testId = int(testId)
            testDetails = Test.objects.get(code=testId)
            questionPaper = testDetails.questionPaper
            data = ''
            for i in questionPaper.chunks():
                data = i.decode()
            data = data.split('\n')
            data.pop(2)
            for i in data:
                x = (i.split(','))
                questions.append(x[0])
                modelAnswers.append(x[1])

            return render(request, "studentTest.html", {"test": testDetails, "questions": questions})
    except Exception as e:
        print(e)
        pass


def logOut(request):
    print(request.session['username'], request.session)
    del request.session['username']
    print('session deleted !!', request.session)
    return redirect("/")


def getMarks(userAnswer, modelAnswer):
    """sent1 = PreProcess(modelAnswer)  # Data Preprocessing
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
    score, accuracy = GetMatchingDegree(semantics)


    ctest = CompletedTests(code=Test.objects.get(code=int(testId)), userEmail=User.objects.get(request.session['username']))
            print('saved', marks)
            ctest.marksObtained = marks

    """
    return 0
