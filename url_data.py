import pandas as pd
import numpy as np
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

data = pd.read_csv("urldata.csv")

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
print("Exactitud: ", logit.score(x_test, y_test))