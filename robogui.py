import time
import socket
import _thread as thread
import threading
from tkinter import *
from tkinter import Tk, Canvas
from tkinter import messagebox
from robo1_3 import *
import sys
#enter the command export DISPLAY =:0 before running the gui via ssh

batteryPower = 1;
secondThread = None
threadFlag = threading.Event()
messageWaiting = ""
messageReady = threading.Event()
otherIp = ""
messageWaiting = []
messageReady = threading.Event()
messageReady.clear()

actionListInv = []
control = RoboControl()
control.recenterAll()
top = Tk()
top.geometry("800x410")
image1 = PhotoImage(file= "up.gif")#images for the arrow buttons
image2 = PhotoImage(file= "down.gif")
image3 = PhotoImage(file= "left.gif")
image4 = PhotoImage(file= "right.gif")
image5 = PhotoImage(file= "bodright.png")
image6 = PhotoImage(file= "bodleft.png")
image7 = PhotoImage(file= "moveFwd.png")
image8 = PhotoImage(file= "movBkwd.png")
image9 = PhotoImage(file= "turnLeft.png")
image10 = PhotoImage(file= "turnRight.png")
image11 = PhotoImage(file="words.png")
can=Canvas(top, width=800, height= 410)
timer = Spinbox(top, from_ = 0, to =10)
timer.place(x=625,y=75)
can.pack()

import time

class Sender:
    HOST = ""
    PORT = 0

    def __init__(self, ipAd="192.168.1.109", port=8181):
        self.HOST = ipAd
        self.PORT = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Attempting connection to", self.HOST, self.PORT)
        self.sock.connect((self.HOST, self.PORT))
        print("Socket Connected")

    def sendMessage(self, message, lastMessage):
        message = message + "\r\n"
        self.sock.send(message.encode('ascii'))
        print(message, "was sent to "+self.HOST)
        self.sock.close()
        if (not lastMessage):
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.HOST, self.PORT))
        
    def close(self):
        self.sock.close()
        
        
class Listener:
    def __init__(self, host='', port=8181):
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.host = host
        
    def setThread(self, mainThread):
        self.mainThread = mainThread
        
    def start(self):
        self.mySocket.bind((self.host,self.port))
        self.mySocket.listen(1024)

        while True:
            print("Awaiting next connection")
            clientsocket,addr = self.mySocket.accept()

            incoming = clientsocket.recv(1024).decode('ascii')
            self.handleMessage(incoming)
            
            clientsocket.close()
            
    def handleMessage(self, message):
        print("Handling message", message)
        if len(message) >0:
           message = message.strip()
           global messageWaiting 
           #TODO send information to mainThread here
           if (message[0] == 'I'):
               message = message.split(" ")
               messageWaiting = message
               messageReady.set()
               print("IP loaded, messageReady set")
               #message[1] is IP address
           elif (message == "start"):
               messarr= []
               messarr.append(message)
               messageWaiting = messarr
               messageReady.set()
               print("start loaded, messageReady set")
               #message[1] is IP address
           elif (message == "home"):
               messarr= []
               messarr.append(message)
               messageWaiting = messarr
               messageReady.set()
               print("home loaded, messageReady set")
               #message[1] is IP address
               
           elif (message[0] == 'M'): #instruction for movement
               message = message.split(" ")
               messageWaiting = message
               messageReady.set()
               print("Movement loaded, messageReady set")
               #message[1] is how many
               #message[2] is direction
               
           elif (message[0] == 'H'): #Instruction for head
               message = message.split(" ")
               messageWaiting = message
               messageReady.set()
               print("Head loaded, messageReady set")
               #message[1] is how many
               #message[2] is direction
               
           elif (message[0] == 'B'): #instruction for body
               message = message.split(" ")
               messageWaiting = message
               messageReady.set()
               #message[1] is direction
               print("Body loaded, messageReady set")
            

def setIP(message):
    global otherIp
    otherIp = message
    print("ip set to "+ otherIp)
    sendToAndroid("Speak: connection made")
    
def createListener():
    listener = Listener();
    listener.setThread(threading.main_thread())
    listener.start()
    

