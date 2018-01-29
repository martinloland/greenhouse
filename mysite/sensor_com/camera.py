import platform, os
from time import sleep
from datetime import datetime
if platform.system() is not 'Windows':
    from picamera import PiCamera


class Camera(object):
    def __init__(self, debug, resolution):
        self.debug = False
        self.folder_url = '../media/camera/'
        self.folder_save = '../static/media/camera/'
        self.suffix = '.jpg'
        if not debug:
            self.picam = PiCamera()
            self.picam.resolution = (resolution[0], resolution[1])

    def capture(self, capture_at_night, light_on):
        if self._decide_to_capture(capture_at_night, light_on):
            if not self.debug:
                filename = datetime.now().strftime("%Y-%m-%d_%H%M%S")
                base = os.path.dirname(__file__)
                path_url = os.path.join(self.folder_url, filename+self.suffix)
                path_save = os.path.join(base, self.folder_save+filename+self.suffix)
                self.picam.start_preview()
                sleep(2)
                # self.picam.capture(path_save)
                self.picam.capture('/home/pi/greenhouse/mysite/media/camera/flower.jpg')
                # return path_url

        return self._default_image()

    def _decide_to_capture(self, capture_at_night, light_on):
        if light_on:
            return True
        elif capture_at_night:
            return True
        else:
            return False

    def _default_image(self):
        filename = 'flower'
        base = os.path.dirname(__file__)
        path_url = os.path.join(self.folder_url, filename + self.suffix)
        path_save = os.path.join(base,
                                 self.folder_save + filename + self.suffix)
        # file = path_save+'delete.txt'
        # with open(file, 'w') as f:
        #     f.write("hey")
        # print('created '+file)
        return path_url
