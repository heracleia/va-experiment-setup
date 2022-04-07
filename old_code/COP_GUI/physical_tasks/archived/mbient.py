# usage: python data_fuser.py [mac1] [mac2] ... [mac(n)]
from __future__ import print_function
from ctypes import c_void_p, cast, POINTER
from mbientlab.metawear import MetaWear, libmetawear, parse_value, cbindings
from time import sleep
from threading import Event
from sys import argv
import datetime, time
import pdb
from mbientlab.metawear.cbindings import *


class bcolors:
    ENDC = '\033[0m'

    ERROR = '\033[1;31m'
    WARNING = '\033[30;41m'

    GOOD =  '\033[1;94m'

    BOLD = '\033[1m'

    MBIENT = '\033[34m'
    BCI = '\033[35m'
    PLUX = '\033[36m'

states = []
MbientLoggingFlag = False
ready = 0
paused = False

Mbient_sensors = ["E1:34:B8:DD:BE:BC","F0:2E:BF:A0:AF:F1", "EB:F4:4C:2F:AE:F1", "EF:E5:4A:37:E9:17"]


class State:
    def __init__(self, device):
        self.device = device
        self.callback = cbindings.FnVoid_VoidP_DataP(self.data_handler)
        self.processor = None
        self.samples = 0
        self.deviceID = 0
        self.deviceFileHandle = None

    def data_handler(self, ctx, data):
        global MbientLoggingFlag
        global paused

        values = parse_value(data, n_elem = 3)

        if MbientLoggingFlag is True:
            if self.deviceFileHandle is not None:
                self.deviceFileHandle.write("{0:f} , {1:f}, {2:f}, {3:f}, {4:f}, {5:f}, {6:f}, {7:f}, {8:f}, {9:f}\n"
                    .format(time.time(),    values[0].x, values[0].y, values[0].z,
                                            values[1].x, values[1].y, values[1].z,
                                            values[2].x, values[2].y, values[2].z))
            else:
                print(bcolors.ERROR + "--Mbient--  ERROR at data_handler() - D%d: Mbient file  is None - cannot write to file"%self.deviceID +bcolors.ENDC)

        self.samples += 1
        if (self.samples % 100) == 0 and not paused:
            print(bcolors.MBIENT +
                  "--Mbient-- D%d: acc: (%.3f,%.3f,%.3f) \t gyro:(%.3f,%.3f,%.3f)\t mag:(%.3f,%.3f,%.3f)"
                  % (self.deviceID,
                     values[0].x, values[0].y, values[0].z,
                     values[1].x, values[1].y, values[1].z,
                     values[2].x, values[2].y, values[2].z)
                  + bcolors.ENDC)

    def setup(self):
        global ready

        if self.device.address == "E1:34:B8:DD:BE:BC":
            self.deviceID = 1
        elif self.device.address == "F0:2E:BF:A0:AF:F1":
            self.deviceID = 2
        elif self.device.address == "EB:F4:4C:2F:AE:F1":
            self.deviceID = 3
        elif self.device.address == "EF:E5:4A:37:E9:17":
            self.deviceID = 4

        # libmetawear.mbl_mw_settings_set_connection_parameters(self.device.board, 7.5, 7.5, 0, 6000)
        libmetawear.mbl_mw_settings_set_connection_parameters(self.device.board, 7.5, 7.5, 0, 15000)

        sleep(1.5)
        e = Event()

        def processor_created(context, pointer):
            global ready

            self.processor = pointer
            if self.processor == None:
                ready = -1
                print(bcolors.ERROR + "--Mbient-- Processor is None\n\t\t\t"
                                      "Use a different sensor and\n\t\t\t"
                                      "Re-Calibrate Mbient D{}".format(self.deviceID)
                      + bcolors.ENDC)
            e.set()

        fn_wrapper = cbindings.FnVoid_VoidP_VoidP(processor_created)

        acc = libmetawear.mbl_mw_acc_get_acceleration_data_signal(self.device.board)
        gyro = libmetawear.mbl_mw_gyro_bmi160_get_rotation_data_signal(self.device.board)
        mag = libmetawear.mbl_mw_mag_bmm150_get_b_field_data_signal(self.device.board)

        signals = (c_void_p * 2)()
        signals[0] = gyro
        signals[1] = mag

        libmetawear.mbl_mw_dataprocessor_fuser_create(acc, signals, 2, None, fn_wrapper)

        e.wait()

        if ready is not -1:
            libmetawear.mbl_mw_datasignal_subscribe(self.processor, None, self.callback)
        else:
            print(bcolors.ERROR + "--Mbient-- D{} failed the setup".format(
                self.deviceID) + bcolors.ENDC)

    def start(self):

        libmetawear.mbl_mw_mag_bmm150_enable_b_field_sampling(self.device.board)
        libmetawear.mbl_mw_gyro_bmi160_enable_rotation_sampling(self.device.board)
        libmetawear.mbl_mw_acc_enable_acceleration_sampling(self.device.board)

        libmetawear.mbl_mw_mag_bmm150_start(self.device.board)
        libmetawear.mbl_mw_gyro_bmi160_start(self.device.board)
        libmetawear.mbl_mw_acc_start(self.device.board)

        pattern = LedPattern(repeat_count=Const.LED_REPEAT_INDEFINITELY)
        libmetawear.mbl_mw_led_load_preset_pattern(byref(pattern), LedPreset.SOLID)
        libmetawear.mbl_mw_led_write_pattern(self.device.board, byref(pattern), LedColor.BLUE)
        libmetawear.mbl_mw_led_play(self.device.board)