class action:
    actionName = ""
    myType = 0
    myLength = 0
    def __init__(self, actionType, in_time, in_actionName):
        self.myType = actionType
        self.myLength = in_time
        self.actionName = in_actionName

actionList = []

class GUI():
   pass

def runGif(event):
    try:
        secondThread = thread.start_new_thread(runProgram,())
    except:
        print ("Error: unable to start thread")
    gifFrames = [PhotoImage(file='animSmall2.gif', format = 'gif -index %i' %(i)) for i in range(60)]
    toplevel = Toplevel()
    newCan = Canvas(toplevel, width=320, height=300)
    newCan.pack()
    i=0
    while True:
        newCan.create_image(160,160,image=gifFrames[i])
        i+=1     
        if (i==60):
            i=0
        top.update()
        if (threadFlag.isSet()):
            break;
        time.sleep(0.1)
    print("Running over")
    toplevel.destroy()
    threadFlag.clear()
    for i in range(len(actionList)):
        backSpace2()
def runFromAndroid():
    try:
        secondThread = thread.start_new_thread(runProgram,())
    except:
        print ("Error: unable to start thread")
    gifFrames = [PhotoImage(file='animSmall2.gif', format = 'gif -index %i' %(i)) for i in range(60)]
    toplevel = Toplevel()
    newCan = Canvas(toplevel, width=320, height=300)
    newCan.pack()
    i=0
    while True:
        newCan.create_image(160,160,image=gifFrames[i])
        i+=1     
        if (i==60):
            i=0
        top.update()
        if (threadFlag.isSet()):
            break;
        time.sleep(0.1)
    print("Running over")
    toplevel.destroy()
    threadFlag.clear()
    for i in range(len(actionList)):
        backSpace2()     
def runBackwards():
    try:
        secondThread = thread.start_new_thread(runProgram,())
    except:
        print ("Error: unable to start thread")
    gifFrames = [PhotoImage(file='animSmall2.gif', format = 'gif -index %i' %(i)) for i in range(60)]
    toplevel = Toplevel()
    newCan = Canvas(toplevel, width=320, height=300)
    newCan.pack()
    i=0
    while True:
        newCan.create_image(160,160,image=gifFrames[i])
        i+=1     
        if (i==60):
            i=0
        top.update()
        if (threadFlag.isSet()):
            break;
        time.sleep(0.1)
    print("Running over")
    toplevel.destroy()
    threadFlag.clear()
    for i in range(len(actionList)):
        backSpace2()

def addHeadUp(event):
    newAction = action(0,int(timer.get()),"head_up")
    if (len(actionList) < 8):
        actionList.append(newAction)
        newIcon = can.create_image(len(actionList)*75 + 25, 275, image = image1)
        my_label = Label(top, text=str(newAction.myLength),font=("Courier",8))
        my_label.place(x=len(actionList)*75 + 20,y=285)
        top.update()

def addHeadDown(event):
    newAction = action(0,int(timer.get()),"head_down")
    if (len(actionList) < 8):
        actionList.append(newAction)
        newIcon = can.create_image(len(actionList)*75 + 25, 275, image = image2)
        my_label = Label(top, text=str(newAction.myLength),font=("Courier",8))
        my_label.place(x=len(actionList)*75 + 20,y=285)
        top.update()

def addHeadLeft(event):
    newAction = action(0,int(timer.get()),"head_left")
    if (len(actionList) < 8):
        actionList.append(newAction)
        newIcon = can.create_image(len(actionList)*75 + 25, 275, image = image3)
        my_label = Label(top, text=str(newAction.myLength),font=("Courier",8))
        my_label.place(x=len(actionList)*75 + 20,y=285)
        top.update()

def addHeadRight(event):
    newAction = action(0,int(timer.get()),"head_right")
    if (len(actionList) < 8):
        actionList.append(newAction)
        newIcon = can.create_image(len(actionList)*75 + 25, 275, image = image4)
        my_label = Label(top, text=str(newAction.myLength),font=("Courier",8))
        my_label.place(x=len(actionList)*75 + 20,y=285)
        top.update()

