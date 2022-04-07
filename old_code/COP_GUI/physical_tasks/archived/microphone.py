import serial
# import matplotlib.pyplot as plt
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import struct
from ast import literal_eval 
import time, datetime

import pyaudio
import wave

ser=[]
sound=[]
McTime=[]
rec= False
path= []

def audnorm(aud):
    normaud=  aud/np.amax(aud)
    return normaud

def MicConnect():
    global ser
    global rec
    ser = serial.Serial('/dev/ttyACM0',115200)
    ser.flushInput()
    rec=True
    print 'Microphone Connected'

def MicRecord(pth): 
    print(pth)
    global rec
    global sound
    global ser
    global McTime
    global path
    path = pth
    if not ser:
        print("Microphone not connected")
    else:
        while rec:
            st= ser.read()
            if int(st) == 1:
                ser_bytes = ser.read()
                ser_bytes2 = ser.read()
                LSB= ord(ser_bytes)
                MSB= ord(ser_bytes2)
                ADC= (MSB<<8)+LSB
                sound.append(ADC)
                # timestr = datetime.datetime.now().strftime('%H:%M:%S.%f')
                # McTime.append(timestr)
                McTime.append(time.time())
            else:
                print("====================================================")

def MicSave():
    global sound
    global McTime
    current_time = datetime.datetime.now().strftime('%H:%M:%S.%f')
    _filename = "%s/Microphone-%s.wav" % (path, current_time)
    _filename2 = "%s/MicrophoneDat-%s.csv" % (path, current_time)
    soundnp= np.asarray(sound)
    McTimenp= np.asarray(McTime)
    soundnp= soundnp - np.mean(soundnp)
    soundnorm= audnorm(soundnp)
    AllData= np.column_stack((McTimenp,soundnorm))
    print("Sound: "+str(soundnorm.shape)+"\t Time: "+str(McTimenp.shape)+"\t All: "+str(AllData.shape))
    np.savetxt(_filename2, (AllData), delimiter=",")
    # np.savetxt(_filename2,(AllData),delimiter=",", fmt=['%s','%.18f'])
    write(_filename,1200,soundnorm)