import threading
import datetime, time
import random
import os, shutil
import socket
import signal

import biosignalplux
import microphone


class bcolors:
    ENDC = '\033[0m'

    ERROR = '\033[1;31m'
    WARNING = '\033[30;41m'

    GOOD =  '\033[1;32m' # Green

    BOLD = '\033[1m'

    MBIENT = '\033[34m'
    BCI = '\033[35m'
    PLUX = '\033[36m'


def newDirectory(UserID, SessionID):

    while True:
        try:
            dir = "Data/{0:02d}/{1:02d}".format(int(UserID),int(SessionID))

            if not os.path.exists(dir):
                os.makedirs(dir)
                print "### Thank you. We created {}".format(dir)
                return dir
            else:
                print(bcolors.WARNING + "{} exists. Do you want to OVERWRITE the Folder".format(dir) + bcolors.ENDC)
                msg = raw_input(bcolors.BOLD + "(y/n): " + bcolors.ENDC)
                if 'y' in msg.lower():
                    print(bcolors.BOLD + "Your Answer was Yes" + bcolors.ENDC)
                    shutil.rmtree(dir)  # removes all the subdirectories!
                    os.makedirs(dir)
                    print "### Thank you. We created {}".format(dir)
                    return dir
                else:
                    print(bcolors.ERROR + "Your Answer was No\n" + bcolors.ENDC)
                    UserID = raw_input(bcolors.BOLD + "New User ID: " + bcolors.ENDC)
                    SessionID = raw_input(bcolors.BOLD +"NewSession ID: " + bcolors.ENDC)
        except Exception as e:
            print bcolors.ERROR + str(e) + bcolors.ENDC
            UserID = raw_input(bcolors.BOLD + "New User ID: " + bcolors.ENDC)
            SessionID = raw_input(bcolors.BOLD + "NewSession ID: " + bcolors.ENDC)


def read_num(msg):
    t = ''
    while not isinstance(t, int):
        t = raw_input(bcolors.BOLD + msg + bcolors.ENDC)

        try:
            t= int(t)
        except Exception as e:
            print bcolors.ERROR + str(e) + bcolors.ENDC
    return t


def my_print(msg):

    while True:
        os.system('play -nq -t alsa synth {} sine {}'.format(0.005, 500))
        print '\n\n'
        user_input = raw_input(bcolors.BOLD + msg + '\n(y/n): ' + bcolors.ENDC)

        if 'y' in user_input.lower():
            print bcolors.BOLD + 'Your Input: Yes' + bcolors.ENDC
            return True
        elif 'n' in user_input.lower():
            print bcolors.BOLD + 'Your Input: No' + bcolors.ENDC
            return False
        else:
            print bcolors.WARNING +'Your Input "{}" was not valid. Try again!'.format(user_input) + bcolors.ENDC


def handler(signum, frame):
    print bcolors.WARNING + 'Responding to Keyboard Interrupt' + bcolors.ENDC

    try:
        # print("I am Here3")
        tPlux.close_sensor()
        tMic.close_sensor()
    except Exception as e:
        print bcolors.ERROR + str(e) + bcolors.ENDC

    exit(0)

signal.signal(signal.SIGINT, handler)


class myThreads (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.ExitThread = False
        self.Restart = False

    def run(self):

        print(bcolors.GOOD + "\n## Starting Thread {} - {} ##\n".format(self.threadID, self.name) + bcolors.ENDC)
        self.connect_sensor()

        while not self.ExitThread:
            time.sleep(0.0001)

        print(bcolors.GOOD + "## Closing Thread {} - {} ##\n".format(self.threadID, self.name) + bcolors.ENDC)

    def connect_sensor(self):

        if self.name == "Plux":
            biosignalplux.PluxConnect()
        elif self.name == "Mic":
            microphone.MicConnect()
        else:
            print bcolors.ERROR + "Error: Specify the Sensor Name to Connect" + bcolors.ENDC

    def start_sensor(self, path_task):

        if self.name == "Plux":
            biosignalplux.PluxStart(path)
        elif self.name == "Mic": 
        	microphone.MicRecord(path)

        else:
            print bcolors.ERROR + "Error: Specify the Sensor Name to Start" + bcolors.ENDC

    def pause_sensor(self):
        if self.name == "Plux":
            biosignalplux.PluxPause()
        else:
            print bcolors.ERROR + "Error: Specify the Sensor Name to Pause" + bcolors.ENDC

        time.sleep(1)

    def restart_sensor(self, path_task):

        if self.name == "Plux":
            biosignalplux.PluxRestart(path)

        else:
            print bcolors.ERROR + "Error: Specify the Sensor Name to Re-Start" + bcolors.ENDC

    def wait_for_sensor(self):
        if self.name == "Plux":
            while (biosignalplux.ready == 0):
                time.sleep(1)
            if biosignalplux.ready == -1:
                # self.close_sensor()
                # The Biosignal Plux is closed in the exception statement, so just close the thread
                self.ExitThread = True
                return -1
            else:
                print bcolors.GOOD + "--Plux-- Plux is good to go!\n\n" + bcolors.ENDC

        return 1

    def close_sensor(self):
        if self.name == "Plux":
        	biosignalplux.exitPluxLoop = True
        	biosignalplux.PluxClose()
        elif self.name == "Mic":
        	microphone.rec=False
        	microphone.MicSave()
        else:
            print bcolors.ERROR + "Error: Specify the Sensor Name to Close" + bcolors.ENDC

        self.ExitThread = True



###############################################
###############################################
###############################################
###############################################
###############################################
###############################################


print bcolors.BOLD + "\nWelcome to COPD Project\n" + bcolors.ENDC
print 'Connecting'

# Plux Connection##
tPlux = myThreads(3, "Plux")
tPlux.start()
if (tPlux.wait_for_sensor() == -1):
    exit(0)

tMic = myThreads(1, "Mic")
tMic.start()


my_print('Enter "y" when you are done with adjusting the sensors?')


tPlux.pause_sensor()

print 'Ready'

user_id = read_num('User ID: ')
SessionID = read_num('Phase: ')

path = newDirectory(user_id, SessionID)

j=0
while True:
    try:
        if j==0:
            tPlux.start_sensor(path)
            tMic.start_sensor(path)
            j+=1
    except KeyboardInterrupt:
        print 'jjjjjjjj'
        tPlux.pause_sensor()
        print 'iiiiiii'
        tMic.close_sensor()
        break

microphone.rec=False

tPlux.close_sensor()
# tMic.close_sensor()

print 'Done'

print(bcolors.GOOD+ "\n## Closeing Main Thread\n" +bcolors.ENDC)
print(bcolors.GOOD+ "Thank you!"+ bcolors.ENDC)
