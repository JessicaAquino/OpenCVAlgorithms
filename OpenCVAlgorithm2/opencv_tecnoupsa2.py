import cv2
import numpy as np
from statistics import mean
from FirebaseApp import *
#pip install statistics
#pip install dnspython

#FUNCIONES PARA EL PROGRAMA
global sendToDB
global banderaDB
global segundosEsperaAlarma
global segundosEsperaBD

nombreCamara = "cAirport"
bandera = False
banderaDB = False
segundosEsperaAlarma = 5    #
segundosEsperaBD = 10       #1 hora = 3600 segundos

aglomeraciones = 0

sendToDB = datetime.datetime.now() + datetime.timedelta(seconds=segundosEsperaBD)

def Average(lst):
    return mean(lst)

#ALGORITMO OPENCV

cap = cv2.VideoCapture("airport_test.mp4") #http://192.168.0.104:4747/mjpegfeed?640x480
frame_width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH)) #

frame_height =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT)) #

fourcc = cv2.VideoWriter_fourcc('X','V','I','D')

out = cv2.VideoWriter("output.avi", fourcc, 5.0, (1280, 720))#(1280,720)) #avi

ret, frame1 = cap.read()
ret, frame2 = cap.read()
print(frame1.shape)


while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contador = 0
    listaPersonas = []
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 1000:
            continue
        elif (cv2.contourArea(contour) > 1000) and (cv2.contourArea(contour) <= 4500):
            #cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # bandera = False
            #DESCOMENTAR SOLAMENTE CUANDO LAS AREAS ESTÉN BIEN DEFINIDAS, CASO CONTRARIO NUNCA VA A SONAR LA ALARMA :) Salu2
            contador = contador + 1

        elif (cv2.contourArea(contour) > 4500) and (cv2.contourArea(contour) < 15000):  #Que el cronometro aun no fue inicializado
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 0, 255), 4)
            cv2.rectangle(frame1, (200, 450), (350, 300), (0, 0, 255), 4)
            cv2.putText(frame1, "ALERTA: {}".format('AGLOMERACION'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 3)

            if bandera == False:
                then = datetime.datetime.now() + datetime.timedelta(seconds=segundosEsperaAlarma)
                bandera = True
                print("Bandera activada")
                aglomeraciones = aglomeraciones + 1

            elif then <= datetime.datetime.now() and bandera == True:
                print ("Encender alarma")
                activarAlarma(nombreCamara)
                bandera = False

    #ENVIO A LA BASE DE DATOS MONGODB A TRAVES DE LA FUNCION crearDB

    print("CONTADOR: ", contador, " AGLOMERACIONES: ", aglomeraciones)
    listaPersonas.append(contador)

    if sendToDB <= datetime.datetime.now() and banderaDB == False:
       promListaPersonas = Average(listaPersonas)
       crearDB(nombreCamara, round(promListaPersonas, 0), aglomeraciones) #FUNCION PARA MANDAR A LA BD (NOMBRE CAMARA, CANTPERSONAS, NROAGLOMERACIONES)
       print ("Datos subidos a la BD con el promedio ", promListaPersonas)
       listaPersonas.clear()
       contador = 0
       aglomeraciones = 0
       banderaDB = True


    if banderaDB == True:
       sendToDB = datetime.datetime.now() + datetime.timedelta(seconds=segundosEsperaBD)
       banderaDB = False

    #CONTINUACION ALGORITMO OPENCV

    image = cv2.resize(frame1, (1280,720))
    out.write(image)
    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(40) == 27:
        end = time.time()
        print(end - start)
        #break

cv2.destroyAllWindows()
cap.release()
out.release()
