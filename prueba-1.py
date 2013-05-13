from Tkinter import *
import Image
import ImageTk 
import cv2


def tk(imagen):                                                                                                                                  
    root = Tk()                                                                                                                                  
    #width, height = imagen.size                                                                                                                  
    width, height = 500, 500
    canvas = Canvas(root, width=width, height=height)                                                                                            
    canvas.pack(expand=YES, fill=BOTH)                                                                                                           
    imagen_canvas = ImageTk.PhotoImage(imagen)                                                                                                   
    imagen_canvas_setting = canvas.create_image((2, 2), image=imagen_canvas, anchor=NW)                                                          
    root.mainloop()                                                                                                                              
    return  

def main():
# setup video capture
    cap = cv2.VideoCapture(0)
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 640)

    while True:
        ret,im = cap.read() 
        cv2.imshow('video test',im) 
        key = cv2.waitKey()
        print key
        if key == 27:
            break
        if key == 32:
            cv2.imwrite('vid_result.jpg',im)
main()
