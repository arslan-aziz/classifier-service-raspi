import picamera
import threading
import time
import io
import cfg

class Camera():
    thread = None
    thread_done = True
    frame = None
    last_access = 0


    def initialize(self):
        if Camera.thread_done:
            Camera.thread = threading.Thread(target=Camera.stream)
            Camera.thread.start()
            Camera.thread_done = False

            #wait until frames are available before resuming main thread
            while Camera.frame is None:
                time.sleep(0)

    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return Camera.frame

    @classmethod
    def stream(cls):
        with picamera.PiCamera() as camera:
            camera.resolution = (320,240)
            camera.hflip = False
            camera.vflip = False

            #warm up camera
            camera.start_preview()
            time.sleep(2)

            stream = io.BytesIO()
            for __ in camera.capture_continuous(stream,format = 'jpeg',use_video_port=True):

                #store frame
                stream.seek(0)
                cls.frame = stream.read()

                #reset stream for next frame
                stream.seek(0)
                stream.truncate() #resize stream to current pos = 0

                #if more than 10 seconds have passed since last call to get_frame, end capture
                if time.time() - cls.last_access > 10:
                    break
            
        cls.thread_done = True