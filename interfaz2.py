#!/usr/bin/env python3
#coding:utf-8
import ssl
import sys
import spidev
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
from tkinter import Menu
from PIL import Image, ImageTk
from time import sleep
from paho.mqtt import client
from paho.mqtt import publish
from imageMaps import GetImage
from maps import Maps
import cv2

topicMatriz = "esp32/indicadores/matrizLed"

"""spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1350000
spi.mode = 0b00
topicServo = "esp32/actuadores/servomotor


class Acquisition:
    
    def __init__(self,x1,x2,y1,y2,b=0):
        self.voltage = 0
        self.grades = 0
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.b = b
    
    
    def bitstring(self,n):
        s = bin(n)[2:]
        return '0'*(8-len(s)) + s
    
    def MCP3204(self):
        reply_bytes = spi.xfer([192,0,0,0])
        reply_bitstring = "".join(self.bitstring(n) for n in reply_bytes)
        Va = reply_bitstring[5:19]
        return int(Va,2)

    def interpolation(self,value,xp1,xp2,yp1,yp2,b=0):
        yp = ((yp2-yp1)/(xp2-xp1))*value + b
        return yp
    
    def voltage2Grads(self):
        self.voltage = 0
        for i in range(0,14):
            adc = self.MCP3204()
            self.voltage += (3.3/4095.0)*adc

        self.voltage /= 14
        self.grads = self.interpolation(self.voltage,self.x1,self.x2,self.y1,self.y2)
        return self.grads
    

data = Acquisition(0,3.3,0,180)"""
def getAddress():
    latitud = textLat.get()
    longitud = textLon.get()
    direction = Maps(latitud, longitud)
    address = direction.getLocation()
    textAddress.set(address)

def showMap():
    latitud = textLat.get()
    longitud = textLon.get()
    center = latitud + ", " + longitud
    imageHandler = GetImage("GPSImage/imageGPS",center,15,"APIKey.txt")
    imageStatus = imageHandler.getStaticGoogleMap()
    if imageStatus:
        imageFile = "GPSImage/imageGPS.jpg"
        imageGPS = cv2.imread(imageFile)
        cv2.imshow("Google Maps", imageGPS)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        textStatus.set("OK!!")
    else:
        textStatus.set("Error")
        _msgImage()

def alertActivation(alert):
    flag = 0
    while alert and not(flag):
        _msgAlert()
        sleep(3)
        flag = 1

def infoActivation(info):
    flag = 0
    while info and not(flag):
        _msgInfo()
        sleep(3)
        flag = 1
    
def sentGrads():
    grads = textGrads.get()
    if int(grads) >= 0 and int(grads) <= 180:
        mqttc.publish("esp32/actuadores/servomotor", grads)
        textGrads.set('')
    else:
        msg.showwarning("Error de Dato", "Dato fuera de rango o tipo incorrecto")
        textGrads.set('')

def sentA():
    mqttc.publish(topicMatriz, "A")

def sentB():
    mqttc.publish(topicMatriz, "B")
    
def sentC():
    mqttc.publish(topicMatriz, "C")
    
def sentD():
    mqttc.publish(topicMatriz, "D")
    
def sent0():
    mqttc.publish(topicMatriz, "0")
    
def sent1():
    mqttc. publish(topicMatriz, "1")
    
def sent2():
    mqttc.publish(topicMatriz, "2")
    
def sent3():
    mqttc.publish(topicMatriz, "3")
    
def sent4():
    mqttc.publish(topicMatriz, "4")
    
def sent5():
    mqttc.publish(topicMatriz, "5")
    
def sent6():
    mqttc.publish(topicMatriz, "6")
    
def sent7():
    mqttc.publish(topicMatriz, "7")
    
def sent8():
    mqttc.publish(topicMatriz, "8")
    
def sent9():
    mqttc.publish(topicMatriz, "9")
    
