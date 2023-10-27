import xml.etree.ElementTree as ET
from CMensaje import CMensaje
import re
from datetime import datetime
from CDatosFechas import CDatosFechas
from CDatos import CDatos

class readFile():
    def __init__(self):
        self.lista_positivos_temp = []
        self.lista_negativos_temp = []
        self.lista_mensajes = []
        self.lista_sentimientos=[]
        self.lista_tipoSentimientos = []
        self.lista_fechas =[]
        self.datos_por_fecha = []
        self.lista_positivosRechazada = []
        self.lista_negativosRechazada = []
    
    def read_xml_sentimientos(self, file_content):
        root = ET.fromstring(file_content)
        NodoListaPositivos = root.findall('sentimientos_positivos')
        for nodoPositivo in NodoListaPositivos:
            lista_sentimientos_positivos = nodoPositivo.findall('palabra')
            for sentimiento_positivo in lista_sentimientos_positivos:
                sentimientoP = sentimiento_positivo.text
                positovoLower = sentimientoP.lower()
                if positovoLower in self.lista_negativos_temp:
                    self.lista_negativos_temp.remove(positovoLower)
                    self.lista_negativosRechazada.append(positovoLower)
                else:
                    self.lista_positivos_temp.append(positovoLower)
            self.imprimirPositivos(self.lista_positivos_temp)
            self.imprimirNegativosRechazada(self.lista_negativosRechazada)
        self.lista_sentimientos.append(self.lista_positivos_temp)
        NodoListaNegativos = root.findall('sentimientos_negativos')
        for nodoNegativo in NodoListaNegativos:
            lista_sentimientos_negativos = nodoNegativo.findall('palabra')
            for sentimiento_negativo in lista_sentimientos_negativos:
                sentimientoN = sentimiento_negativo.text
                negativoLower = sentimientoN.lower()
                if negativoLower in self.lista_positivos_temp:
                    self.lista_positivos_temp.remove(negativoLower)
                    self.lista_positivosRechazada.append(negativoLower)
                else:
                    self.lista_negativos_temp.append(negativoLower)
            self.imprimirNegativos(self.lista_negativos_temp)
            self.imprimirPositivosRechazada(self.lista_positivosRechazada)
        self.lista_sentimientos.append(self.lista_negativos_temp)
        self.xml_config()
    
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
    
    def imprimirPositivosRechazada(self,lista):
        print("*********Lista Sentimientos Positivos Rechazados********")
        for sentimiento in lista:
            rechazado = sentimiento
            print("Sentimiento Positivo Rechazado: ",rechazado)
        print("*********************************************")
        print("")
    
    def imprimirNegativosRechazada(self,lista):
        print("*********Lista Sentimientos Negativos Rechazados********")
        for sentimiento in lista:
            rechazado = sentimiento
            print("Sentimiento Negativo Rechazado: ",rechazado)
        print("*********************************************")
        print("")
    
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
            # if date not in self.lista_fechas:
            #     self.lista_fechas.append(date)
        self.imprimirMensajes(self.lista_mensajes)
        self.get_message_data()
        self.xml_mensajes()

    def imprimirMensajes(self,lista):
            print("*********Lista Mensajes********")
            for mensaje in lista:
                fecha = mensaje.fecha
                texto = mensaje.texto
                print("fecha: ",fecha)
                print("texto: ",texto)
            print("*********************************************")
    
    
    def get_message_data(self):
        date_format = "%d/%m/%Y"

        for mensaje in self.lista_mensajes:
            tempDate = datetime.strptime(mensaje.fecha, date_format)
            hashtags = re.findall(r'#\w+#', mensaje.texto)
            menciones = re.findall(r'@\w+', mensaje.texto)

            # Busca si ya existe una instancia de CDatos para la fecha
            data_existente = None
            for data in self.datos_por_fecha:
                if data.fecha == tempDate:
                    data_existente = data
                    break

            if data_existente:
                data_existente.hashtags.extend(hashtags)
                data_existente.menciones.extend(menciones)
                data_existente.mensajes += 1
            else:
                nueva_data = CDatos(tempDate)
                nueva_data.hashtags.extend(hashtags)
                nueva_data.menciones.extend(menciones)
                nueva_data.mensajes = 1
                self.datos_por_fecha.append(nueva_data)

        for datos in self.datos_por_fecha:
            print("Fecha:", datos.fecha)
            print("Contador hashtags:", len(datos.hashtags))
            print("Contador menciones:", len(datos.menciones))
            print("Contador mensajes:", datos.mensajes)
    
    
    
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
    
    
    def xml_mensajes(self):
        padre = ET.Element('MENSAJES_RECIBIDOS')
        lista_datos_por_fecha = self.datos_por_fecha
        
        for dato in lista_datos_por_fecha:
            nodoTiempo = ET.SubElement(padre,'TIEMPO')
            nodoFecha = ET.SubElement(nodoTiempo,'FECHA')
            fecha_formateada = dato.fecha.strftime("%d/%m/%Y")
            nodoFecha.text = fecha_formateada
            nodoMensaje = ET.SubElement(nodoTiempo,'MSJ_RECIBIDOS')
            nodoMensaje.text = str(dato.mensajes)
            nodoMenciones = ET.SubElement(nodoTiempo,'USR_MENCIONADOS')
            nodoMenciones.text = str(len(dato.menciones))
            nodoHashtags = ET.SubElement(nodoTiempo,'HASH_INCLUIDOS')
            nodoHashtags.text = str(len(dato.hashtags))
        self.prettify_xml(padre)
        tree = ET.ElementTree(padre)
        tree.write("resumenMensajes.xml",encoding="UTF-8",xml_declaration=True)
    
    
    
    def xml_config(self):
        padre = ET.Element('CONFIG_RECIBIDA')
        
        nodoPalabrasPositivas = ET.SubElement(padre,'PALABRAS_POSITIVAS')
        nodoPalabrasPositivas.text = str(len(self.lista_positivos_temp))
        nodoPositivasRechazadas = ET.SubElement(padre,'PALABRAS_POSITIVAS_RECHAZADA')
        nodoPositivasRechazadas.text = str(len(self.lista_positivosRechazada))
        nodoPalabrasNegativas = ET.SubElement(padre,'PALABRAS_NEGATIVAS')
        nodoPalabrasNegativas.text = str(len(self.lista_negativos_temp))
        nodoNegativasRechazadas = ET.SubElement(padre,'PALABRAS_NEGATIVAS_RECHAZADA')
        nodoNegativasRechazadas.text = str(len(self.lista_negativosRechazada))
        
        self.prettify_xml(padre)
        tree = ET.ElementTree(padre)
        tree.write("resumenConfig.xml",encoding="UTF-8",xml_declaration=True)

    
    def prettify_xml(self,element, indent='    '):
        queue = [(0, element)]  # (level, element)
        while queue:
            level, element = queue.pop(0)
            children = [(level + 1, child) for child in list(element)]
            if children:
                element.text = '\n' + indent * (level+1) 
            if queue:
                element.tail = '\n' + indent * queue[0][0]  
            else:
                element.tail = '\n' + indent * (level-1)  
            queue[0:0] = children
    
    def clear_lists(self):
        self.lista_positivos_temp = []
        self.lista_negativos_temp = []
        self.lista_mensajes = []
        self.lista_sentimientos=[]
        self.lista_tipoSentimientos = []
        self.lista_fechas =[]
        self.datos_por_fecha = []
        self.lista_positivosRechazada = []
        self.lista_negativosRechazada = []