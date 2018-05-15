import time
import socket
import _thread as thread
import threading


otherIp = ""
messageWaiting = []
messageReady = threading.Event()
messageReady.clear()

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
        print(message, "was sent to android")
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
        print("Handling message")
        message = message.strip()
        global messageWaiting 
        #TODO send information to mainThread here
        if (message[0] == 'I'):
            message = message.split(" ")
            messageWaiting = message
            messageReady.set()
            print("IP loaded, messageReady set")
            #message[1] is IP address
            
        elif (message[0] == 'M'): #instruction for movement
            message = message.split(" ")
            messageWaiting = message
            messageReady.set()
            print("IP loaded, messageReady set")
            #message[1] is how many
            #message[2] is direction
            
        elif (message[0] == 'H'): #Instruction for head
            message = message.split(" ")
            messageWaiting = message
            messageReady.set()
            print("IP loaded, messageReady set")
            #message[1] is how many
            #message[2] is direction
            
        elif (message[0] == 'B'): #instruction for body
            message = message.split(" ")
            messageWaiting = message
            messageReady.set()
            print("IP loaded, messageReady set")
            #message[1] is direction
            

def setIP(message):
    otherIP = message
    print ("Set IP Address for android")

def setIP(newIp):
   otherIP = newIp
   
def createListener():
    listener = Listener();
    listener.setThread(threading.main_thread())
    listener.start()
    
def createSender():
    sender = Sender(ipAd = otherIP, port=8181)

def sendMessages():
    sender.sendMessage("First Message", False)
    time.sleep(5)

    sender.sendMessage("Second Message", True)

try:
    thread.start_new_thread(createListener, ())
except:
    print("Error starting threads")
    
while True:
    if (messageReady.isSet()):
        print(messageWaiting, "pulled from event")
        messageReady.clear()
    time.sleep(0.01)
    
    
    
import socket