def clear():
    mqttc.publish(topicMatriz, ".")

def _msgAlert():
    msg.showwarning("Alerta MQ9","!!PELIGRO!!\nGas LP o Monoxido de carbono detectado")

def _msgInfo():
    msg.showinfo("Alerta LJ12A3","Objeto metálico DETECTADO")

def _msgImage():
    msg.showwarning("Alerta Imagen", "Error al abrir el archivo")
    
#======TKINTER=======#
win = tk.Tk()
win.title("Interfaz MQTT")
win.geometry("600x400")
win.resizable(False, False)
tabControl = ttk.Notebook(win)
tabSensors = ttk.Frame(tabControl)
tabControl.add(tabSensors, text="Sensores")
tabControl.pack(expand=1, fill="both")
#==========SENSORS======================
sensors = ttk.LabelFrame(tabSensors, text="Sensores")
sensors.grid(column=0, row=0, padx=8, pady=4)
ttk.Label(sensors, text="Fecha:").grid(column=0, row=1,pady=16)
textDate = tk.StringVar()
textDate_entered = ttk.Entry(sensors, width=8, textvariable=textDate)
textDate_entered.grid(column=1, row=1)
ttk.Label(sensors, text="Hora:").grid(column=2,row=1,padx=16)
textTime = tk.StringVar()
textTime_entered = ttk.Entry(sensors, width=6, textvariable=textTime)
textTime_entered.grid(column=3, row=1)
ttk.Label(sensors, text="Temperatura(DS18B20):").grid(column=0,row=4,pady=8)
textSensor1 = tk.StringVar()
textSensor1_entered = ttk.Entry(sensors, width=7,textvariable=textSensor1)
textSensor1_entered.grid(column=1, row=4)
ttk.Label(sensors, text="°C").grid(column=2,row=4)
ttk.Label(sensors, text="Luminosidad(BH1750):").grid(column=0, row=5, pady=8)
textSensor2 = tk.StringVar()
textSensor2_entered = ttk.Entry(sensors, width=7, textvariable=textSensor2)
textSensor2_entered.grid(column=1,row=5)
ttk.Label(sensors, text="luxes").grid(column=2, row=5)
ttk.Label(sensors, text="Humedad(DHT11):").grid(column=0, row=6, pady=8)
textSensor3 = tk.StringVar()
textSensor3_entered = ttk.Entry(sensors, width=7, textvariable=textSensor3)
textSensor3_entered.grid(column=1, row=6)
ttk.Label(sensors, text="%").grid(column=2, row=6)
ttk.Label(sensors, text="Brújula(HMC5883L):").grid(column=0, row=7, pady=8)
textSensor4 = tk.StringVar()
textSensor4_entered = ttk.Entry(sensors, width=7, textvariable=textSensor4)
textSensor4_entered.grid(column=1, row=7)
ttk.Label(sensors, text="°N").grid(column=2, row=7)
ttk.Label(sensors, text="Efecto Hall(ESP32):").grid(column=0, row=8, pady=8)
textSensor5 = tk.StringVar()
textSensor5_entered = ttk.Entry(sensors, width=7, textvariable=textSensor5)
textSensor5_entered.grid(column=1,row=8)
#======GPS TAB=======
GPS = ttk.Frame(tabControl)
tabControl.add(GPS, text="GPS")
tabGPS = ttk.LabelFrame(GPS, text="Coordenadas")
tabGPS.grid(column=0, row=0, padx=8, pady=4)
ttk.Label(tabGPS, text="Fecha:").grid(column=0, row=1,pady=16)
textDateGPS = tk.StringVar()
textDateGPS_entered = ttk.Entry(tabGPS, width=8, textvariable=textDateGPS)
textDateGPS_entered.grid(column=1, row=1)
ttk.Label(tabGPS, text="Hora:").grid(column=0,row=2,padx=16,pady=16)
textTimeGPS = tk.StringVar()
textTimeGPS_entered = ttk.Entry(tabGPS, width=6, textvariable=textTimeGPS)
textTimeGPS_entered.grid(column=1, row=2)
#======LAT=========
ttk.Label(tabGPS, text="Latitud:").grid(column=0, row=3, padx=0, pady=8)
textLat = tk.StringVar()
textLat_entered = ttk.Entry(tabGPS, width=10, textvariable=textLat)
textLat_entered.grid(column=1, row=3)
#====LON=====
ttk.Label(tabGPS, text="Longitud:").grid(column=0, row=4, padx=0, pady=8)
textLon = tk.StringVar()
textLon_entered = ttk.Entry(tabGPS, width=10, textvariable=textLon)
textLon_entered.grid(column=1, row=4)
#=====ALT======
ttk.Label(tabGPS, text="Altitud:").grid(column=0, row=5, padx=0, pady=8)
textAlt = tk.StringVar()
textAlt_entered = ttk.Entry(tabGPS, width=8, textvariable=textAlt)
textAlt_entered.grid(column=1, row=5)
#=====ADDRESS=========
ttk.Label(tabGPS, text="Direccion:").grid(column=0, row=6,padx=20, pady=8)
textAddress = tk.StringVar()
textAddress_entered = ttk.Entry(tabGPS, width=50, textvariable=textAddress)
textAddress_entered.grid(column=1, row=6)
latitud = textLat.get()
longitud = textLon.get()
#======ShowImage===========
ttk.Label(tabGPS, text="Status:").grid(column=0, row=7, padx=0, pady=8)
textStatus = tk.StringVar()
textStatus_entered = ttk.Entry(tabGPS, width=7, textvariable=textStatus)
textStatus_entered.grid(column=1, row=7)
actionAddress = ttk.Button(tabGPS, text="Dirección", command=getAddress)
actionAddress.grid(column=1, row=8)
actionMap = ttk.Button(tabGPS, text="Mapa", command=showMap)
actionMap.grid(column=1, row=10)
#=======SENT TAB==============
tabSent = ttk.Frame(tabControl)
tabControl.add(tabSent, text="Controles")
controls = ttk.LabelFrame(tabSent, text="Actuadores e indicadores")
controls.grid(column=0, row=0)
#=======SERVOMOTOR===============
ttk.Label(controls, text="Grados Servomotor:").grid(column=0, row=1, padx=0, pady=8)
textGrads = tk.StringVar()
textGrads_entered = ttk.Entry(controls, width=5, textvariable=textGrads)
textGrads_entered.grid(column=1, row=1, padx=4, pady=8)
ttk.Label(controls, text="°").grid(column=2, row=1)
actionServo = ttk.Button(controls, text="Enviar", command=sentGrads)
actionServo.grid(column=3, row=1,padx=4)
#=========MATRIZ LED==================
ttk.Label(controls, text="Matriz Led").grid(column=0, row=2,padx=0,pady=8)
actionA = ttk.Button(controls, text="A", command=sentA)
actionA.grid(column=0, row=3,padx=4)
actionB = ttk.Button(controls, text="B", command=sentB)
actionB.grid(column=1, row=3, padx=4)
actionC = ttk.Button(controls, text="C", command=sentC)
actionC.grid(column=2, row=3, padx=4)
actionD = ttk.Button(controls, text="D", command=sentD)
actionD.grid(column=3, row=3, padx=4)
actionClear = ttk.Button(controls, text="Limpiar", command=clear).grid(column=4, row=3, padx=4, pady=4)
action0 = ttk.Button(controls, text="0", command=sent0).grid(column=0, row=4, padx=0, pady=4)
action1 = ttk.Button(controls, text="1", command=sent1).grid(column=1, row=4, padx=4, pady=4)
action2 = ttk.Button(controls, text="2", command=sent2).grid(column=2, row=4, padx=4, pady=4)
action3 = ttk.Button(controls, text="3", command=sent3).grid(column=3, row=4, padx=4, pady=4)
action4 = ttk.Button(controls, text="4", command=sent4).grid(column=4, row=4, padx=4, pady=4)
action5 = ttk.Button(controls, text="5", command=sent5).grid(column=0, row=5, padx=4, pady=4)
action6 = ttk.Button(controls, text="6", command=sent6).grid(column=1, row=5, padx=4, pady=4)
action7 = ttk.Button(controls, text="7", command=sent7).grid(column=2, row=5, padx=4, pady=4)
action8 = ttk.Button(controls, text="8", command=sent8).grid(column=3, row=5, padx=4, pady=4)
action9 = ttk.Button(controls, text="9", command=sent9).grid(column=4, row=5, padx=4, pady=4)

        
def on_connect(client,userdata,flags,rc):
    print("Connected: ",client._client_id)
    client.subscribe(topic = "esp32/sensores/gps/fecha", qos=2)
    client.subscribe(topic = "esp32/sensores/gps/hora", qos=2)
    client.subscribe(topic = "esp32/sensores/gps/altitud", qos=2)
    client.subscribe(topic = "esp32/sensores/gps/latitud", qos=2)
    client.subscribe(topic = "esp32/sensores/gps/longitud", qos=2)
    client.subscribe(topic = "esp32/sensores/ds18b20", qos=2)
    client.subscribe(topic = "esp32/sensores/bh1750", qos=2)
    client.subscribe(topic = "esp32/sensores/dht11/humedad", qos=2)
    client.subscribe(topic = "esp32/sensores/hmc5883l", qos=2)
    client.subscribe(topic = "esp32/sensores/hall", qos=2)
    client.subscribe(topic = "esp32/sensores/mq9", qos=0)
    client.subscribe(topic = "esp32/sensores/lj12a3", qos=0)
        
    