def addBodyLeft(event):
    newAction = action(0,int(timer.get()),"body_left")
    if (len(actionList) < 8):
        actionList.append(newAction)
        newIcon = can.create_image(len(actionList)*75 + 25, 275, image = image6)
        my_label = Label(top, text=str(newAction.myLength),font=("Courier",8))
        my_label.place(x=len(actionList)*75 + 20,y=285)
        top.update()

def addBodyRight(event):
    newAction = action(0,int(timer.get()),"body_right")
    if (len(actionList) < 8):
        actionList.append(newAction)
        newIcon = can.create_image(len(actionList)*75 + 25, 275, image = image5)
        my_label = Label(top, text=str(newAction.myLength),font=("Courier",8))
        my_label.place(x=len(actionList)*75 + 20,y=285)
        top.update()

def addMoveForward(event):
    newAction = action(1,int(timer.get()),"move_fwd")
    if (len(actionList) < 8):
        actionList.append(newAction)
        newIcon = can.create_image(len(actionList)*75 + 25, 275, image = image7)
        my_label = Label(top, text=str(newAction.myLength),font=("Courier",8))
        my_label.place(x=len(actionList)*75 + 20,y=285)
        top.update()

def addMoveBackward(event):
    newAction = action(1,int(timer.get()),"move_bck")
    if (len(actionList) < 8):
        actionList.append(newAction)
        newIcon = can.create_image(len(actionList)*75 + 25, 275, image = image8)
        my_label = Label(top, text=str(newAction.myLength),font=("Courier",8))
        my_label.place(x=len(actionList)*75 + 20,y=285)
        top.update()

def addTurnRight(event):
    newAction = action(2,int(timer.get()),"turn_right")
    if (len(actionList) < 8):
        actionList.append(newAction)
        newIcon = can.create_image(len(actionList)*75 + 25, 275, image = image10)
        my_label = Label(top, text=str(newAction.myLength),font=("Courier",8))
        my_label.place(x=len(actionList)*75 + 20,y=285)
        top.update()

def addTurnLeft(event):
    newAction = action(2,int(timer.get()),"turn_left")
    if (len(actionList) < 8):
        actionList.append(newAction)
        newIcon = can.create_image(len(actionList)*75 + 25, 275, image = image9)
        my_label = Label(top, text=str(newAction.myLength),font=("Courier",8))
        my_label.place(x=len(actionList)*75 + 20,y=285)
        top.update()
      
def backSpace(event):
    global actionList
    if len(actionList)>0:
        clearIcon = can.create_rectangle(len(actionList)*75,250,len(actionList)*75+50,300,fill='green')
        actionList=actionList[:len(actionList)-1]

def backSpace2():
    global actionList
    if len(actionList)>0:
        clearIcon = can.create_rectangle(len(actionList)*75,250,len(actionList)*75+50,300,fill='green')
        actionList=actionList[:len(actionList)-1]
def sayYes(event): #robot says yes
    newAction = action(2,2,"say_yes")
    if (len(actionList) < 8):
        actionList.append(newAction)
        newIcon = can.create_image(len(actionList)*75 + 25, 275, image = image11)
        my_label = Label(top, text=str(newAction.myLength),font=("Courier",8))
        my_label.place(x=len(actionList)*75 + 20,y=285)
        top.update()
      
def sayNo(event): #robot says no
    newAction = action(2,2,"say_no")
    if (len(actionList) < 8):
        actionList.append(newAction)
        newIcon = can.create_image(len(actionList)*75 + 25, 275, image = image11)
        my_label = Label(top, text=str(newAction.myLength),font=("Courier",8))
        my_label.place(x=len(actionList)*75 + 20,y=285)
        top.update()
def sayDab(event): #robot says dab on the haters
    newAction = action(2,2,"say_dab")
    if (len(actionList) < 8):
        actionList.append(newAction)
        newIcon = can.create_image(len(actionList)*75 + 25, 275, image = image11)
        my_label = Label(top, text=str(newAction.myLength),font=("Courier",8))
        my_label.place(x=len(actionList)*75 + 20,y=285)
        top.update()
def sayNothing(event): #robot says nothing here
    newAction = action(2,2,"say_nothing")
    if (len(actionList) < 8):
        actionList.append(newAction)
        newIcon = can.create_image(len(actionList)*75 + 25, 275, image = image11)
        my_label = Label(top, text=str(newAction.myLength),font=("Courier",8))
        my_label.place(x=len(actionList)*75 + 20,y=285)
        top.update()
