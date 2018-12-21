import cv2
import cv2 as cv
import numpy as np
import pygame
import time
import serial

kernel = np.ones((5,5),np.uint8)

# Take input from webcam
cap = cv2.VideoCapture(0)

maxX = 320;
maxY = 240;

centerX = int(maxX/2);
centerY = int(maxY/2);

lastCode = 0
code = 0

# variable for keys pressed
left    = 0
right   = 0
up      = 0
down    = 0


# You will have to change this to the port where arduino is connected
port = "COM5"
# open serial port
ser = serial.Serial( port, 115200, timeout=0.1)

# Reduce the size of video to maxX x maxY so rpi can process faster
cap.set(3,maxX)
cap.set(4,maxY)

def nothing(x):
    pass
# Creating a windows for later use
cv2.namedWindow('HueComp')
cv2.namedWindow('SatComp')
cv2.namedWindow('ValComp')
cv2.namedWindow('closing')
cv2.namedWindow('tracking')


# My experimental values
hmn = 2
hmx = 26
smn = 124
smx = 255
vmn = 153
vmx = 255


while(1):

    buzz = 0
    _, frame = cap.read()

    #converting to HSV
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    hue,sat,val = cv2.split(hsv)
 
    # Apply thresholding
    hthresh = cv2.inRange(np.array(hue),np.array(hmn),np.array(hmx))
    sthresh = cv2.inRange(np.array(sat),np.array(smn),np.array(smx))
    vthresh = cv2.inRange(np.array(val),np.array(vmn),np.array(vmx))

    # AND h s and v
    tracking = cv2.bitwise_and(hthresh,cv2.bitwise_and(sthresh,vthresh))

    # Some morpholigical filtering
    dilation = cv2.dilate(tracking,kernel,iterations = 1)
    closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)
    closing = cv2.GaussianBlur(closing,(5,5),0)

    # Detect circles using HoughCircles
    circles = cv2.HoughCircles(closing,cv2.HOUGH_GRADIENT,2,120,param1=120,param2=50,minRadius=10,maxRadius=40)
        

    #Draw Circles
    if circles is not None:
        for i in circles[0,:]:
            print( len(i))
            print( len(circles))
            # If the ball is far, draw it in green
            if int(round(i[2])) < 30 and int(round(i[2])) > 10:
                cv2.circle(frame,(int(round(i[0])),int(round(i[1]))),int(round(i[2])),(0,255,0),5)
                cv2.circle(frame,(int(round(i[0])),int(round(i[1]))),2,(0,255,0),10)
                cv2.line(frame,(int(centerX),int(centerY)), (int(round(i[0])),int(round(i[1]))),(0,0,255),2)
                                
                if centerX < int(round(i[0])):
                    left = 1
                    right = 0
                   
                if centerX > int(round(i[0])):
                   right = 1
                   left = 0 
            # else draw it in red
            elif int(round(i[2])) > 35:
                cv2.circle(frame,(int(round(i[0])),int(round(i[1]))),int(round(i[2])),(0,0,255),5)
                cv2.circle(frame,(int(round(i[0])),int(round(i[1]))),2,(0,0,255),10)
      
    #Show the result in frames
    cv2.imshow('HueComp',hthresh)
    cv2.imshow('SatComp',sthresh)
    cv2.imshow('ValComp',vthresh)
    cv2.imshow('closing',closing)
    cv2.imshow('tracking',frame)

    code = chr ( 65 + 2**1*right + 2**0*left );
        
    # write to serial - if there is a change in the state of keys
    if ( lastCode != code ) :
        ser.write( code.encode() )
        lastCode = code
                        
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
ser.close()
cv2.destroyAllWindows()

#https://www.facebook.com/mrlunk