def MbientFile(s, path):

    try:
        current_time = datetime.datetime.now().strftime('%Y-%m-%d__%H.%M.%S.%f')
        _filename = "%s/Mbient-D%d-%s.csv" % (path, s.deviceID, current_time)

        if s.deviceFileHandle is not None:
            s.deviceFileHandle.close()

        s.deviceFileHandle = open(_filename, "a")
        print(bcolors.MBIENT + "--Mbient--  %s is created" % _filename + bcolors.ENDC)
        s.deviceFileHandle.write("{0} , {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}\n"
                                    .format('Time', 'ACCX', 'ACCY', 'ACCZ',
                                            'GYROX','GYROY', 'GYROY',
                                            'MAGX', 'MAGY', 'MAGZ'))

    except Exception as e:
        print(bcolors.ERROR + "--Mbient--  Error: Inside MbientFile()" + bcolors.ENDC)
        print(bcolors.ERROR + str(e) + bcolors.ENDC)
        # exit(0)


def MbientConnect():
    global states
    global Mbient_sensors
    global ready
    global paused

    sensor_num = raw_input(bcolors.BOLD + "Enter Mbient ID(s) with spaces (1 2 3): " + bcolors.ENDC)

    sensor_num = list(map(int, sensor_num.split()))

    for i in range(len(sensor_num)):
        sensor_address = Mbient_sensors[sensor_num[i] - 1]
        d = MetaWear(sensor_address)

        t0 = datetime.datetime.now()
        d.connect()
        print(bcolors.GOOD +
              "--Mbient-- Device: D{} connected in {} seconds".format(sensor_num[i], (datetime.datetime.now() - t0).seconds)
              + bcolors.ENDC)

        states.append(State(d))

        t0 = datetime.datetime.now()
        states[-1].setup()

        if ready == -1:
            print(bcolors.ERROR +
                  "--Mbient-- Device: D{} failed in setup after {} seconds".format(states[-1].deviceID,
                                                                              (datetime.datetime.now() - t0).seconds)
                  + bcolors.ENDC)
            return
        else:
            print(bcolors.GOOD +
                  "--Mbient-- Device: D{} was configured correctly in {} seconds".format(states[-1].deviceID,
                                                                                (datetime.datetime.now() - t0).seconds)
                  + bcolors.ENDC)


            t0 = datetime.datetime.now()
            states[-1].start()
            print(bcolors.GOOD +
                  "--Mbient-- Device: D{} started streaming in {} seconds".format(states[-1].deviceID,
                                                                                    (datetime.datetime.now() - t0).seconds)
                  + bcolors.ENDC)
    paused = False
    ready = 1


def MbientStart(path):
    global MbientLoggingFlag
    global states
    global paused
    for s in states:
        MbientFile(s, path)
        libmetawear.mbl_mw_led_stop_and_clear(s.device.board)
        sleep(0.01)
        pattern = LedPattern(repeat_count=Const.LED_REPEAT_INDEFINITELY)
        libmetawear.mbl_mw_led_load_preset_pattern(byref(pattern), LedPreset.SOLID)
        libmetawear.mbl_mw_led_write_pattern(s.device.board, byref(pattern), LedColor.GREEN)
        libmetawear.mbl_mw_led_play(s.device.board)
        s.samples = 0

    sleep(0.01)

    print(bcolors.GOOD + "--Mbient-- Starting to Log Data ... " + bcolors.ENDC)
    MbientLoggingFlag = True
    paused = False