def sayDone(event): #robot says I'm done
    newAction = action(2,2,"say_done")
    if (len(actionList) < 8):
        actionList.append(newAction)
        newIcon = can.create_image(len(actionList)*75 + 25, 275, image = image11)
        my_label = Label(top, text=str(newAction.myLength),font=("Courier",8))
        my_label.place(x=len(actionList)*75 + 20,y=285)
        top.update()
def sayWake(event): #robot says wake me up inside
    newAction = action(2,2,"say_wake")
    if (len(actionList) < 8):
        actionList.append(newAction)
        newIcon = can.create_image(len(actionList)*75 + 25, 275, image = image11)
        my_label = Label(top, text=str(newAction.myLength),font=("Courier",8))
        my_label.place(x=len(actionList)*75 + 20,y=285)
        top.update()
      
def sendToAndroid(message):
    print("sending to "+ otherIp)
    quickClient = Sender(ipAd = otherIp, port=8181)
    quickClient.sendMessage(message,True)
      
      
def runProgram():
    turnModifier = 0.15
    for action in actionList:
        actionListInv.insert(0, action)
        #print(action.actionName, "for", action.myLength)
        if (action.actionName == "head_up"):
            for i in range (action.myLength):
                control.lookDownOneStep()
        elif (action.actionName == "head_down"):
            for i in range (action.myLength):
                control.lookUpOneStep()
        elif (action.actionName == "head_right"):
            for i in range (action.myLength):
                control.lookRightOneStep()
        elif (action.actionName == "head_left"):
            for i in range (action.myLength):
                control.lookLeftOneStep()
        elif (action.actionName == "body_right"):
            for i in range (action.myLength):
                control.rotateRight()
        elif (action.actionName == "body_left"):
            for i in range (action.myLength):
                control.rotateLeft()

        elif (action.actionName == "move_fwd"):
            startTime = time.clock()
            control.accelerateOneStep()
            time.sleep(batteryPower * float(action.myLength))
            control.stop()
        elif (action.actionName == "move_bck"):
            startTime = time.clock()
            control.decelerateOneStep()
            time.sleep(batteryPower * float(action.myLength))
            control.stop()
        elif (action.actionName == "turn_right"):
            startTime = time.clock()
            control.startTurnRight()
            time.sleep(float(action.myLength) * turnModifier)
            control.endTurn()
        elif (action.actionName == "turn_left"):
            startTime = time.clock()
            control.startTurnLeft()
            time.sleep(float(action.myLength) * turnModifier)
            control.endTurn()
        elif (action.actionName == "say_yes"):
            sendToAndroid("Speak: yes")
        elif (action.actionName == "say_no"):
            sendToAndroid("Speak: no")
        elif (action.actionName == "say_dab"):
            sendToAndroid("Speak: dab")
        elif (action.actionName == "say_nothing"):
            sendToAndroid("Speak: nothing here")
        elif (action.actionName == "say_done"):
            sendToAndroid("Speak: done")
        elif (action.actionName == "say_wake"):
            sendToAndroid("Speak: wake")
        time.sleep(1)
    global threadFlag
    threadFlag.set()
    control.recenterAll()
    sendReadyAlt()
    
