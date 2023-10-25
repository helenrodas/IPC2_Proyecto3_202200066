import xml.etree.ElementTree as ET
from CPositivo import CPositivo
from listaPositivos import listaPositivos
from CNegativo import CNegativo
from listaNegativos import listaNegativos

class readFile():
    def __init__(self):
        self.lista_positivos_temp = listaPositivos()
        self.lista_negativos_temp = listaNegativos()
    
    def read_xml(self, file_content):
        root = ET.fromstring(file_content)
        NodoListaPositivos = root.findall('sentimientos_positivos')
        for nodoPositivo in NodoListaPositivos:
            lista_sentimientos_positivos = nodoPositivo.findall('palabra')
            for sentimiento_positivo in lista_sentimientos_positivos:
                sentimientoP = sentimiento_positivo.text
                nuevo_sentimientoPos= CPositivo(sentimientoP)
                self.lista_positivos_temp.insertar(nuevo_sentimientoPos)
            print(self.lista_positivos_temp.imprimir())
        NodoListaNegativos = root.findall('sentimientos_negativos')
        for nodoNegativo in NodoListaNegativos:
            lista_sentimientos_negativos = nodoNegativo.findall('palabra')
            for sentimiento_negativo in lista_sentimientos_negativos:
                sentimientoN = sentimiento_negativo.text
                nuevo_sentimientoNeg= CNegativo(sentimientoN)
                self.lista_negativos_temp.insertar(nuevo_sentimientoNeg)
            print(self.lista_negativos_temp.imprimir())