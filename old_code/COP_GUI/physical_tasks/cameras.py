import numpy as np
import cv2
import threading
import time
import os

class bcolors:
    ENDC = '\033[0m'

    ERROR = '\033[1;31m'
    WARNING = '\033[30;41m'

    GOOD =  '\033[1;32m' # Green

    BOLD = '\033[1m'

    MBIENT = '\033[34m'
    BCI = '\033[35m'
    PLUX = '\033[36m'


close_camera = False

class camThread(threading.Thread):
    def __init__(self, path, log):
        threading.Thread.__init__(self)
        self.path = path
        self.log = log
        self.counter = 0
        self.name1 = "Main Camera - {0:0.3f}".format(time.time())
        self.name2 = "Second Camera - {0:0.3f}".format(time.time())

    def run(self):
        global close_camera
        print bcolors.BOLD + "\n\n--Cameras-- Opening the Cameras ...###" + bcolors.ENDC

        filename1 = '{}/MainCamera.avi'.format(self.path)
        cam1 = cv2.VideoCapture(0)
        if self.log:
            out1 = cv2.VideoWriter(filename1, cv2.VideoWriter_fourcc(*'XVID'), 30.0, (640,480))

        if cam1.isOpened():  # try to get the first frame
            rval1, frame1 = cam1.read()
            print bcolors.BOLD + "--Cameras-- Main Camera is Connected ###" + bcolors.ENDC
        else:
            rval1 = False

        time.sleep(0.01)

        filename2 = '{}/SecondaryCamera.avi'.format(self.path)
        cam2 = cv2.VideoCapture(1)
        if self.log:
            out2 = cv2.VideoWriter(filename2, cv2.VideoWriter_fourcc(*'XVID'), 30.0, (640,480))

        if cam2.isOpened():  # try to get the first frame
            rval2, frame2 = cam2.read()
            print bcolors.BOLD + "--Cameras-- Secondary Camera is Connected ###" + bcolors.ENDC
        else:
            rval2 = False

        t0 = time.time()
        t1 = time.time()
        fps = []


        while rval1 and rval2 and not close_camera:
            if (time.time() - t0) > 1:
                fps.append(self.counter)
                self.counter = 0
                t0 = time.time()
            else:
                self.counter += 1


            if (time.time() - t1) > 3:
                print "--Cameras-- {0:0.1f} FPS in average ###".format(float(sum(fps)) / len(fps))
                fps = []
                t1 = time.time()


            time.sleep(0.001)

            rval1, frame1 = cam1.read()

            rval2, frame2 = cam2.read()
            frame2 = cv2.flip(frame2, -1)


            if self.log:
                out1.write(frame1)
                out2.write(frame2)
            else:
                cv2.imshow(self.name1, frame1)
                cv2.imshow(self.name2, frame2)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cam1.release()
        cam2.release()

        if self.log:
            out1.release()
            out2.release()
        else:
            cv2.destroyAllWindows()

        print bcolors.BOLD + "\n\n--Cameras-- Closed the Cameras! ###\n\n" + bcolors.ENDC


def record_cameras(path='Data/Errors', log=True):
    global close_camera
    thread1 = camThread(path, log)

    close_camera = False
    thread1.start()


if __name__ == '__main__':

    record_cameras(log=False)

    raw_input('Click Enter to Close the program!!!')
    close_camera = True

    print 'End of the main program'