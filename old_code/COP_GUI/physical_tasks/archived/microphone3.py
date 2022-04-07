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
sound=[[],[],[],[]]
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
    print('Microphone Connected')

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
            mdat1=[]
            mdat2=[]
            st= ser.read()
            if int(st) == 1:
                for i in range(0,4):
                    mdat1.append(ser.read())
                    mdat2.append(ser.read())
                for i in range(0,4):
                    LSB = ord(mdat1[i])
                    MSB = ord(mdat2[i])
                    ADC = (MSB << 8) + LSB
                    sound[i].append(ADC)
                # timestr = datetime.datetime.now().strftime('%H:%M:%S.%f')
                # McTime.append(timestr)
                McTime.append(time.time())
            else:
                print("====================================================")

def MicSave():
    global sound
    global McTime
    current_time = datetime.datetime.now().strftime('%H:%M:%S.%f')
    _filenamew1 = "%s/Microphone1-%s.wav" % (path, current_time)
    _filenamew2 = "%s/Microphone2-%s.wav" % (path, current_time)
    _filenamew3 = "%s/Microphone3-%s.wav" % (path, current_time)
    _filenamew4 = "%s/Microphone4-%s.wav" % (path, current_time)
    _filename2 = "%s/MicrophoneDat-%s.csv" % (path, current_time)
    McTimenp= np.asarray(McTime)
    soundnp = np.asarray(sound[0])
    soundnp= soundnp - np.mean(soundnp)
    soundnorm1= audnorm(soundnp)
    soundnp = np.asarray(sound[1])
    soundnp = soundnp - np.mean(soundnp)
    soundnorm2 = audnorm(soundnp)
    soundnp = np.asarray(sound[2])
    soundnp = soundnp - np.mean(soundnp)
    soundnorm3 = audnorm(soundnp)
    soundnp = np.asarray(sound[3])
    soundnp = soundnp - np.mean(soundnp)
    soundnorm4 = audnorm(soundnp)
    AllData= np.column_stack((McTimenp,soundnorm1,soundnorm2,soundnorm3,soundnorm4))
    print("Sound: "+str(soundnorm1.shape)+"\t Time: "+str(McTimenp.shape)+"\t All: "+str(AllData.shape))
    np.savetxt(_filename2, (AllData), delimiter=",")
    # np.savetxt(_filename2,(AllData),delimiter=",", fmt=['%s','%.18f'])
    write(_filenamew1,1200,soundnorm1)
    write(_filenamew2, 1200, soundnorm2)
    write(_filenamew3, 1200, soundnorm3)
    write(_filenamew4, 1200, soundnorm4)
