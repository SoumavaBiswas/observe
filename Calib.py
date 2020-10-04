import tkinter as tk, pyautogui as pg
from tkinter import *
from scipy.spatial import distance as dist
import cv2
import dlib
import numpy as np
import pymsgbox
class Calib:
    def __init__(self, root):
        self.intensity=0
        self.master = root
        self.w,self.h = pg.size()
        root.geometry("{0}x{1}".format(self.w, self.h))
        root.attributes("-fullscreen", True)
        self.bgc="#F49F05"
        self.abgc="#F5A81D"
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        self.xmin,self.xmax,self.ymin,self.ymax,self.EAR=0,0,0,0,0
        self.rects=None
    #Calculationg eye aspect ratio to measure blink threshold
    def eye_aspect_ratio(self,left,right,top,bottom):
        A = dist.euclidean(left,right)
        B= dist.euclidean(top, bottom)
        if B==0:
            B=1
        ear=A/B 
        return ear
    #Calculationg average intensity
    def brightnessDetector(self,gray):
    	blur=cv2.GaussianBlur(gray,(7,7),0)
    	avg=np.mean(blur,axis=(0,1))
    	return avg
    def midpoint(self,p1 ,p2):
        return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)
    
    #Calculating eye,nose points while looking at extreme screen coordinates
    def eyeDetector(self,rect,gray):
        for eye in rect:
            landmarks = self.predictor(gray, eye)
            fx,fy= (landmarks.part(30).x, landmarks.part(30).y)
            self.left_point = (landmarks.part(36).x, landmarks.part(36).y)
            self.right_point = (landmarks.part(39).x, landmarks.part(39).y)
            self.center_top = self.midpoint(landmarks.part(37), landmarks.part(38))
            self.center_bottom = self.midpoint(landmarks.part(41), landmarks.part(40))
            EAR=self.eye_aspect_ratio(self.left_point,self.right_point,self.center_top,self.center_bottom)
            return fx,fy,EAR
    #Image is captured while clicking at extream screen points
    def collect(self):
        cap = cv2.VideoCapture(-1)
        _, frame = cap.read()
        frame=cv2.flip(frame,1)
        self.gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.rects = self.detector(self.gray_frame, 0)
        self.point=self.eyeDetector(self.rects,self.gray_frame)
        self.intensity+=self.brightnessDetector(self.gray_frame) 
        print(self.point)
        cap.release()
        return self.point
    #Design of the calibration window    
    def display(self,root):
        self.b1 = tk.Button(root, text="1", borderwidth=1, highlightthickness=1, bg=self.bgc, activebackground=self.abgc, command=self.b2c,relief="flat", compound="top", font=('Arial', 30))
        self.b1.place(x=0, y=0, height=50, width=50)
        self.b2 = tk.Button(root, text="4", borderwidth=2, highlightthickness=2, bg=self.bgc, activebackground=self.abgc, state="disabled", relief="flat", font=('Arial', 30), compound="top", command=self.b5c)
        self.b2.place(x=0, y=self.h-50, height=50, width=50)
        self.b3 = tk.Button(root, text="3", borderwidth=2, highlightthickness=2, bg=self.bgc, activebackground=self.abgc, state="disabled", font=('Arial', 30), command=self.b4c, relief="flat", compound="top")
        self.b3.place(x=self.w-50, y=self.h-50, height=50, width=50)
        self.b4 = tk.Button(root, text="2", borderwidth=2, highlightthickness=2, bg=self.bgc, activebackground=self.abgc, state="disabled",font=('Arial', 30), command=self.b3c, relief="flat", compound="top")
        self.b4.place(x=self.w-50, y=0, height=50, width=50)
        self.b5 = tk.Button(root, text="OK", borderwidth=2, highlightthickness=2, bg=self.bgc, activebackground=self.abgc, state="disabled", font=('Arial', 30), command=self.Done, relief="flat", compound="top")
        self.b5.place(x=self.w/2-40, y=self.h/2-40, height=80, width=80)
    #Functions corresponding to each button
    def b2c(self):
        print('The current pointer position is {0}'.format(pg.position()))
        self.b4['state']=NORMAL
        x,y,AR=self.collect()
        self.EAR+=AR
        self.xmin+=x
        self.ymin+=y
        self.b1.destroy()
    def b3c(self):
        print('The current pointer position is {0}'.format(pg.position()))
        self.b3['state']=NORMAL
        x,y,AR=self.collect()
        self.EAR+=AR
        self.xmax+=x
        self.ymin+=y
        self.b4.destroy()
    def b4c(self):
        print('The current pointer position is {0}'.format(pg.position()))
        self.b2['state']=NORMAL
        x,y,AR=self.collect()
        self.EAR+=AR
        self.xmax+=x
        self.ymax+=y      
        self.b3.destroy()
    def b5c(self):
        print('The current pointer position is {0}'.format(pg.position()))
        self.b5['state']=NORMAL
        x,y,AR=self.collect()
        self.EAR+=AR
        self.xmin+=x
        self.ymax+=y
        self.b2.destroy()
    #Measuring the threshold values
    def Done(self):
        #pymsgbox.alert("Close Your eyes for 5sec!.","Warning",timeout=1000)
        print('The current pointer position is {0}'.format(pg.position()))
        _,_,AR=self.collect()
        self.xmin/=2
        self.xmax/=2
        self.ymin/=2
        self.ymax/=2
        self.EAR/=4
        self.EAR=(self.EAR+AR)/2
        self.intensity/=4
        #Checking whether the calibration is successfuol or not
        if self.xmax-self.xmin>50 and self.ymax-self.ymin>20:
            try:
                calt = open("cal.txt", "w")
                cald=open("calt.txt","w")
                cald.write("1")   
                calt.write('{} {} {} {} {} {}\n'.format(self.xmin, self.xmax,self.ymin,self.ymax,self.EAR,self.intensity))
                print(self.xmin,self.xmax,self.ymin,self.ymax,self.EAR)
            finally:
                calt.close()
                cald.close()
            self.master.destroy()
        else:
            #pymsgbox.alert("Calibration unsuccessful!Please try again!.","Warning",timeout=2000)
            self.xmin,self.xmax,self.ymin,self.ymax,self.EAR,self.intensity=0,0,0,0,0,0
            self.display(self.master)
    def __del__(self):
        print("calibration stopped")
    
if __name__=='__main__':
    
    root = tk.Tk()
    #e=EyeTracker(root)
    calb = Calib(root)
    calb.display(root)
    root.mainloop()

    
    
    
    
	
