import xml.etree.ElementTree as ET
from CPositivo import CPositivo
from listaPositivos import listaPositivos
from CNegativo import CNegativo
from listaNegativos import listaNegativos
from CMensaje import CMensaje
import re
from datetime import datetime
from CDatosFechas import CDatosFechas

class readFile():
    def __init__(self):
        self.lista_positivos_temp = []
        self.lista_negativos_temp = []
        self.lista_mensajes = []
        self.lista_sentimientos=[]
        self.lista_tipoSentimientos = []
    
    def read_xml_sentimientos(self, file_content):
        root = ET.fromstring(file_content)
        NodoListaPositivos = root.findall('sentimientos_positivos')
        for nodoPositivo in NodoListaPositivos:
            lista_sentimientos_positivos = nodoPositivo.findall('palabra')
            for sentimiento_positivo in lista_sentimientos_positivos:
                sentimientoP = sentimiento_positivo.text
                PositovoLower = sentimientoP.lower()
                # nuevo_sentimientoPos= CPositivo(sentimientoP)
                self.lista_positivos_temp.append(PositovoLower)
            self.imprimirPositivos(self.lista_positivos_temp)
        self.lista_sentimientos.append(self.lista_positivos_temp)
        NodoListaNegativos = root.findall('sentimientos_negativos')
        for nodoNegativo in NodoListaNegativos:
            lista_sentimientos_negativos = nodoNegativo.findall('palabra')
            for sentimiento_negativo in lista_sentimientos_negativos:
                sentimientoN = sentimiento_negativo.text
                negativoLower = sentimientoN.lower()
                # nuevo_sentimientoNeg= CNegativo(sentimientoN)
                self.lista_negativos_temp.append(negativoLower)
            self.imprimirNegativos(self.lista_negativos_temp)
        self.lista_sentimientos.append(self.lista_negativos_temp)
        
    
    def imprimirPositivos(self,lista):
        print("*********Lista Sentimientos Positivos********")
        for sentimiento in lista:
            positivo = sentimiento
            print("Sentimiento Positivo: ",positivo)
        print("*********************************************")
        print("")
    
    def imprimirNegativos(self,lista):
        print("*********Lista Sentimientos Negativos********")
        for sentimiento in lista:
            negativo = sentimiento
            print("Sentimiento Negativo: ",negativo)
        print("*********************************************")
    
    def read_xml_mensajes(self, file_content):
        root = ET.fromstring(file_content)
        NodoListaMensajes = root.findall('MENSAJE')
        for nodoMensajes in NodoListaMensajes:
            lista_fechas = nodoMensajes.findall('FECHA')
            lista_textos = nodoMensajes.findall('TEXTO')
            for nodofecha in lista_fechas:
                patron = r'\b\d{2}/\d{2}/\d{4}\b'
                fecha = nodofecha.text
                fechas_encontradas = re.findall(patron, fecha)
                date = fechas_encontradas[0]
            for nodotexto in lista_textos:
                texto = nodotexto.text
                textoLower = texto.lower()
            nuevoMensaje= CMensaje(date,textoLower)
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
    
    
    def hashtags_by_date(self,fechainicio, fechafinal):
        hashtags_count = {}
        date_format = "%d/%m/%Y"
        firstdate = datetime.strptime(fechainicio, date_format)
        lastdate = datetime.strptime(fechafinal, date_format)
        
        for mensaje in self.lista_mensajes:
            tempDate = datetime.strptime(mensaje.fecha, date_format)
            if (firstdate <= tempDate <= lastdate):
                hashtags = re.findall(r'#\w+#', mensaje.texto)
                for hashtag in hashtags:
                    if hashtag in hashtags_count:
                        hashtags_count[hashtag] += 1
                    else:
                        hashtags_count[hashtag] = 1
        return hashtags_count

    def mentions_by_date(self,fechainicio, fechafinal):
        menciones_count = {}
        date_format = "%d/%m/%Y"
        firstdate = datetime.strptime(fechainicio, date_format)
        lastdate = datetime.strptime(fechafinal, date_format)
        
        for mensaje in self.lista_mensajes:
            tempDate = datetime.strptime(mensaje.fecha, date_format)
            if (firstdate <= tempDate <= lastdate):
                menciones_encontradas = re.findall(r'@\w+', mensaje.texto)
                for mencion in menciones_encontradas:
                    if mencion in menciones_count:
                        menciones_count[mencion] += 1
                    else:
                        menciones_count[mencion] = 1
        return menciones_count
    
    def sentimientos_by_date(self,fechainicio, fechafinal):
        contador_sentimientos = {'positivos': 0, 'negativos': 0, 'neutros': 0}
        self.return_palabras()
        date_format = "%d/%m/%Y"
        firstdate = datetime.strptime(fechainicio, date_format)
        lastdate = datetime.strptime(fechafinal, date_format)
        
        for dato in self.lista_tipoSentimientos:
            tempDate = dato.fecha
            if (firstdate <= tempDate <= lastdate):
                if dato.tipo == 'positivo':
                    contador_sentimientos['positivos'] += 1
                elif dato.tipo == 'negativo':
                    contador_sentimientos['negativos'] += 1
                elif dato.tipo == 'neutro':
                    contador_sentimientos['neutros'] += 1

        return contador_sentimientos

    def return_palabras(self):
        contador_positivas = 0
        contador_negativas = 0
        date_format = "%d/%m/%Y"
        for mensaje in self.lista_mensajes:
            palabras = mensaje.texto
            tempDate = datetime.strptime(mensaje.fecha, date_format)
            for palabra in palabras.replace("#", "").replace(",", "").replace(".", "").replace(";", "").replace("¡", "").replace("!", "").replace("?", "").replace("¿", "").split():
                if palabra in self.lista_positivos_temp:
                    contador_positivas += 1
                    print("palabra positiva: ", palabra)
                elif palabra in self.lista_negativos_temp:
                    contador_negativas += 1
                    print("palabra negativa: ", palabra)
    
            if contador_positivas > contador_negativas:
                tipo = 'positivo'
            elif contador_negativas > contador_positivas:
                tipo = 'negativo'
            else:
                tipo = 'neutro'
        
            self.lista_tipoSentimientos.append(CDatosFechas(tempDate,tipo))
            contador_positivas = 0
            contador_negativas = 0
            
        for sentimiento in self.lista_tipoSentimientos:
            fecha = sentimiento.fecha
            tipo = sentimiento.tipo
            print("fecha: ",fecha,"tipo: ",tipo)