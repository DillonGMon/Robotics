import sys
import serial
import time
from sys import version_info
from Maestro import *

currentSpeed = 0

class RoboControl:
    x = Controller()
    #Motor and servo enumeration
    HEAD_VERTICAL_SERVO = 4
    HEAD_HORIZONTAL_SERVO = 3
    BODY_SERVO = 0
    ACCELL_MOTOR = 1
    TURN_MOTOR = 2

    #Centers, max, steps
    BODY_CENTER = 6000 #x.getMax(BODY_SERVO) - ((x.getMax(BODY_SERVO) - x.getMin(BODY_SERVO)) // 2)
    BODY_MAX = 7800 #x.getMax(BODY_SERVO)
    BODY_MIN = 4200 #x.getMin(BODY_SERVO)
    BODY_STEP = 600 #(x.getMax(BODY_SERVO) - BODY_CENTER // 2)
    HEAD_CENTER_HORIZONTAL = 6000 #x.getMax(HEAD_HORIZONTAL_SERVO) - ((x.getMax(HEAD_HORIZONTAL_SERVO) - x.getMin(HEAD_HORIZONTAL_SERVO)) // 2)
    HEAD_STEP_HORIZONTAL = 1000 #(x.getMax(HEAD_HORIZONTAL_SERVO) - HEAD_CENTER_HORIZONTAL) // 2
    HEAD_MAX_HORIZONTAL = 8000 #x.getMax(HEAD_HORIZONTAL_SERVO)
    HEAD_MIN_HORIZONTAL = 4000 #x.getMin(HEAD_HORIZONTAL_SERVO)
    HEAD_CENTER_VERTICAL = 6000 #x.getMax(HEAD_VERTICAL_SERVO) - ((x.getMax(HEAD_VERTICAL_SERVO) - x.getMin(HEAD_VERTICAL_SERVO)) // 2)
    HEAD_STEP_VERTICAL = 1000 #(HEAD_MAX_VERTICAL - HEAD_CENTER_VERTICAL) // 2
    HEAD_MAX_VERTICAL = 8000 #x.getMax(HEAD_VERTICAL_SERVO)
    HEAD_MIN_VERTICAL = 4000 #x.getMin(HEAD_VERTICAL_SERVO)

    #Motor speeds
    TURN_SPEED = 3000
    SPEED_STEP = 2000 #Resolution for speed. Max speed - Min Speed / 3 x.getMax(RIGHT_MOTOR) // 3
    MAX_FORWARD = 7000
    MAX_REVERSE = -7000

    #Variables
    bodyPosition = BODY_CENTER
    currentSpeed = 0
    headPositionH = HEAD_CENTER_HORIZONTAL
    headPositionV = HEAD_CENTER_VERTICAL
    
    def recenterAll(self):
        #print ("\n\n--------- RESET ALL ----------\n\n")
        self.x.setTarget(self.BODY_SERVO, self.BODY_CENTER)
        self.x.setTarget(self.HEAD_HORIZONTAL_SERVO, self.HEAD_CENTER_HORIZONTAL)
        self.x.setTarget(self.HEAD_VERTICAL_SERVO, self.HEAD_CENTER_VERTICAL)
    
    def __init__(self):
        self.x = Controller()

    #Motion functions          
    def stop(self):
        global currentSpeed
        #print ("Stopping moving")
        #stepDown = x.getPosition(LEFT_MOTOR) // 30
        if self.x.getPosition(self.ACCELL_MOTOR) >6000:
            for i in range(10):
                self.x.setTarget(self.ACCELL_MOTOR, 6800 - i*100)
            currentSpeed=0
        elif self.x.getPosition(self.ACCELL_MOTOR) <6000:
            for i in range(10):
                self.x.setTarget(self.ACCELL_MOTOR, 4900 + i*100)
            currentSpeed =0

    def decelerateOneStep(self):
        #print ("Decelerating")
        global currentSpeed
        if (currentSpeed==0):
            #print ("running loop")
            for i in range(5):
                self.x.setTarget(self.ACCELL_MOTOR,6500+i*100 )
                time.sleep(.1)
            currentSpeed=7000
        elif (currentSpeed ==7000):
            for i in range(5):
                self.x.setTarget(self.ACCELL_MOTOR,7000+i*100 )
                time.sleep(.1)
            currentSpeed=7500
        elif (currentSpeed ==7500):
            for i in range(5):
                self.x.setTarget(self.ACCELL_MOTOR,7500+i*100 )
                time.sleep(.1)
            currentSpeed=8000
        elif(currentSpeed<6000):
            stop()
            time.sleep(.5)
            for i in range(5):
                self.x.setTarget(self.ACCELL_MOTOR,6500+i*100 )
                time.sleep(.1)
            currentSpeed=7000               
            

    def accelerateOneStep(self):
        #print ("accelerating")
        global  currentSpeed
        if (currentSpeed==0):
            for i in range(5):
                self.x.setTarget(self.ACCELL_MOTOR,5000- i*100)
                time.sleep(.05)
            currentSpeed=5000
        elif (currentSpeed==5000):
            for i in range(5):
                self.x.setTarget(self.ACCELL_MOTOR,5000- i*100)
                time.sleep(.1)
            currentSpeed=4500
        elif (currentSpeed==4500):
            for i in range(5):
                self.x.setTarget(self.ACCELL_MOTOR,4500- i*100)
                time.sleep(.1)
            currentSpeed=4000
        elif (currentSpeed >6000):
            stop()
            time.sleep(.5)
            for i in range(5):
                self.x.setTarget(self.ACCELL_MOTOR,5500- i*100)
                time.sleep(.1)
            currentSpeed=5000
            
    def startTurnRight(self):
        #print ("Turning right")
        self.stop()
        for i in range(5):
            self.x.setTarget(self.TURN_MOTOR, 5000 - i*100)
            time.sleep(.1)  

    def startTurnLeft(self):
        #print ("Turning left")
        self.stop()
        for i in range(5):
            self.x.setTarget(self.TURN_MOTOR, 7500 - i*100)
            time.sleep(.1)  

    def endTurn(self):
        #print ("Stopping turning")
        for i in range(10):
            self.x.setTarget(self.TURN_MOTOR, 4900 + i*100)

    def lookAhead(self):
        #print ("centering head")
        self.x.setTarget(self.HEAD_HORIZONTAL_SERVO, self.HEAD_CENTER_HORIZONTAL)
        self.x.setTarget(self.HEAD_VERTICAL_SERVO, self.HEAD_CENTER_VERTICAL)
            
    def lookUpOneStep(self):
        #print ("looking up")
        if (self.x.getPosition(self.HEAD_VERTICAL_SERVO) > self.HEAD_MIN_VERTICAL):
            self.x.setTarget(self.HEAD_VERTICAL_SERVO, self.x.getPosition(self.HEAD_VERTICAL_SERVO)-self.HEAD_STEP_VERTICAL)
                    
    def lookDownOneStep(self):
        #print ("looking down")
        if (self.x.getPosition(self.HEAD_VERTICAL_SERVO) < self.HEAD_MAX_VERTICAL):
            self.x.setTarget(self.HEAD_VERTICAL_SERVO, self.x.getPosition(self.HEAD_VERTICAL_SERVO)+self.HEAD_STEP_VERTICAL)
                    
    def lookLeftOneStep(self):
        #print ("looking left")
        if  (self.x.getPosition(self.HEAD_HORIZONTAL_SERVO) < self.HEAD_MAX_HORIZONTAL):
            self.x.setTarget(self.HEAD_HORIZONTAL_SERVO, self.x.getPosition(self.HEAD_HORIZONTAL_SERVO)+self.HEAD_STEP_HORIZONTAL)
        
                    
    def lookRightOneStep(self):
        #print ("looking right")
        if (self.x.getPosition(self.HEAD_HORIZONTAL_SERVO) > self.HEAD_MIN_HORIZONTAL):
            self.x.setTarget(self.HEAD_HORIZONTAL_SERVO, self.x.getPosition(self.HEAD_HORIZONTAL_SERVO)-self.HEAD_STEP_HORIZONTAL)
                    
    def nodHead(self):
        #print ("yes")
        self.x.setTarget(self.HEAD_VERTICAL_SERVO, self.HEAD_MAX_VERTICAL)
        time.sleep(0.5)
        self.x.setTarget(self.HEAD_VERTICAL_SERVO, self.HEAD_MIN_VERTICAL)
        time.sleep(0.5)
        self.x.setTarget(self.HEAD_VERTICAL_SERVO, self.HEAD_MAX_VERTICAL)
        time.sleep(0.5)
        self.x.setTarget(self.HEAD_VERTICAL_SERVO, self.HEAD_MAX_VERTICAL)
        time.sleep(0.5)
        self.x.setTarget(self.HEAD_VERTICAL_SERVO, self.HEAD_CENTER_VERTICAL)
            
    def shakeHead(self):
        #print ("no")
        self.x.setTarget(self.HEAD_HORIZONTAL_SERVO, self.HEAD_MAX_HORIZONTAL)
        time.sleep(0.5)
        self.x.setTarget(self.HEAD_HORIZONTAL_SERVO, self.HEAD_MIN_HORIZONTAL)
        time.sleep(0.5)
        self.x.setTarget(self.HEAD_HORIZONTAL_SERVO, self.HEAD_MAX_HORIZONTAL)
        time.sleep(0.5)
        self.x.setTarget(self.HEAD_HORIZONTAL_SERVO, self.HEAD_MIN_HORIZONTAL)
        time.sleep(0.5)
        self.x.setTarget(self.HEAD_HORIZONTAL_SERVO, self.HEAD_CENTER_HORIZONTAL)
                    
    def rotateRight(self):
        self.x.setTarget(self.BODY_SERVO, self.BODY_MIN)
        #if (x.getPosition(BODY_SERVO) > BODY_MIN):
        #       x.setTarget(BODY_SERVO,x.getPosition(BODY_SERVO) + BODY_STEP)
        #       #print "turning right"
           
    def rotateLeft(self):
        self.x.setTarget(self.BODY_SERVO, self.BODY_MAX)
        #if (x.getPosition(BODY_SERVO) < BODY_MAX):
        #       x.setTarget(BODY_SERVO,x.getPosition(BODY_SERVO) + BODY_STEP)
        #       #print "turning left"
            
    def centerBody(self):
        self.x.setTarget(self.BODY_SERVO,self.BODY_CENTER)
        #print("centering")
            
    def quit():
        sys.exit("escape pressed")
            
            
    ###Input loop
    ##for event in dev.read_loop():
    ##        if event.code == 56 and event.value == 1:
    ##                recenterALL()
    ##        elif event.code == 57 and event.value == 1:
    ##                stop()
    ##        elif event.code == 106 and event.value == 1:
    ##                rotateRight()
    ##        elif event.code == 103 and event.value ==1:
    ##                centerBody()
    ##        elif event.code == 105 and event.value == 1:
    ##                rotateLeft()
    ##        elif event.code == 75 and event.value == 1:
    ##                lookLeftOneStep()
    ##        elif event.code == 76 and event.value == 1:
    ##                lookAhead()
    ##        elif event.code == 77 and event.value == 1:
    ##                lookRightOneStep()
    ##        elif event.code == 72 and event.value == 1:
    ##                lookDownOneStep()
    ##        elif event.code == 80 and event.value == 1:
    ##                lookUpOneStep()
    ##        elif event.code == 71 and event.value == 1:
    ##                nodHead()
    ##        elif event.code == 73 and event.value == 1:
    ##                shakeHead()
    ##        elif event.code == 17 and event.value == 1:
    ##                accelerateOneStep()
    ##        elif event.code == 31 and event.value == 1:
    ##                decelerateOneStep()
    ##        elif event.code == 30 and event.value == 1:
    ##                startTurnLeft()
    ##        elif event.code == 32 and event.value == 1:
    ##                startTurnRight()
    ##        elif event.code == 30 and event.value == 0 or event.code == 32 and event.value == 0:
    ##                endTurn()
    ##        elif event.code == 1 and event.value == 1:
    ##                quit()
                