def returnHome():
    turnModifier = 0.15
    for action in actionListInv:
        if (action.actionName == "head_up"):
            for i in range (action.myLength):
                control.lookDownOneStep()
        elif (action.actionName == "head_down"):
            for i in range (action.myLength):
                control.lookUpOneStep()
        elif (action.actionName == "head_right"):
            for i in range (action.myLength):
                control.lookRightOneStep()
        elif (action.actionName == "head_left"):
            for i in range (action.myLength):
                control.lookLeftOneStep()
        elif (action.actionName == "body_right"):
            for i in range (action.myLength):
                control.rotateRight()
        elif (action.actionName == "body_left"):
            for i in range (action.myLength):
                control.rotateLeft()

        elif (action.actionName == "move_fwd"):
            startTime = time.clock()
            control.accelerateOneStep()
            time.sleep(batteryPower * float(action.myLength))
            control.stop()
        elif (action.actionName == "move_bck"):
            startTime = time.clock()
            control.decelerateOneStep()
            time.sleep(batteryPower * float(action.myLength))
            control.stop()
        elif (action.actionName == "turn_right"):
            startTime = time.clock()
            control.startTurnRight()
            time.sleep(float(action.myLength) * turnModifier)
            control.endTurn()
        elif (action.actionName == "turn_left"):
            startTime = time.clock()
            control.startTurnLeft()
            time.sleep(float(action.myLength) * turnModifier)
            control.endTurn()
        elif (action.actionName == "say_yes"):
            sendToAndroid("Speak: yes")
        elif (action.actionName == "say_no"):
            sendToAndroid("Speak: no")
        elif (action.actionName == "say_dab"):
            sendToAndroid("Speak: dab")
        elif (action.actionName == "say_nothing"):
            sendToAndroid("Speak: nothing here")
        elif (action.actionName == "say_done"):
            sendToAndroid("Speak: done")
        elif (action.actionName == "say_wake"):
            sendToAndroid("Speak: wake")
        time.sleep(1)
    global threadFlag
    threadFlag.set()
    control.recenterAll()
   
def addMoveForwardNum(moves):
    newAction = action(1,moves,"move_fwd")
    if (len(actionList) < 8):
        actionList.append(newAction)
        newIcon = can.create_image(len(actionList)*75 + 25, 275, image = image7)
        my_label = Label(top, text=str(newAction.myLength),font=("Courier",8))
        my_label.place(x=len(actionList)*75 + 20,y=285)
        top.update()

def addMoveBackwardNum(moves):
    newAction = action(1,moves,"move_bck")
    if (len(actionList) < 8):
        actionList.append(newAction)
        newIcon = can.create_image(len(actionList)*75 + 25, 275, image = image8)
        my_label = Label(top, text=str(newAction.myLength),font=("Courier",8))
        my_label.place(x=len(actionList)*75 + 20,y=285)
        top.update()

def addTurnRightNum(moves):
    newAction = action(2,moves,"turn_right")
    if (len(actionList) < 8):
        actionList.append(newAction)
        newIcon = can.create_image(len(actionList)*75 + 25, 275, image = image10)
        my_label = Label(top, text=str(newAction.myLength),font=("Courier",8))
        my_label.place(x=len(actionList)*75 + 20,y=285)
        top.update()

def addTurnLeftNum(moves):
    newAction = action(2,moves,"turn_left")
    if (len(actionList) < 8):
        actionList.append(newAction)
        newIcon = can.create_image(len(actionList)*75 + 25, 275, image = image9)
        my_label = Label(top, text=str(newAction.myLength),font=("Courier",8))
        my_label.place(x=len(actionList)*75 + 20,y=285)
        top.update()
   
   
def addHeadUpNum(moves):
    newAction = action(0,moves,"head_up")
    if (len(actionList) < 8):
        actionList.append(newAction)
        newIcon = can.create_image(len(actionList)*75 + 25, 275, image = image1)
        my_label = Label(top, text=str(newAction.myLength),font=("Courier",8))
        my_label.place(x=len(actionList)*75 + 20,y=285)
        top.update()

def addHeadDownNum(moves):
    newAction = action(0,moves,"head_down")
    if (len(actionList) < 8):
        actionList.append(newAction)
        newIcon = can.create_image(len(actionList)*75 + 25, 275, image = image2)
        my_label = Label(top, text=str(newAction.myLength),font=("Courier",8))
        my_label.place(x=len(actionList)*75 + 20,y=285)
        top.update()

def addHeadLeftNum(moves):
    newAction = action(0,moves,"head_left")
    if (len(actionList) < 8):
        actionList.append(newAction)
        newIcon = can.create_image(len(actionList)*75 + 25, 275, image = image3)
        my_label = Label(top, text=str(newAction.myLength),font=("Courier",8))
        my_label.place(x=len(actionList)*75 + 20,y=285)
        top.update()

def addHeadRightNum(moves):
    newAction = action(0,moves,"head_right")
    if (len(actionList) < 8):
        actionList.append(newAction)
        newIcon = can.create_image(len(actionList)*75 + 25, 275, image = image4)
        my_label = Label(top, text=str(newAction.myLength),font=("Courier",8))
        my_label.place(x=len(actionList)*75 + 20,y=285)
        top.update()