def MbientPuase():
    global MbientLoggingFlag
    global paused
    global states

    MbientLoggingFlag = False
    paused = True

    print(bcolors.GOOD + "--Mbient-- Pausing Mbient ..." + bcolors.ENDC)
    sleep(0.1)

    for s in states:
        if s.deviceFileHandle is not None:
            s.deviceFileHandle.close()
            print(bcolors.MBIENT + "--Mbient-- Device %d: closed.  Total Sample = %d" %
                  (s.deviceID, s.samples) + bcolors.ENDC)

        libmetawear.mbl_mw_led_stop_and_clear(s.device.board)
        sleep(0.01)
        pattern = LedPattern(repeat_count=Const.LED_REPEAT_INDEFINITELY)
        libmetawear.mbl_mw_led_load_preset_pattern(byref(pattern), LedPreset.SOLID)
        libmetawear.mbl_mw_led_write_pattern(s.device.board, byref(pattern), LedColor.BLUE)
        libmetawear.mbl_mw_led_play(s.device.board)

    print(bcolors.GOOD + "--Mbient-- All Mbient Files are Closed" + bcolors.ENDC)


def MbientRestart(path):
    global MbientLoggingFlag
    global states
    global paused
    for s in states:
        MbientFile(s, path)
        libmetawear.mbl_mw_led_stop_and_clear(s.device.board)
        sleep(0.01)
        pattern = LedPattern(repeat_count=Const.LED_REPEAT_INDEFINITELY)
        libmetawear.mbl_mw_led_load_preset_pattern(byref(pattern), LedPreset.SOLID)
        libmetawear.mbl_mw_led_write_pattern(s.device.board, byref(pattern), LedColor.GREEN)
        libmetawear.mbl_mw_led_play(s.device.board)
        s.samples = 0

    sleep(0.01)

    print(bcolors.GOOD + "--Mbient-- Re-Starting to Log Data ... " + bcolors.ENDC)
    MbientLoggingFlag = True
    paused = False


def MbientClose():
    global states
    global MbientLoggingFlag

    MbientLoggingFlag = False
    sleep(0.01)

    print(bcolors.MBIENT + "--Mbient-- Closing devices" + bcolors.ENDC)
    events = []
    for s in states:
        e = Event()
        events.append(e)

        s.device.on_disconnect = lambda s: e.set()
        # libmetawear.mbl_mw_debug_reset(s.device.board)
        print(bcolors.MBIENT + "--Mbient-- Device %d: Total Sample = %d"%(s.deviceID, s.samples) + bcolors.ENDC)

        libmetawear.mbl_mw_acc_stop(s.device.board)
        libmetawear.mbl_mw_mag_bmm150_stop(s.device.board)
        libmetawear.mbl_mw_gyro_bmi160_stop(s.device.board)

        libmetawear.mbl_mw_acc_disable_acceleration_sampling(s.device.board)
        libmetawear.mbl_mw_mag_bmm150_disable_b_field_sampling(s.device.board)
        libmetawear.mbl_mw_gyro_bmi160_disable_rotation_sampling(s.device.board)

        libmetawear.mbl_mw_datasignal_unsubscribe(s.processor)
        libmetawear.mbl_mw_debug_disconnect(s.device.board)

        libmetawear.mbl_mw_led_stop_and_clear(s.device.board)

        if s.deviceFileHandle is not None:
            s.deviceFileHandle.close()
            print(bcolors.MBIENT + "--Mbient-- Device %d: closed file" % (s.deviceID) + bcolors.ENDC)

    for e in events:
        e.wait()

    print(bcolors.GOOD + "--Mbient-- All Mbient devices are Closed" + bcolors.ENDC)



# def test():
#     print("Hello World!")

# MbientConnect()
# print("1- wait 5 seconds")
# sleep(5)
#
# MbientStart('Data/00/0')
# print("2- wait 5 seconds")
# sleep(15)

# MbientStart(0)
# sleep(15)
#
# MbientPuase()
# sleep(10)
#
# MbientRestart(0)
# sleep(10)
#
# MbientClose()