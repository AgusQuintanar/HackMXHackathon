
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
		self.limiteRiesgo=15
		self.riesgoActual=0
		self.contadorPeligro = 0

	def insertar(self,valor, nivel):
		if self.raiz==None:
			self.raiz=nodo(valor, nivel)
		else:
			self._insertar(valor,self.raiz, nivel)

	def _insertar(self,valor,nodoActual, nivel):
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
	
	def buscar(self,valor):
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

	def _imprimirArbol(self,nodoActual):
		if nodoActual!=None:
			self._imprimirArbol(nodoActual.nodoI)
			print (nodoActual.valor)
			self._imprimirArbol(nodoActual.nodoD)	

arbol=Arbol()



# diccionario = {"urgente": 5, }

arbol.insertar("urgente",5)
arbol.insertar("importante",3)
arbol.insertar("pago",3)
arbol.insertar("cargo",5)
arbol.insertar("deuda",4)
arbol.insertar("inmediatamente",3)
arbol.insertar("seguridad",2)
arbol.insertar("alerta",2)
arbol.insertar("intento",1)
arbol.insertar("contraseña",3)
arbol.insertar("pin",5)
arbol.insertar("cvv",5)
arbol.insertar("bloqueado",4)
arbol.insertar("bloqueada",4)
arbol.insertar("tarjeta",3)
arbol.insertar("premio",4)
arbol.insertar("loteria",4)
arbol.insertar("valida",2)
arbol.insertar("cambie",1)
arbol.insertar("falló",2)
arbol.insertar("desorden",1)
arbol.insertar("contacto",2)
arbol.insertar("fraudulenta",3)
	

arreglo = ['cvv', 'loteria', 'manzana', 'urgente', 'fallo', 'sinceramente,', 'luis', 'delgado']

for x in arreglo:
	arbol.buscar(x)

if arbol.contadorPeligro > 0:
	print('Existe una alta probabilidad de que este sitio contenga Phishing')
else:
	print('Existe una baja probabilidad de que este sitio contenga Phishing')