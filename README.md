# VimbaPeron!
This script is used to acquire images with Allied Vision cameras using Python API of Vimba SDK. Tested on model  Alvium 1800 U-500m

Vimba for Windows can be downloaded from here:
https://www.alliedvision.com/en/products/vimba-sdk/

Requires to install openCV. It has been tested with pip install opencv-python==4.5.4.60, but will likely work with other versions.

Instructions:
1- Run VimbaPeron-1.1.py
2- set camera parameters (image size, FPS, Exposure and duration of recording)
   - available sizes in px: 0= 480, 1= 800, 2=1200 and 3=2592. This will set width, height will be calculated as width*3/4
   - exposure time and FPS values are mutually limited.
   - press enter to save parameters and start recording.
3- Video is recorded in .avi format for the time set in the previous step, or until the Enter key is pressed
4- Begin again from step 1.
