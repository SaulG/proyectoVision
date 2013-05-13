from Tkinter import *
import Image
import ImageTk 
import cv2
from subprocess import call

def main():
    vd = cv2.VideoCapture()
    vd.open(0)
    retval, image = vd.retrieve()
    vd.release()
    cv2.imwrite(".png", image)
    call(["./thumbnail.sh"])
    return

main()
