from openbci import cyton as bci
import time, datetime
import glob
from scipy import signal
import numpy as np


class bcolors:
    ENDC = '\033[0m'

    ERROR = '\033[1;31m'
    WARNING = '\033[30;41m'

    GOOD =  '\033[1;95m'

    BOLD = '\033[1m'

    MBIENT = '\033[34m'
    BCI = '\033[35m'
    PLUX = '\033[36m'

bciBoard = None
bciFile = None
exitBCILoop = False
BCILoggingFlag = False

ready = 0
paused = False

raw_channels = [[1], [2], [3], [4], [5], [6], [7], [8]]
status_channels = [-1, -1, -1, -1, -1, -1, -1, -1]
data_checked = [False, False, False, False]


def print_channels_status():
    global status_channels

    if 0 in status_channels or -1 in status_channels:
        colors = ['Gray', 'Purple', 'Blue', 'Green', 'Yellow', 'Orange', 'Red', 'Brown']
        msg = 'Channels Status: '
        for i in range(len(status_channels)):
            if status_channels[i] != 1:
                msg += '{} '.format(colors[i])
        print bcolors.ERROR + '--BCI-- {} are/is not connected properly'.format(msg) + bcolors.ENDC


def checkrail(data):
    def butter_highpass(cutoff, fs, order=5):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
        return b, a

    def butter_highpass_filter(data, cutoff, fs, order=5):
        b, a = butter_highpass(cutoff, fs, order=order)
        y = signal.filtfilt(b, a, data)
        return y

    if len(data) < 256:
        return -1

    fil= butter_highpass_filter(data, 1, 256, order=1)
    a=fil[(fil.size/2):]
    if (int(np.mean(a))==0):
        return 0
    return 1

def save_to_BCI_file(sample):
    global bciFile
    global BCILoggingFlag
    global paused
    global raw_channels
    global status_channels
    global data_checked

    if BCILoggingFlag:
        if bciFile is not None:
            bciFile.write("{0:f}, {1}, \
                {2:f}, {3:f}, {4:f}, {5:f}, {6:f}, {7:f}, {8:f}, {9:f},\
                {10:f}, {11:f}, {12:f}\n".format(
                time.time(), sample.id,
                sample.channel_data[0], sample.channel_data[1], sample.channel_data[2], sample.channel_data[3],
                sample.channel_data[4], sample.channel_data[5], sample.channel_data[6], sample.channel_data[7],
                sample.aux_data[0], sample.aux_data[1], sample.aux_data[2]))
        else:
            print bcolors.ERROR + "--BCI-- Error: at save_to_BCI_file() - BCI file is None" + bcolors.ENDC

    if (not paused):
        for i in range(len(raw_channels)):
            raw_channels[i].append(sample.channel_data[i])

        if (datetime.datetime.now().second % 4 == 0) and not data_checked[0]:
            data_checked = [True, False, False, False]
            status_channels[0] = checkrail(raw_channels[0])
            raw_channels[0] = []
            status_channels[1] = checkrail(raw_channels[1])
            raw_channels[1] = []
            print_channels_status()
            print bcolors.BCI + "--BCI-- {}\n\t\t\t{}".format(sample.channel_data, sample.aux_data) + bcolors.ENDC

        elif (datetime.datetime.now().second % 4 == 1) and not data_checked[1]:
            data_checked = [False, True, False, False]
            status_channels[2] = checkrail(raw_channels[2])
            raw_channels[2] = []
            status_channels[3] = checkrail(raw_channels[3])
            raw_channels[3] = []
            print_channels_status()
            print bcolors.BCI + "--BCI-- {}\n\t\t\t{}".format(sample.channel_data, sample.aux_data) + bcolors.ENDC

        elif (datetime.datetime.now().second % 4 == 2) and not data_checked[2]:
            data_checked = [False, False, True, False]
            status_channels[4] = checkrail(raw_channels[4])
            raw_channels[4] = []
            status_channels[5] = checkrail(raw_channels[5])
            raw_channels[5] = []
            print_channels_status()
            print bcolors.BCI + "--BCI-- {}\n\t\t\t{}".format(sample.channel_data, sample.aux_data) + bcolors.ENDC

        elif (datetime.datetime.now().second % 4 == 3) and not data_checked[3]:
            data_checked = [False, False, False, True]
            status_channels[6] = checkrail(raw_channels[6])
            raw_channels[6] = []
            status_channels[7] = checkrail(raw_channels[7])
            raw_channels[7] = []
            print_channels_status()
            print bcolors.BCI + "--BCI-- {}\n\t\t\t{}".format(sample.channel_data, sample.aux_data) + bcolors.ENDC

    if exitBCILoop:
        # print "--BCI-- Stopping BCI Stream"
        bciBoard.stop()
        print bcolors.GOOD + "--BCI-- Stopped BCI Stream" + bcolors.ENDC


