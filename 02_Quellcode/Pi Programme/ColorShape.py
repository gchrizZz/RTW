#import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
#sfrom matplotlib import pyplot as plt
import time
import cv2
import numpy as np
import cv2.cv as cv


#initialize the camera and graba reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640,480))


# define range of blue color in HSV
lower_blue = cv.Scalar(100,60,60)
upper_blue = cv.Scalar(135,255,255)

#define range of green in HSV
lower_green = cv.Scalar(65,50,50)#[45,50,50])
upper_green = cv.Scalar(85,255,255)#[75,255,255]

#define range of red in HSV
lower_red = cv.Scalar(0,50,50)
upper_red = cv.Scalar(10,255,255)

#import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
#define range of red in HSV
lower_purple = cv.Scalar(140,50,50)#160,50,225
upper_purple = cv.Scalar(169,255,255)#180,255,255

lb =[0,0,0]
ub = [0,0,0]
#allow camera to warmup
time.sleep(2)

colour = "blue"

#user interface 
print "give the  name colour to recocnize (blue, green, red, purple or other)"
colour = raw_input()
while colour != "blue" and colour != "green" and colour != "red" and colour != "purple" colour != "other":
    print "colour slot 1: give a colour to recocnize (blue, green, red, purple or other)"
    colour = raw_input()
    
if colour != "other":
    print "whant to add bounds for colour? (y/n)"
    calibrate = raw_input()
    while calibrate != "y" and calibrate != "n":
        print "whant to add bounds for colour? (y/n)"
        calibrate = raw_input()
   
if calibrate == "y" or colour == "other":

    print "LOWER BOUND:"
    hmin = raw_input('  H: ')
    smin = raw_input('  S: ')
    vmin = raw_input('  V: ')
    print "UPPER BOUND:"
    hmax = raw_input('  H: ')
    smax = raw_input('  S: ')
    vmax = raw_input('  V: ')
    lower = cv.Scalar(float(hmin),float(smin),float(vmin))
    upper = cv.Scalar(float(hmax),float(smax),float(vmax))
else:
    if colour == "blue":
        lower = lower_blue
        upper = upper_blue
    elif colour == "red":
        lower = lower_red
        upper = upper_red
    elif colour == "green":
        lower = lower_green
        upper = upper_green
    else:
        lower = lower_purple
        upper = upper_purple

if colour == "other":
    colour = raw_input('Give colour name: ')
print lower
print upper
i=0
tri=[0,0,0,0,0]
cir=[0,0,0,0,0]
rec=[0,0,0,0,0]
obj = [0,0,0,0,0]

#capture frames from camera
for frame in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
        
        #grab the raw NumPy array representing the image, then initialize the timestamp
        #and occupied/unoccupied text
        image = frame.array
        #src = cv2.blur(image,(10,10))
        # Convert BGR to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        

        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower, upper)
        

        
        res = cv2.medianBlur(mask,5)
        res2 = res
   
        #contours
        contours, hierarchy = cv2.findContours(res2,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)    
     
        cntnum = 0
        tri[i] = 0
        rec[i] = 0
        cir[i] = 0
        obj[i] = 0
 
        #Approoximation
        for cnt in contours:
            #cut small noise areas
            area = cv2.contourArea(cnt) 
            if area > 3000: 
                #print area
                a = cv2.approxPolyDP(cnt,0.04*cv2.arcLength(cnt,True),True)
                cv2.drawContours(image, cnt, -1, (0,255,0), 3)
                cv2.drawContours(image, a, -1, (0,0,255), 5)
            
                cntnum = cntnum+1
            
                #find extreme points
                #l = a[a[:,:,0].argmin()][0]
                #r = a[a[:,:,0].argmax()][0]
                #t = a[a[:,:,1].argmin()][0]
                #b = a[a[:,:,1].argmax()][0]
            
                #find triangle (two of the extreme points are very close)
                #if (abs(l[0]-t[0]) < 30 and abs(l[1]-t[1]) < 30) or \
                #   (abs(l[0]-b[0]) < 30 and abs(l[1]-b[1]) < 30) or \
                #   (abs(r[0]-t[0]) < 30 and abs(r[1]-t[1]) < 30) or \
                #   (abs(r[0]-b[0]) < 30 and abs(r[1]-b[1]) < 30):
                       #print "TRIANGLE"
                if len(a) == 3:
                       tri[i] = tri[i] + 1
 
                #find circle (left and right are on the same height and top bottom are in themiddle)
                #elif (abs(l[1]-r[1]) < 60 and abs(t[0]-b[0]) < 60):
                elif len(a) == 4:
                    #print "CIRCLE"
                    rec[i] = rec[i] + 1  

                #find rectangle (extreme points are away from each other)
                else:
                    #print "RECTANGLE"
                    cir[i] = cir[i] + 1
    
        #fault tolerace (5MR + detection)
        obj[i] = cntnum
        i = i+1
        if i == 5:
            #detect error:
            total = max(set(tri),key = tri.count) +  max(set(cir),key = cir.count) + max(set(rec),key = rec.count)
            if (total == max(set(obj),key = obj.count)) :
                print "Detected " + str(max(set(obj),key = obj.count)) + " "+ colour +" objects:" 
                print "	   Triangles " + str(max(set(tri),key = tri.count))
                print "	   Circles " +  str(max(set(cir),key = cir.count))
                print "	   Rectangles " +  str(max(set(rec),key = rec.count))
            else:
                print "Error occured! Could not read clear image."
            i = 0

        #Print whatever must be printed
            cv2.imshow('frame',image)
        #cv2.imshow('mask',mask)
        #cv2.imshow('rs',res)
        #cv2.imshow('th',img)
       
        #if q ise pressed exit
        key = cv2.waitKey(10) & 0xFF
    
        #raw_input("press enter to continue..")
        #time.sleep(1)

        #clear the stream in preparation for the next frame
        rawCapture.truncate(0)

        #if the q is pressed break
        if key == ord("q"):
            break

cv2.destroyAllWindows()
