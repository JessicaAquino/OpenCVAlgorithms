#pip install requests
#pip install python-firebase
#If from .async import process pool -> https://www.youtube.com/watch?v=TiMACTNbNl8
from firebase import firebase
import datetime, time

firebaseURL = 'https://crowdcams.firebaseio.com/'
firebase = firebase.FirebaseApplication(firebaseURL, None)

def crearDB(camara, personas, cantaglomeraciones):
   rightNow = datetime.datetime.now()
   fechaActual = rightNow.strftime("%Y-%m-%d")
   hora = rightNow.strftime("%H:%M:%S")
   newInformation = {
   'Crowds': cantaglomeraciones,
   'People': personas
   }
   destination = camara+'/information/'+fechaActual+'/'
   firebase.put(destination,hora,newInformation)