def setup_bciBoard():
    global bciBoard
    global ready

    try:
        _port = '/dev/ttyUSB0'
        # ports = glob.glob('/dev/ttyUSB*') # Got it from cyton.py
        # print ports
        bciBoard = bci.OpenBCICyton(port=_port, scaled_output=False, log=False)
        print bcolors.GOOD + "--BCI-- Board Instantiated"+ bcolors.ENDC
        bciBoard.ser.write('v')
        ready = 1

    except Exception as e:
        print bcolors.ERROR+ "--BCI-- Error: Inside setup_bciBoard()"+ bcolors.ENDC
        print bcolors.ERROR + str(e) + bcolors.ENDC
        ready = -1

        if(bciBoard):
            bciBoard.disconnect()


def BCI_DataFile(path):
    global bciFile

    try:
        current_time = datetime.datetime.now().strftime('%Y-%m-%d__%H.%M.%S.%f')
        _filename = "%s/OpenBCI-%s.csv" % (path, current_time)

        if bciFile is not None:
            bciFile.close()
            bciFile = None

        bciFile = open(_filename, "a")
        bciFile.write("{0}, {1}, \
                        {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9},\
                        {10}, {11}, {12}\n".format(
           'Time', 'SampleID',
            'FP2', 'FP1', 'O2', 'O1', 'C4', 'C3', 'P3', 'P4',
            'ACCX', 'ACCY', 'ACCZ'))
        print bcolors.BCI + "--BCI-- %s is created" % _filename + bcolors.ENDC

    except Exception as e:
        print bcolors.ERROR +"--BCI-- Error: Inside BCI_DataFile()" + bcolors.ENDC
        print bcolors.ERROR + str(e) + bcolors.ENDC
        exit()


def BCIConnect():
    global BCILoggingFlag
    global bciBoard
    global exitBCILoop
    global paused

    print bcolors.BCI + "--BCI-- Connecting to Sensors" + bcolors.ENDC
    if bciBoard is None:
        setup_bciBoard()

    exitBCILoop = False
    BCILoggingFlag = False
    paused = False

    print bcolors.GOOD + "--BCI-- Starting to Stream BCI Data" + bcolors.ENDC
    bciBoard.start_streaming(save_to_BCI_file)


def BCIStart(path):
    global BCILoggingFlag
    global bciBoard
    global exitBCILoop
    global paused

    BCI_DataFile(path)

    exitBCILoop = False
    BCILoggingFlag = True
    paused = False
    print bcolors.GOOD + "--BCI-- Starting to Log Data" + bcolors.ENDC


def BCIPuase():
    global bciBoard
    global bciFile
    global BCILoggingFlag
    global paused

    paused = True
    BCILoggingFlag = False

    print bcolors.GOOD + "--BCI-- Pausing Logging/Printing" + bcolors.ENDC

    if bciBoard is None:
        print bcolors.ERROR + "--BCI-- BCI is not initialized" + bcolors.ENDC

    if bciFile is not None:
        time.sleep(0.1)
        bciFile.close()
        bciFile = None
        print bcolors.GOOD + "--BCI-- Closed BCI File" + bcolors.ENDC


def BCIRestart(path):
    global BCILoggingFlag
    global bciBoard
    global exitBCILoop
    global paused

    BCI_DataFile(path)

    exitBCILoop = False
    BCILoggingFlag = True
    paused = False
    print bcolors.GOOD + "--BCI-- Re-Starting to Log Data" + bcolors.ENDC


def BCIClose():
    global exitBCILoop
    global bciBoard
    global bciFile

    exitBCILoop = True


    if bciBoard is not None:
        # print "--BCI-- Closing BCI Connection after 0.1s"
        time.sleep(0.1)
        bciBoard.disconnect()
        print bcolors.GOOD + "--BCI-- Closed BCI Connection" + bcolors.ENDC
    else:
        print bcolors.ERROR + "--BCI-- Error: BCI is not initialized" + bcolors.ENDC
        # exit()

    if bciFile is not None:
        # print "--BCI-- Closing BCI File after 0.01s"
        time.sleep(0.01)
        bciFile.close()
        bciFile = None
        print bcolors.GOOD + "--BCI-- Closed BCI File" + bcolors.ENDC
