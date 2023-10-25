import xml.etree.ElementTree as ET
from CPositivo import CPositivo
from listaPositivos import listaPositivos
from CNegativo import CNegativo
from listaNegativos import listaNegativos
from CMensaje import CMensaje
import re
from datetime import datetime

class readFile():
    def __init__(self):
        self.lista_positivos_temp = []
        self.lista_negativos_temp = []
        self.lista_mensajes = []
    
    def read_xml_sentimientos(self, file_content):
        root = ET.fromstring(file_content)
        NodoListaPositivos = root.findall('sentimientos_positivos')
        for nodoPositivo in NodoListaPositivos:
            lista_sentimientos_positivos = nodoPositivo.findall('palabra')
            for sentimiento_positivo in lista_sentimientos_positivos:
                sentimientoP = sentimiento_positivo.text
                nuevo_sentimientoPos= CPositivo(sentimientoP)
                self.lista_positivos_temp.append(nuevo_sentimientoPos)
            self.imprimirPositivos(self.lista_positivos_temp)
        NodoListaNegativos = root.findall('sentimientos_negativos')
        for nodoNegativo in NodoListaNegativos:
            lista_sentimientos_negativos = nodoNegativo.findall('palabra')
            for sentimiento_negativo in lista_sentimientos_negativos:
                sentimientoN = sentimiento_negativo.text
                nuevo_sentimientoNeg= CNegativo(sentimientoN)
                self.lista_negativos_temp.append(nuevo_sentimientoNeg)
            self.imprimirNegativos(self.lista_negativos_temp)
    
    def imprimirPositivos(self,lista):
        print("*********Lista Sentimientos Positivos********")
        for sentimiento in lista:
            positivo = sentimiento.sentimiento
            print("Sentimiento Positivo: ",positivo)
        print("*********************************************")
        print("")
    
    def imprimirNegativos(self,lista):
        print("*********Lista Sentimientos Negativos********")
        for sentimiento in lista:
            negativo = sentimiento.sentimiento
            print("Sentimiento Negativo: ",negativo)
        print("*********************************************")
    
    def read_xml_mensajes(self, file_content):
        root = ET.fromstring(file_content)
        NodoListaMensajes = root.findall('MENSAJE')
        for nodoMensajes in NodoListaMensajes:
            lista_fechas = nodoMensajes.findall('FECHA')
            for nodofecha in lista_fechas:
                patron = r'\b\d{2}/\d{2}/\d{4}\b'
                fecha = nodofecha.text
                fechas_encontradas = re.findall(patron, fecha)
                date = fechas_encontradas[0]
            lista_textos = nodoMensajes.findall('TEXTO')
            for nodotexto in lista_textos:
                texto = nodotexto.text
                nuevoMensaje= CMensaje(date,texto)
            self.lista_mensajes.append(nuevoMensaje)
        self.imprimirMensajes(self.lista_mensajes)

    def imprimirMensajes(self,lista):
            print("*********Lista Mensajes********")
            for mensaje in lista:
                fecha = mensaje.fecha
                texto = mensaje.texto
                print("fecha: ",fecha)
                print("texto: ",texto)
            print("*********************************************")
    
    # def hashtags_by_date(self, FDate,LDate):
    #     hashtags_count = {}
    #     date_format = "%d/%m/%Y"
    #     firstdate = datetime.strptime(FDate,date_format)
    #     lastdate = datetime.strptime(LDate,date_format)
    #     for mensaje in self.lista_mensajes:
    #         tempDate = datetime.strptime(mensaje.fecha,date_format)
    #         if (tempDate >= firstdate) and (tempDate<=lastdate):
    #             # Divide el texto en palabras
    #             palabras = mensaje.texto.split()
    #             for palabra in palabras:
    #                 # Comprueba si la palabra contiene el carácter "#"
    #                 if "#" in palabra:
    #                     # Elimina caracteres especiales al principio y al final de la palabra
    #                     # palabra = palabra.strip("#,.;!?")
    #                     # Incrementa el contador de la palabra en el diccionario
    #                     if palabra in hashtags_count:
    #                         hashtags_count[palabra] += 1
    #                     else:
    #                         hashtags_count[palabra] = 1
    #     print("hashtags: " ,hashtags_count)
    #     return hashtags_count
    
    
    def hashtags_by_date(self,fechainicio, fechafinal):
        hashtags_count = {}
        date_format = "%d/%m/%Y"
        firstdate = datetime.strptime(fechainicio, date_format)
        lastdate = datetime.strptime(fechafinal, date_format)
        
        for mensaje in self.lista_mensajes:
            tempDate = datetime.strptime(mensaje.fecha, date_format)
            if (firstdate <= tempDate <= lastdate):
                # Divide el texto en palabras
                palabras = mensaje.texto.split()
                for palabra in palabras:
                    # Comprueba si la palabra contiene el carácter "#"
                    if "#" in palabra:
                        # Elimina caracteres especiales al principio y al final de la palabra
                        # Incrementa el contador de la palabra en el diccionario
                        if palabra in hashtags_count:
                            hashtags_count[palabra] += 1
                        else:
                            hashtags_count[palabra] = 1
        return hashtags_count