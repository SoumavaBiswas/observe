#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 17:23:54 2020

@author: Soumava
"""

import cv2
import numpy as np
import dlib
import time
from scipy.spatial import distance as dist
from pynput.mouse import Button, Controller
import pyautogui as pg
import sys
import os

class EyeTracker:
    def __init__(self):
        pg.FAILSAFE=False
        self.mouse = Controller()
        #Initializing live video capture
        self.cap = cv2.VideoCapture(0)

        #Calculating screen height and width
        self.Sheight,self.Swidth=pg.size()

        self.rects=None
        self.point=(0,0,1,0,0)
        self.old_point=(0,0,1,0,0)
        self.landmarks=None
        print(self.Sheight,self.Swidth)
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

        #Reading the calibration values from file
        with open('cal.txt') as f: 
            self.cal_list=[word for line in f for word in line.split()]
            f.close()
    #Calculation midpoint of two points
    def midpoint(self,p1 ,p2):
        return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

    #brightness detector returns current brightness level of captured frame
    def brightnessDetector(self,gray):
    	blur=cv2.GaussianBlur(gray,(7,7),0)
    	avg=np.mean(blur,axis=(0,1))
    	return avg

    #returns eye aspect ratio to detect a blink 
    def eye_aspect_ratio(self,left,right,top,bottom):
        A = dist.euclidean(left,right)
        B= dist.euclidean(top, bottom)
        if B==0:
            B=1
        mar=A/B
        return mar
    
    #Detects nose,eye point in the given frame
    def eyeDetector(self,rect,gray):
        for eye in rect:
            landmarks = self.predictor(gray, eye)
            fx=((landmarks.part(28).x+landmarks.part(29).x+landmarks.part(30).x+landmarks.part(31).x+landmarks.part(34).x)/5)
            fy=((landmarks.part(28).y+landmarks.part(29).y+landmarks.part(30).y+landmarks.part(31).y+landmarks.part(34).y)/5)
            self.left_point = (landmarks.part(36).x, landmarks.part(36).y)
            self.right_point = (landmarks.part(39).x, landmarks.part(39).y)
            self.center_top = self.midpoint(landmarks.part(37), landmarks.part(38))
            self.center_bottom = self.midpoint(landmarks.part(41), landmarks.part(40))
            EAR=self.eye_aspect_ratio(self.left_point,self.right_point,self.center_top,self.center_bottom)
            print (EAR)
            try:
                x_mid =((landmarks.part(21).x+landmarks.part(22).x)/2)
                y_mid =((landmarks.part(21).y+landmarks.part(22).y)/2)
            except:
                return False
            else:
                return x_mid,y_mid,EAR,fx,fy
        
    def eyeTracking(self):
        _, frame = self.cap.read()
        frame=cv2.flip(frame,1)
        self.gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.rects = self.detector(self.gray_frame, 0)
        x,y,fx,fy=(0,0,0,0)
        self.intensity=self.brightnessDetector(self.gray_frame)

        #If current brightness level differes from the brightness level detected at the time of calibration displays an warning messege
        if abs(self.intensity-float(self.cal_list[5]))>60:
            pymsgbox.alert("Background light changed. Calibrate for better accuracy.","Warning",timeout=2000)

        #Detects eye,nose point,EAR
        self.point=self.eyeDetector(self.rects,self.gray_frame)
    
        #If point is detected and passes in fluctuation then cursor moves, otherwise remains at old position
        if(self.point): 
            xprev,yprev,ear,fxp,fyp=self.old_point
            xnew,ynew,ear,fx1,fy1=self.point  
            if(abs(xprev-xnew)>0.5 and abs(yprev-ynew)>0.37 and abs(fxp-fx1)>0.5 and abs(fyp-fy1)>0.37):
                if(abs(xprev-xnew)>abs(yprev-ynew) and abs(fxp-fx1)>abs(fyp-fy1)):
                    (x,y,EAR,fx,fy)=xnew,yprev,ear,fx1,fyp
                    self.old_point=xnew,yprev,ear,fx1,fyp
                elif(abs(fxp-fx1)<abs(fyp-fy1)):
                    (x,y,EAR,fx,fy)=xprev,ynew,ear,fxp,fy1
                    self.old_point=xprev,ynew,ear,fxp,fy1
                else:
                    (x,y,EAR,fx,fy)=self.old_point
            else:
                (x,y,EAR,fx,fy)=self.old_point
        else:
            (x,y,EAR,fx,fy)=self.old_point
        sx1=((fx-float(self.cal_list[0]))/(float(self.cal_list[1])-float(self.cal_list[0])))*self.Swidth
        sy1=((fy-float(self.cal_list[2]))/(float(self.cal_list[3])-float(self.cal_list[2])))*self.Sheight
        if(EAR>float(self.cal_list[4])):
            pg.click()
        else:
            self.mouse.position=(sx1,sy1)   
            #pg.move(sx1,sy1,0.8,pg.easeInOutQuad)
        #print(sx1,sy1,EAR)
        #cv2.circle(frame,(round(fx),round(fy)), 5, (0, 255, 0), -1)
        #cv2.waitKey()
        #cv2.imshow('Frame',frame)
        
    def stopTracking(self):
        os.remove("check.txt")
        self.cap.release()
        cv2.destroyAllWindows()
    def __del__(self):
        print("Eye Tracking stopped")
        
if __name__=='__main__':
    e=EyeTracker()
    while True:
        e.eyeTracking()
        key = cv2.waitKey(1)
        if key == 27:
            cv2.destroyAllWindows()
            break
    cap.release()
    cv2.destroyAllWindows()
        
            
