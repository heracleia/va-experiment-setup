from DepthCamera import DepthCamThread


if __name__ == '__main__':
    print("Starting test module for intel realsense depth cam...")
    thread1 = DepthCamThread("TestFolder")
    thread1.start()