def addBodyLeftNum():
    newAction = action(0,1,"body_left")
    if (len(actionList) < 8):
        actionList.append(newAction)
        newIcon = can.create_image(len(actionList)*75 + 25, 275, image = image6)
        my_label = Label(top, text=str(newAction.myLength),font=("Courier",8))
        my_label.place(x=len(actionList)*75 + 20,y=285)
        top.update()

def addBodyRightNum():
    newAction = action(0,1,"body_right")
    if (len(actionList) < 8):
        actionList.append(newAction)
        newIcon = can.create_image(len(actionList)*75 + 25, 275, image = image5)
        my_label = Label(top, text=str(newAction.myLength),font=("Courier",8))
        my_label.place(x=len(actionList)*75 + 20,y=285)
        top.update()
   
def handleAndroidMessage(messageArray):
    print("handling message ", messageArray)
    
    if(messageArray[0] =="start"):
       print("receiving start")
       runFromAndroid()
    if (messageArray[0] == 'IP:'):
       setIP(messageArray[1])
    if (messageArray[0] == 'M:'):
        if (messageArray[2] == "forward"):
            addMoveForwardNum(int(messageArray[1]))
        elif (messageArray[2] == "back"):
            addMoveBackwardNum(int(messageArray[1]))
        elif (messageArray[2] == "left"):
            addTurnLeftNum(int(messageArray[1]))
        elif (messageArray[2] == "right"):
            addTurnRightNum(int(messageArray[1]))
    elif (messageArray[0] == 'H:'):
        if (messageArray[2] == "up"):
            addHeadUpNum(int(messageArray[1]))
        elif (messageArray[2] == "down"):
            addHeadDownNum(int(messageArray[1]))
        elif (messageArray[2] == "left"):
            addHeadLeftNum(int(messageArray[1]))
        elif (messageArray[2] == "right"):
            addHeadRightNum(int(messageArray[1]))
    elif (messageArray[0] == 'B:'):
        if (messageArray[1] == "left"):
            addBodyLeftNum()
        elif (messageArray[1] == "right"):
            addBodyRightNum()
    elif (messageArray[0] == "start"):
        runProgram()
    elif (messageArray[0] == "home"):
        returnHome()
def sendReady(event):
   print("sending ready")
   sendToAndroid("Ready")
def sendReadyAlt():
   sendToAndroid("Ready")
