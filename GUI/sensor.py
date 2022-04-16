
import platform
import sys


osDic = {"Darwin": "MacOS/plux.so",
         "Linux": "Linux64/plux.so",
         "Windows": f"Win{platform.architecture()[0][:2]}_{''.join(platform.python_version().split('.')[:2])}"}

sys.path.append(f"PLUX-API-Python3/{osDic[platform.system()]}")

import plux
import datetime, time , os , threading
import numpy as np


class bcolors:
    ENDC = '\033[0m'

    ERROR = '\033[1;31m'
    WARNING = '\033[30;41m'

    GOOD =  '\033[1;96m'

    BOLD = '\033[1m'

    MBIENT = '\033[34m'
    BCI = '\033[35m'
    PLUX = '\033[36m'



class MyDevice(plux.MemoryDev):

   
    def __init__(self, address):
        plux.MemoryDev.__init__(address)
        self.duration = 0
        self.frequency = 0
        self.plux_file = None
        self.PluxLoggingFlag = False
        self.exitPluxLoop  = False

    def onRawFrame(self, nSeq, data):
        
        if self.PluxLoggingFlag:
            if self.plux_file is not None:
                timestr=datetime.datetime.now().strftime('%H:%M:%S.%f')
                self.plux_file.write("{0:s},{1:f},{2:f},{3:f}\n".format(timestr, data[0], data[1], data[2]))
            else:
                print(bcolors.ERROR + "--Plux-- ERROR at RawFrame() - Can't write to file" + bcolors.ENDC)

        if nSeq % 1000 == 0:
           print(bcolors.PLUX + "--Plux-- ", nSeq, data  , bcolors.ENDC)# Print out a data frame every 1000 frames)


        if self.exitPluxLoop:
            print(bcolors.GOOD + "--Plux-- Exiting Plux Loop" + bcolors.ENDC)
            return True

        return False


    def onEvent(self, event):
        if type(event) == plux.Event.DigInUpdate:
            print(bcolors.PLUX + '--Plux-- Digital input event - Clock source:', event.timestamp.source, \
                  ' Clock value:', event.timestamp.value, ' New input state:', event.state, bcolors.ENDC)
        elif type(event) == plux.Event.SchedChange:
            print('--Plux-- Schedule change event - Action:', event.action, \
                  ' Schedule start time:', event.schedStartTime)
        elif type(event) == plux.Event.Sync:
            print('--Plux-- Sync event:')
            for tstamp in event.timestamps:
                print(' Clock source:', tstamp.source, ' Clock value:', tstamp.value)
        elif type(event) == plux.Event.Disconnect:
            print('--Plux-- Disconnect event - Reason:', event.reason)
            return True # Exit loop() after receiving a disconnect event
        return False

    def onInterrupt(self, param):
        print('--Plux-- Interrupt:', param)
        return False

    def onTimeout(self):
        print('--Plux-- Timeout')
        return False

    def onSessionRawFrame(self, nSeq, data):
        print >>self.f, nSeq, self.lastDigState,
        for val in data:
            print >>self.f, val,
        print >>self.f
        if nSeq % 1000 == 0:
            print('--Plux-- Session:', nSeq, data)
        return False

    def onSessionEvent(self, event):
        if type(event) == plux.Event.DigInUpdate:
            print('--Plux-- Session digital input event - Clock source:', event.timestamp.source, \
                  ' Clock value:', event.timestamp.value, ' New input state:', event.state)
            self.lastDigState = 1 if event.state else 0
        elif type(event) == plux.Event.Sync:
            print('--Plux-- Session sync event:')
            for tstamp in event.timestamps:
                print(' Clock source:', tstamp.source, ' Clock value:', tstamp.value)
        return False

    def return_logged_data():
        global data2
        # data3 = data2
        # data2=[]
        return data2


