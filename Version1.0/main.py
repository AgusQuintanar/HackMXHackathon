from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import pandas as pd
import numpy as np
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import sklearn.utils
import re

def arbol(palabras): #Creacion de un arbol binario
    class nodo:
        """docstring for nodo"""
        def __init__(self, valor ,nivel):
            self.valor = valor
            self.nodoI=None
            self.nodoD=None
            self.nivelPeligro=nivel

    class Arbol:
        def __init__(self):
            self.raiz=None
            self.limiteRiesgo=10
            self.riesgoActual=0
            self.contadorPeligro = 0

        def insertar(self,valor, nivel): #Funcion para crear un nodo
            if self.raiz==None:
                self.raiz=nodo(valor, nivel)
            else:
                self._insertar(valor,self.raiz, nivel)

        def _insertar(self,valor,nodoActual, nivel):#Funcion alternativa usada cuando la raiz ya tiene valor
            if valor<nodoActual.valor:
                if nodoActual.nodoI==None:
                    nodoActual.nodoI=nodo(valor, nivel)
                else:
                    self._insertar(valor,nodoActual.nodoI, nivel)
            elif valor>nodoActual.valor:
                if nodoActual.nodoD==None:
                    nodoActual.nodoD=nodo(valor, nivel)
                else:
                    self._insertar(valor,nodoActual.nodoD, nivel)	
            else:
                print("Valor repetido")			
        
        def buscar(self,valor):#Funcion  que busca un valor en cada nodo
            if self.raiz!=None:
                return self._buscar(valor,self.raiz)			
            else:
                return False

        def _buscar(self,valor,nodoActual):
            if valor==nodoActual.valor:
                self.riesgoActual+=nodoActual.nivelPeligro
                if self.riesgoActual>=self.limiteRiesgo:
                    self.contadorPeligro += 1
                return True
            elif valor<nodoActual.valor and nodoActual.nodoI!=None:
                return self._buscar(valor,nodoActual.nodoI)
            elif valor>nodoActual.valor and nodoActual.nodoD!=None:
                return self._buscar(valor,nodoActual.nodoD)
            return False
        def imprimirArbol(self):
            if self.raiz!=None:
                self._imprimirArbol(self.raiz)

        def _imprimirArbol(self,nodoActual): #Funcion para probar que los nodos se insertaron correctamente
            if nodoActual!=None:
                self._imprimirArbol(nodoActual.nodoI)
                print (nodoActual.valor)
                self._imprimirArbol(nodoActual.nodoD)	

    arbol=Arbol() #Crea un objeto de tipo arbol

    diccionario = {"urgente":[5, "Ninguna institución bancaria utiliza este tipo de lenguaje alarmante."], "importante":[3, ""], "pago":[3, ""], "cargo":[5, "Verificar directamente con su banco este mismo."], "deuda":[4,""], "inmediatamente":[3, "Ninguna institución bancaria utiliza este tipo de lenguaje alarmante."],
                   "seguridad":[2, ""], "alerta":[2, ""],"intento":[1, ""],"contraseña":[3, "Ninguna institucion o agente bancario debe solicitarte este tipo de información."],"pin":[5, "Ninguna institucion o agente bancario debe solicitarte este tipo de información."],"cvv":[5, "Ninguna institucion o agente bancario debe solicitarte este tipo de información."],"bloqueado":[4, "Verificar directamente con tu banco dichas acciones."],
                   "bloqueada":[4, "Verificar directamente con tu banco dichas acciones."],"tarjeta":[3, ""],"premio":[4, "Desconfía de recompensas inesperadas o desconocidas."],"ganaste":[4, "Desconfía de recompensas inesperadas o desconocidas."],"loteria":[4, "Desconfía de recompensas inesperadas o desconocidas."],"valida":[2, ""],"cambie":[1,""],
                   "falló":[2, ""],"desorden":[1, ""],"contacto":[2, ""],"fraudulenta":[3, "Realiza una doble verificación directamente con tu banco, sobre movimientos sospechosos"]}

    ### Diccionario que contiene las palabras claves para detectar phishing, incluye su valor de riesgo, asi como el mensaje 
    ## que saldria si saliera un margen mayor a 15

    for palabra in diccionario:
        arbol.insertar(palabra, diccionario[palabra][0])

    for x in palabras:
        arbol.buscar(x)

    if arbol.contadorPeligro > 0: #Si obtiene un nivel de riesgo muy alto, se lanza una advertencia
        print('\nExiste una alta probabilidad de que este correo contenga Phishing')
        texto = ""
        for x in palabras:
            if x in diccionario:
                texto += diccionario[x][1] + '\n'
        print(texto)
    else:
        print('\nExiste una baja probabilidad de que este correo contenga Phishing')


def checarUrl(x_predict):
    x_predict_temp = x_predict
    data = pd.read_csv("urldata.csv")

    num_good = data.label.value_counts()["good"]
    num_bad = data.label.value_counts()["bad"]
   
    #Shuffle del data set y verificar que la proporción es cercana a la orginal

    df = sklearn.utils.shuffle(data)
    data = df[:50000] #Manejando solo 50000 variables para ser mas practicos

    num_good = df.label.value_counts()["good"]
    num_bad = df.label.value_counts()["bad"]
   

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
    y = data["label"]
    vectorizer = TfidfVectorizer(tokenizer=maketokens)
    x = vectorizer.fit_transform(lista)
    x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=.2, random_state=42)
    logit = LogisticRegression(solver='lbfgs', multi_class='auto')
    logit.fit(x_train, y_train)
    print("Exactitud: ", logit.score(x_test, y_test), "\n")

    #Ejemplo de la predicción
    x_predict = vectorizer.transform(x_predict)
    New_predict = logit.predict(x_predict)
   
    for url in range(len(x_predict_temp)):
        print("URL: " + x_predict_temp[url] + ': ' + (' '.join(New_predict)).split(' ')[url])

def leerEmail():
    SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))

    # Call the Gmail API to fetch INBOX
    results = service.users().messages().list(userId='me',labelIds = ['INBOX']).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No messages found.")
    else:
        msg = service.users().messages().get(userId='me', id=messages[0]['id']).execute() #Ultimo mensaje recibido
        correo = msg['snippet']
        print("Correo: ",correo)
        urls = re.findall('(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+', correo)
        correo = correo.split()
        palabras = [(correo[x].lower()) for x in range(len(correo)) if correo[x] not in urls ]
        print("Urls: ",urls)
        print("Palabras: ",palabras)
    return [urls, palabras]


def main():
    leer_email = leerEmail()
    arbol(leer_email[1])
    if len(leer_email[0]) > 0:
        checarUrl(leer_email[0])

main()




