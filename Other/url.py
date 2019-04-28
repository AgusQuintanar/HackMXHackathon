import pandas as pd
import numpy as np
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import sklearn.utils

data = pd.read_csv("urldata.csv")

num_good = data.label.value_counts()["good"]
num_bad = data.label.value_counts()["bad"]
print(num_bad/num_good, "\n")

#Shuffle del data set y verificar que la proporción es cercana a la orginal

df = sklearn.utils.shuffle(data)
data = df[:50000] #Manejando solo 50000 variables para ser mas practicos

num_good = data_m.label.value_counts()["good"]
num_bad = data_m.label.value_counts()["bad"]
print(num_bad/num_good, "\n")

def maketokens(f):
    tkns_slash = str(f.encode("utf-8")).split("/")
    tokens_total = []
    for i in tkns_slash:
        tokens = str(i).split("-") #Tokens hechos después de separar por un guión
        tkns_punto = []
        for j in range(0, len(tokens)):
            temp_tokens = str(tokens[j]).split(".")
            tkns_punto = tkns_punto + temp_tokens
        tokens_total = tokens_total + tokens + tkns_punto
        tokens_total = list(set(tokens_total))
        if "com" in tokens_total:
            tokens_total.remove("com")
        return tokens_total

lista = data["url"]
y = data["url"]
vectorizer = TfidfVectorizer(tokenizer=maketokens)
x = vectorizer.fit_transform(lista)
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=.2, random_state=42)
logit = LogisticRegression(solver='lbfgs', multi_class='auto')
logit.fit(x_train, y_train)
print("Exactitud: ", logit.score(x_test, y_test, "\n"))

#Ejemplo de la predicción

x_predict = ["diaryofagameaddict.com",
             "google.com/",
             "tubemoviez.com",
             "http://matbea4land.tilda.ws"
            ]

