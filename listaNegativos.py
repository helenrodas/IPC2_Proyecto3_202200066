from nodoNegativo import nodoNegativo
from CNegativo import CNegativo

class listaNegativos:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.contador = 0
        
    def insertar(self,CNegativo):
            nodo = nodoNegativo(CNegativo)
            if self.contador == 0:
                self.primero = nodo
                self.ultimo = nodo
            else:
                actual = self.primero
                anterior = None
                while actual is not None:
                    anterior = actual
                    actual = actual.siguiente
                if anterior is None:
                    nodo.siguiente = self.primero
                    self.primero = nodo
                else:
                    nodo.siguiente = actual
                    anterior.siguiente = nodo
            self.contador += 1

    def imprimir(self):
        print("")
        actual=self.primero
        print("*********Lista Sentimientos Negativos********")
        while actual!= None:
            print("Sentimiento Negativo:",actual.CNegativo.sentimiento)
            actual=actual.siguiente
        print("*********************************************")
    
    def __iter__(self):
        self.actual = self.primero
        return self

    def __next__(self):
        if self.actual is not None:
            valor_actual = self.actual
            self.actual = self.actual.siguiente
            return valor_actual
        else:
            raise StopIteration