class SensorsHandler(threading.Thread):
    def __init__(self, path,user_id, block_id):
        threading.Thread.__init__(self)
        self.save_path = path
        self.user_id = user_id
        self.block_id = block_id
        self.ExitThread = False
        self.device = None
        self.plux_file = None

    def run(self):

        print("## Connecting biosignalsplux sensors ##")
        self.connect_sensor()

        while not self.ExitThread:
            time.sleep(0.0001)

        print("## Closing Thread##",self.name)

    def connect_sensor(self):
        """
        Handler Function to connect to the biosignalsplux sensor and create a file to write the data
        :return: None
        """

        try:
            address = "00:07:80:46:E5:C0" # MAC address of device
            self.device = MyDevice(address)  
            props = self.device.getProperties()  # get and print device properties
            if props is  not None:
                print(bcolors.GOOD + "--Plux-- Connection is established" + bcolors.ENDC)

            self.device.PluxLoggingFlag = False
            self.device.exitPluxLoop = False
            
            # port1: ECG , port2: GSR , port4: EMG
            src_a = plux.Source()
            src_a.port = 1

            src_b = plux.Source()
            src_b.port = 2

            src_c = plux.Source()
            src_c.port = 4

            frequency=1000

            self.device.start(frequency, (src_a, src_b, src_c))

            print(bcolors.GOOD + "--Plux-- Started Streaming" + bcolors.ENDC)

            self.device.loop()  # calls device.onRawFrame until it returns True

            time.sleep(0.01)

            self.device.stop()
            print(bcolors.GOOD + "--Plux-- Stopped Plux Connection" + bcolors.ENDC)

        except Exception as e:
            print(bcolors.ERROR +  "--Plux-- Error: Inside connect_sensor()" + bcolors.ENDC)
            print(bcolors.ERROR + str(e) + bcolors.ENDC)
            if (self.device):
                self.device.close()

    def PluxDataFile(self,path,user_id, block_id):
        # create a csv file with column headers for each signal
        try:
            _filename = "%s/Plux-%s_%s.csv" % (path, str(user_id),str(block_id))
            if self.plux_file is not None:
                self.plux_file.close()
                self.plux_file = None

            self.plux_file = open(_filename, "w")

            self.plux_file.write("{0},{1},{2},{3}\n".format('Time', 'ECG', 'GSR', 'EMG'))
            print(bcolors.PLUX + "--Plux-- %s is created" % _filename + bcolors.ENDC)

        except Exception as e:
            print(bcolors.ERROR + "--Plux-- Error: Inside PluxDataFile()" + bcolors.ENDC)
            print(e)
            exit(0)

    def start_recording(self):
        """
        Handler Function to start recording the sensor data
        :return:
        """ 
        self.PluxDataFile(self.save_path, self.user_id, self.block_id)
        self.device.plux_file = self.plux_file
        self.device.PluxLoggingFlag = True
        self.device.exitPluxLoop = False
        print(bcolors.GOOD + "--Plux-- Starting to Log Data" + bcolors.ENDC)


    def close_sensor(self):
        """
         Handler function to disconnect and close the sensor
         :return: None
        """

        # Set variable to stop recording from biosignalsplux

        self.device.PluxLoggingFlag = False
        self.device.exitPluxLoop = True

        if self.device is not None:
            time.sleep(0.2)
            self.device.close()
            print(bcolors.GOOD + "--Plux-- Closed Plux Connection" + bcolors.ENDC)
        else:
            print(bcolors.ERROR + "--Plux-- Error: Dev is not initialized - Line 233" + bcolors.ENDC)

        if self.plux_file is not None:
            time.sleep(0.01)
            self.plux_file.close()
            self.plux_file = None
            print(bcolors.GOOD + "--Plux-- Closed Plux File" + bcolors.ENDC)

        self.ExitThread = True


if __name__ == '__main__':

    path = r"C:\Sensor"

    User_ID = 6
    Block_Id = 2

    sensor = SensorsHandler(path, User_ID, Block_Id)
    sensor.start()

    time.sleep(5)

    sensor.start_recording()

    time.sleep(10)

    sensor.close_sensor()