def __main__():
    try:
        thread.start_new_thread(createListener, ())
    except:
        print("Error starting threads")
    
    queueSize = 0
    up = Button(top, image=image1, width ="25",height="25") #the buttons for the head controls
    up.place(x = 75,y = 75)
    up.bind('<ButtonPress-1>', addHeadUp)
    up.bind('<ButtonRelease-1>')
    down = Button(top, image=image2,width ="25",height="25")
    down.place(x = 75,y = 125)
    down.bind('<ButtonPress-1>', addHeadDown)
    down.bind('<ButtonRelease-1>')
    left = Button(top, image=image3,width ="25",height="25")
    left.place(x = 25,y = 125)
    left.bind('<ButtonPress-1>', addHeadLeft)
    left.bind('<ButtonRelease-1>')
    right = Button(top, image=image4,width ="25",height="25")
    right.place(x = 125,y = 125)
    right.bind('<ButtonPress-1>', addHeadRight)
    right.bind('<ButtonRelease-1>')
    headLab = Label(top, text = "Head controls",font=("Courier", 15))
    headLab.place(x = 20,y=15);

    leftBod = Button(top, image=image6,width ="47",height="29") #button controls for the body
    leftBod.place(x = 225,y = 75)
    leftBod.bind('<ButtonPress-1>', addBodyLeft)
    leftBod.bind('<ButtonRelease-1>')
    rightBod = Button(top, image=image5,width ="47",height="29")
    rightBod.place(x = 300,y = 75)
    rightBod.bind('<ButtonPress-1>', addBodyRight)
    rightBod.bind('<ButtonRelease-1>')
    bodLab = Label(top, text = "body controls",font=("Courier", 15))
    bodLab.place(x = 220,y=15);

    fwd = Button(top, image=image7, width ="25",height="25") #the buttons for the wheel controls
    fwd.place(x = 475,y = 75)
    fwd.bind('<ButtonPress-1>', addMoveForward)
    fwd.bind('<ButtonRelease-1>')
    bkwd = Button(top, image=image8,width ="25",height="25")
    bkwd.place(x = 475,y = 125)
    bkwd.bind('<ButtonPress-1>', addMoveBackward)
    bkwd.bind('<ButtonRelease-1>')
    turnleft = Button(top, image=image9,width ="25",height="25")
    turnleft.place(x = 425,y = 125)
    turnleft.bind('<ButtonPress-1>', addTurnLeft)
    turnleft.bind('<ButtonRelease-1>')
    turnright = Button(top, image=image10,width ="25",height="25")
    turnright.place(x = 525,y = 125)
    turnright.bind('<ButtonPress-1>', addTurnRight)
    turnright.bind('<ButtonRelease-1>')
    wheelLab = Label(top, text = "Wheel controls",font=("Courier", 15))
    wheelLab.place(x = 420,y=15);

    timerLab = Label(top, text = "Feet/90 deg/Steps",font=("Courier", 12))
    timerLab.place(x=625,y=15)

   
    startbut = Button(top, text ="START") #the buttons for the wheel controls
    startbut.place( x=375,y=360)
    startbut.bind('<ButtonPress-1>', runGif)
    startbut.bind('<ButtonRelease-1>')

    readybut = Button(top, text ="READY") 
    readybut.place( x=250,y=360)
    readybut.bind('<ButtonPress-1>', sendReady)
    readybut.bind('<ButtonRelease-1>')
   
    backbut = Button(top, text='BACKSPACE')
    backbut.place(x=675,y=250)
    backbut.bind('<ButtonPress-1>',backSpace)
    backbut.bind('<ButtonRelease-1>')

    talkLab = Label(top, text = "Say Something",font=("Courier", 15))
    talkLab.place(x = 625 ,y= 100);
    yesbut = Button(top, text = 'yes')
    yesbut.place(x= 625, y= 130)
    yesbut.bind('<ButtonPress-1>',sayYes)
    yesbut.bind('<ButtonRelease-1>')
    nobut = Button(top, text = 'no')
    nobut.place(x= 685, y= 130)
    nobut.bind('<ButtonPress-1>',sayNo)
    nobut.bind('<ButtonRelease-1>')

    dabbut = Button(top, text = 'dab')
    dabbut.place(x= 740, y= 130)
    dabbut.bind('<ButtonPress-1>',sayDab)
    dabbut.bind('<ButtonRelease-1>')

    nothingbut = Button(top, text = 'nothing here')
    nothingbut.place(x= 625, y= 170)
    nothingbut.bind('<ButtonPress-1>',sayNothing)
    nothingbut.bind('<ButtonRelease-1>')

    donebut = Button(top, text = 'done')
    donebut.place(x= 740, y= 170)
    donebut.bind('<ButtonPress-1>',sayDone)
    donebut.bind('<ButtonRelease-1>')

    wakebut = Button(top, text = 'wake me up inside')
    wakebut.place(x= 650, y=210 )
    wakebut.bind('<ButtonPress-1>',sayWake)
    wakebut.bind('<ButtonRelease-1>')

    q1 = can.create_rectangle(75,250,125,300,fill='green')
    q2 = can.create_rectangle(150,250,200,300,fill='green')
    q3 = can.create_rectangle(225,250,275,300,fill='green')
    q4 = can.create_rectangle(300,250,350,300,fill='green')
    q5 = can.create_rectangle(375,250,425,300,fill='green')
    q6 = can.create_rectangle(450,250,500,300,fill='green')
    q7 = can.create_rectangle(525,250,575,300,fill='green')
    q8 = can.create_rectangle(600,250,650,300,fill='green')
 
    while True:
        if (messageReady.isSet()):
            print(messageWaiting, "pulled from event")
            handleAndroidMessage(messageWaiting)
            
            messageReady.clear()
        time.sleep(0.01)
        top.update()
    #top.mainloop()
   
__main__()
