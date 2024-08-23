# sincronico
import sys
import cv2
import time
import os
from typing import Optional
from vimba import *
import threading

ancho = 800
size = 1
FPS = 30
Exp = 10
timestr = ""
changed = False
duracion = 86400
start = 0

def update(x):
    global changed
    changed = True
    return

def setCamera(cam):
    global size, FPS, Exp, changed, duracion
    frameRateRange = cam.AcquisitionFrameRate.get_range()
    expRange = cam.ExposureTime.get_range()
#     print(frameRateRange)
#     print(expRange)
    tiempoTotal = cv2.getTrackbarPos("Length [s]", "Trackbars")
    
    if tiempoTotal !=0:
        duracion = tiempoTotal
    else:
        duracion = 86400
        
    size = cv2.getTrackbarPos("Size", "Trackbars")
    
    Exp =  cv2.getTrackbarPos("Exp [ms]", "Trackbars")
    if Exp < expRange[0]:
        Exp = int(expRange[0]+1)
        cv2.setTrackbarPos("Exp [ms]", "Trackbars", Exp)
    elif Exp > expRange[1]:
        Exp = int(expRange[1])
        cv2.setTrackbarPos("Exp [ms]", "Trackbars", Exp)
        
    FPS = cv2.getTrackbarPos("FPS", "Trackbars")
    if FPS < frameRateRange[0]:
        FPS = int(frameRateRange[0]+1)
        cv2.setTrackbarPos("FPS", "Trackbars", FPS)
    elif FPS > frameRateRange[1]:
        FPS = int(frameRateRange[1])
        cv2.setTrackbarPos("FPS", "Trackbars", FPS)

#     print("changed")
#     cam.ExposureAuto.set('Off')
#     cam.ExposureMode.set('Timed')
#     cam.AcquisitionFrameRateEnable.set(True)
     
    if (size == 0):
        ancho = 480
    elif (size == 1):
        ancho = 800
    elif (size ==2):
        ancho = 1200
    elif (size == 3):
        ancho = 2592

    alto = ancho *3/4
    cam.Width.set(ancho)
    cam.Height.set(alto)
    cam.AcquisitionFrameRate.set(FPS)
    expValue = Exp*1000
    cam.ExposureTime.set(expValue)
    changed = False
    return

def main():
    cv2.namedWindow("Trackbars",cv2.WINDOW_GUI_NORMAL)
    cv2.resizeWindow("Trackbars", 400,100)
    cv2.createTrackbar("Size", "Trackbars", 1, 3, update)
    cv2.createTrackbar("FPS", "Trackbars", 30, 65, update)
    cv2.createTrackbar("Exp [ms]","Trackbars",10,50, update)
    cv2.createTrackbar("Length [s]", "Trackbars", 0, 30, update)
    cv2.waitKey(1)

    with Vimba.get_instance() as vimba:
        cams = vimba.get_all_cameras()
        with cams[0] as cam:
            cam.ExposureAuto.set('Off')
            cam.ExposureMode.set('Timed')
            cam.AcquisitionFrameRateEnable.set(True)
            cv_fmts = intersect_pixel_formats(cam.get_pixel_formats(), OPENCV_PIXEL_FORMATS)
            mono_fmts = intersect_pixel_formats(cv_fmts, MONO_PIXEL_FORMATS)    
            cam.set_pixel_format(mono_fmts[0])
            while (True):
                if (changed):
                    setCamera(cam)
                frame = cam.get_frame()
                cv2.imshow('VimbaPeron!     Set Parameters--->Press <Enter> to RECORD',frame.as_opencv_image())
                if cv2.waitKey(1) & 0xFF == 13:  #ord('q')
                    cv2.destroyAllWindows()
                    break


def print_preamble():
    print('///////////////////////////////////////////////////////')
    print('///                Start Recording                  ///')
    print('///////////////////////////////////////////////////////\n')


def print_usage():
    print('Usage:')
    print('    python asynchronous_grab_opencv.py [camera_id]')
    print('    python asynchronous_grab_opencv.py [/h] [-h]')
    print()
    print('Parameters:')
    print('    camera_id   ID of the camera to use (using first camera if not specified)')
    print()


def abort(reason: str, return_code: int = 1, usage: bool = False):
    print(reason + '\n')

    if usage:
        print_usage()

    sys.exit(return_code)


