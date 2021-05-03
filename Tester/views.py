import re
import numpy as np
from django.shortcuts import render, HttpResponse
from gensim import models
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM

# Load word to vector model
w = models.KeyedVectors.load('C:/Projects/semantic matching/SemanticMatching/Tester/Models/wordvector')

# Define LSTM backward model
backwardmodel = Sequential()
backwardmodel.add(LSTM(units=300, go_backwards=True))
backwardmodel.compile('rmsprop', 'mse')

# Define LSTM forward model
forwardmodel = Sequential()
forwardmodel.add(LSTM(units=300))
forwardmodel.compile('rmsprop', 'mse')


def home(request):
    if request.method == "POST":
        print(request.POST)
        print('FILEs = \n', request.FILES['model-answer-sheet'], request.FILES['answer-sheet'])
        modelans = request.FILES['model-answer-sheet']
        userans = request.FILES['answer-sheet']
        for i in modelans.chunks():
            modelans = i.decode()
            print("Model ans = ", modelans)
        for i in userans.chunks():
            userans = i.decode()
            print("User ans = ", userans)
        # Here we are ready with 2 sentences now let's calculate their matching degree.
        sent1 = PreProcess(modelans)
        sent2 = PreProcess(userans)
        l1 = len(sent1)
        l2 = len(sent2)
        mn = min(l1, l2)
        sent1orig = GetOriginalSemantics(sent1)
        sent2orig = GetOriginalSemantics(sent2)
        sent1orig = sent1orig.reshape((l1, 1, 300))
        sent2orig = sent2orig.reshape((l2, 1, 300))
        sent1forward = forwardmodel.predict(sent1orig)
        sent2forward = forwardmodel.predict(sent2orig)
        sent1backward = backwardmodel.predict(sent1orig)
        sent2backward = backwardmodel.predict(sent2orig)
        sent1orig = sent1orig.reshape((l1, 300))
        sent2orig = sent2orig.reshape((l2, 300))
        S1 = np.array([sent1orig, sent1forward, sent1backward])
        S2 = np.array([sent2orig, sent2forward, sent2backward])
        cross_comb = []
        for i in S1:
            for j in S2:
                x = np.dot(i, j.T)
                x = np.pad(x, (50 - mn, 50 - mn))
                # print(x)
                if l1 < l2:
                    x = x[50 - mn:, 50 - mn:-abs(l1 - l2)]
                elif l1 > l2:
                    x = x[50 - mn:-abs(l1 - l2), 50 - mn:]
                else:
                    x = x[50 - mn:, 50 - mn:]
                cross_comb.append(x)
        cross_comb = np.array(cross_comb)
        print('shape of cross combination is ', cross_comb.shape)
        score = GetMatchingDegree(cross_comb)
        iscore = True
        return render(request, "home.html",{'iscore':iscore, 'score':score})
    else:
        # form = FileForm()
        iscore = False
        return render(request, "home.html", {'iscore':iscore})


"""def Display(request):
    data = SampleModel.objects.all()
    # print("data=>", SampleModel.objects.all())
    for i in data:
        print(i, i.name, type(i.filepath))
        for c in i.filepath.chunks():
            print('c=', c)

    return HttpResponse("yessssssss")"""


def GetOriginalSemantics(sent):  # Apply word to vector to every word in sentence
    semantics = []
    for i in sent:
        try:
            try:
                semantics.append(w[i])
            except:
                i = i[0].upper() + i[1:]
                semantics.append(w[i])
        except:
            semantics.append([0.1] * 300)
    semantics = np.array(semantics)
    return semantics


def PreProcess(sent):  # tokenizing sentence into words
    sent = re.sub(r'[^\w\s]', '', sent)
    sent = np.array(sent.split())
    return sent


def GetMatchingDegree(crosscomb):  # Use CNN model here and return matching degree
    return 0
