import cv2
import numpy as np
import pyrealsense2 as rs
from time import sleep
import threading

class DepthCamThread(threading.Thread):
    def __init__(self, path):
        threading.Thread.__init__(self)
        self.recording = False
        self.pipeline = None
        self.recorder = None
        self.colorwriter = None
        self.depthwriter = None
        self.pathtosavefile = path


    # call this destructor for resource cleanup
    def destructor(self):
        if self.pipeline is not None:
            self.recording = False
            sleep(0.1)
            self.pipeline.stop()
            self.pipeline = None
            self.colorwriter.release()
            self.depthwriter.release()
            self.colorwriter = None
            self.depthwriter = None
        cv2.destroyWindow("RealSense")  # it is not mandatory in this application

    #authomatically called when thread is started
    def run(self):
        print("Starting Intel RealSense Depth Cam")
        # Thread sleep so the stream has time to start recording
        self.record_rgb_depth_video()


    def record_rgb_depth_video(self):
        self.recording = True
        if self.pipeline is None:
            self.pipeline = rs.pipeline()
            self.colorwriter = cv2.VideoWriter(self.pathtosavefile + '/video.avi', cv2.VideoWriter_fourcc(*'MJPG'), 30, (640, 480), 1)
            self.depthwriter = cv2.VideoWriter(self.pathtosavefile + '/depth_video.avi', cv2.VideoWriter_fourcc(*'MJPG'), 30, (640, 480), 1)
        else:
            self.pipeline.stop()
            self.pipeline = rs.pipeline()
        path = self.pathtosavefile
        print(path)
        try:
            # Config pipeline
            config = rs.config()
            if self.recording is True:
                config.enable_record_to_file(self.pathtosavefile + '/rgb_depth_bagfile.bag')
            config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
            config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
            profile = self.pipeline.start(config)
            self.recorder = profile.get_device().as_recorder()


            sleep(0.1)
            while (self.recording):
                # Wait for a coherent pair of frames: depth and color
                frames = self.pipeline.wait_for_frames()
                depth_frame = frames.get_depth_frame()
                color_frame = frames.get_color_frame()
                if not depth_frame or not color_frame:
                    continue

                # Convert images to numpy arrays
                depth_image = np.asanyarray(depth_frame.get_data())
                color_image = np.asanyarray(color_frame.get_data())



                # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
                depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

                depth_colormap_dim = depth_colormap.shape
                color_colormap_dim = color_image.shape

                #write the frames in video writer
                self.colorwriter.write(color_image)
                self.depthwriter.write(depth_colormap)

                # If depth and color resolutions are different, resize color image to match depth image for display
                if depth_colormap_dim != color_colormap_dim:
                    resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]),
                                                     interpolation=cv2.INTER_AREA)
                    images = np.hstack((resized_color_image, depth_colormap))
                else:
                    images = np.hstack((color_image, depth_colormap))

                # Show images
                cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('RealSense', images)
                if cv2.waitKey(10) == 'q':
                    break
        finally:
            self.stop_rgb_depth_video()

    def stop_rgb_depth_video(self):
        if self.pipeline is not None:
            self.recording = False
            print("Stopping...")
            sleep(10)
            self.pipeline.stop()
            self.pipeline = None
            self.colorwriter.release()
            self.depthwriter.release()
            self.colorwriter = None
            self.depthwriter = None
            print("Stopped")