def parse_args() -> Optional[str]:
    args = sys.argv[1:]
    argc = len(args)

    for arg in args:
        if arg in ('/h', '-h'):
            print_usage()
            sys.exit(0)

    if argc > 1:
        abort(reason="Invalid number of arguments. Abort.", return_code=2, usage=True)

    return None if argc == 0 else args[0]


def get_camera(camera_id: Optional[str]) -> Camera:
    with Vimba.get_instance() as vimba:
        if camera_id:
            try:
                return vimba.get_camera_by_id(camera_id)

            except VimbaCameraError:
                abort('Failed to access Camera \'{}\'. Abort.'.format(camera_id))

        else:
            cams = vimba.get_all_cameras()
            if not cams:
                abort('No Cameras accessible. Abort.')

            return cams[0]


def setup_camera(cam: Camera):
    global ancho, size, FPS, Exp, timestr

    with cam:
        try:
            cam.ExposureAuto.set('Off')
            cam.ExposureMode.set('Timed')
            cam.AcquisitionFrameRateEnable.set(True)
            
            width = cam.Width
            height = cam.Height
            frame_rate = cam.AcquisitionFrameRate
            shutter = cam.ExposureTime
            shutter.set(30)
            
          
            if (size == 0):
                ancho = 480
            elif (size == 1):
                ancho = 800
            elif (size ==2):
                ancho = 1200
            elif (size == 3):
                ancho = 2592
                
            tiempoExp =  shutter.get()/1000
            alto = ancho *3/4
            width.set(ancho)
            height.set(alto)
            frame_rate.set(FPS)
            expValue = Exp*1000
            shutter.set(expValue)
                    
            ancho = width.get()
            alto = height.get()
            tiempoExp = shutter.get()/1000
            fps = frame_rate.get()
            print('Width x Height: {}x{}'.format(ancho, alto))
            print("FPS: {:.3f}" .format(fps))
            print("Exposure Time: {:.2f} ms" .format(tiempoExp))
            if duracion == 86400:
                print("Length: not set")
            else:
                print("Length: {} seconds".format(duracion))
            
        except (AttributeError, VimbaFeatureError):
            print(VimbaFeatureError)
            print("error en setup FeatureError")
            pass
        
        # Query available, open_cv compatible pixel formats
        # prefer color formats over monochrome formats
        cv_fmts = intersect_pixel_formats(cam.get_pixel_formats(), OPENCV_PIXEL_FORMATS)
        mono_fmts = intersect_pixel_formats(cv_fmts, MONO_PIXEL_FORMATS)
        cam.set_pixel_format(mono_fmts[0])
        timestr = time.strftime("/%Y-%m-%d_%H%M%S") + ".avi"
        path = os.path.dirname(os.path.abspath(__file__))
        print(path)
        fullpath = path + timestr
        print(fullpath)
        print("Saved to file: {}".format(fullpath))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(fullpath,fourcc, fps, (ancho,alto),0)
        cv2.destroyAllWindows()   #/////////////////////////////ver si se puede sacar///
        
        return out


class Handler:
    def __init__(self, out):
        self.shutdown_event = threading.Event()
        self.out = out
        self.start = 0
        self.inicio = 2525394545
        
    def __call__(self, cam: Camera, frame: Frame):
        global duracion
        if self.start == 0:
            self.inicio =time.time()
            self.start = 1
            
        ENTER_KEY_CODE = 13
        elapsed = time.time()-self.inicio
#         print(elapsed)
        
        key = cv2.waitKey(1)
        if ((key == ENTER_KEY_CODE) or (elapsed>duracion)):
            self.shutdown_event.set()
            return

        elif frame.get_status() == FrameStatus.Complete:
            #print('{} acquired {}'.format(cam, frame), flush=True)
            msg = 'VimbaPeron!     Recording to {} --->Press <Enter> to STOP'
            cuadro = frame.as_opencv_image()
            cv2.imshow(msg.format(timestr), cuadro)
            self.out.write(cuadro)
        cam.queue_frame(frame)


def main2():
    print_preamble()
    cam_id = parse_args()

    with Vimba.get_instance():
        with get_camera(cam_id) as cam:
            out = setup_camera(cam)
            handler = Handler(out)
            try:
                # Start Streaming with a custom a buffer of 10 Frames (defaults to 5)
                cam.start_streaming(handler=handler, buffer_count=10)
                handler.shutdown_event.wait()

            finally:
                cam.stop_streaming()
                out.release()

main()
main2()