def on_message(client,userdata,message):
    #print(message.topic, message.payload.decode("utf-8"))
    if message.topic == "esp32/sensores/gps/fecha":
        textDate.set(message.payload.decode("utf-8"))
        textDateGPS.set(message.payload.decode("utf-8"))
    elif message.topic == "esp32/sensores/gps/hora":
        textTime.set(message.payload.decode("utf-8"))
        textTimeGPS.set(message.payload.decode("utf-8"))
    elif message.topic == "esp32/sensores/ds18b20":
        textSensor1.set(message.payload.decode("utf-8"))
    elif message.topic == "esp32/sensores/bh1750":
        textSensor2.set(message.payload.decode("utf-8"))
    elif message.topic == "esp32/sensores/dht11/humedad":
        textSensor3.set(message.payload.decode("utf-8"))
    elif message.topic == "esp32/sensores/hmc5883l":
        textSensor4.set(message.payload.decode("utf-8"))
    elif message.topic == "esp32/sensores/hall":
        textSensor5.set(message.payload.decode("utf-8"))
    elif message.topic == "esp32/sensores/mq9":
        sensorMq9 = float(message.payload.decode("utf-8"))
        alertActivation(sensorMq9)
    elif message.topic == "esp32/sensores/lj12a3":
        sensorInd = float(message.payload.decode("utf-8"))
        infoActivation(sensorInd)
    elif message.topic == "esp32/sensores/gps/altitud":
        textAlt.set(message.payload.decode("utf-8"))
    elif message.topic == "esp32/sensores/gps/latitud":
        textLat.set(message.payload.decode("utf-8"))
    elif message.topic == "esp32/sensores/gps/longitud":
        textLon.set(message.payload.decode("utf-8"))
    #grads = int(grads)
    #client.publish(topicServo, grads)
    
mqttc = client.Client(client_id="RaspberryBroker", clean_session=False)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect(host="127.0.0.1", port=1883)
mqttc.loop_start()
win.mainloop()