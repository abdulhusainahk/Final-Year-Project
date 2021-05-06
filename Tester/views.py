import math
import re
import numpy as np
from django.shortcuts import render
from gensim.models import KeyedVectors
from tensorflow.keras.layers import LSTM
from tensorflow.keras.models import load_model
# Load word to vector model
model = KeyedVectors.load('C:/Users/Admin/Data/Final_yr_project/model/wordvector')
model1=LSTM(300,return_sequences=True) # forward LSTM
model2=LSTM(300,go_backwards=True,return_sequences=True) # backward LSTM
model3=load_model('C:/Users/Admin/Data/Final_yr_project/mpsc.h5') #mpsc model for prediction

def home(request):
    if request.method == "POST":
        print('FILEs = \n', request.FILES['model-answer-sheet'], request.FILES['answer-sheet'])
        modelans = request.FILES['model-answer-sheet']
        userans = request.FILES['answer-sheet']
        for i in modelans.chunks():
            modelans = i.decode()
        for i in userans.chunks():
            userans = i.decode()
        # Here we are ready with 2 sentences now let's calculate their matching degree.
        sent1 = PreProcess(modelans)     # Data Preprocessing
        sent2 = PreProcess(userans)
        vec1 = GetOriginalSemantics(sent1)
        vec2 = GetOriginalSemantics(sent2)  # The 2 sentences are vectorized
        forwardX, backwardX = model1(vec1),model2(vec1)
        forwardY, backwardY = model1(vec2),model2(vec2)    # ofrward and backward semantic generation
        X=[vec1,forwardX,backwardX]
        Y=[vec2,forwardY,backwardY]
        semantics=[]
        for i in X:
            for j in Y:
                semantics.append(np.dot(i,j))
        semantics = np.array(semantics).reshape(1, 300, 300, 9)
        print('shape of cross combination is ',semantics.shape)
        score,accuracy = GetMatchingDegree(semantics)
        iscore = True
        return render(request, "home.html",{'iscore':iscore, 'score':score, 'accuracy':accuracy})
    else:
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


def GetOriginalSemantics(sent):
    # Apply word to vector to every word in sentence
    vec=[]
    for word in sent:
        try:
            try:
                vec.append(model[word])
            except:
                vec.append(model[word[0].upper()+word[1:]])
        except:
            pass
    extra = 300 - len(vec)
    vec = np.pad(vec, [(0, extra), (0, 0)], 'constant').reshape(1, 300, 300)
    return np.array(vec, np.float32)



def PreProcess(sent):  # tokenizing sentence into words
    sent = re.sub(r'[^\w\s]', '', sent)
    sent = np.array(sent.split())
    return sent


def GetMatchingDegree(crosscomb,outoff=5):  # Use CNN model here and return matching degree
    pos=model3.predict(crosscomb)
    threshold=0.03 # current Threshold Difference between 0 and 1
    range=threshold/outoff
    val=pos[0][0]-0.62   # 0.62 is the lower bound and 0.65 is the upper bound
    return math.floor(val/range),pos[0][0]
