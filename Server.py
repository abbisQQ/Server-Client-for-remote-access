import socket, argparse

def server():
    host = "127.0.0.1"
    port = 5000
    
    mySocket = socket.socket()
    mySocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    mySocket.bind((host,port))

    mySocket.listen(1)

    conn,addr = mySocket.accept()


    print('Connection from: {}'.format(addr))

    sending_message = "welcome"

    while sending_message!= 'quit':
        if sending_message=="help":
            helpFunction()
            sending_message="welcome"
        else:    
            conn.send(sending_message.encode())
            received_message = conn.recv(4096).decode()
            print(received_message)
            sending_message = input("say something boss: ")
       
    conn.close()





def helpFunction():
    print("Welcome to Server-Client program made by C.Theodorou in April 2017.")
    print("This is the help function made to help you in order to remote any machine in you local network. \n\n")
    print("Command: getcwd  Usage: Prints the current working directory.\n")
    print("Command: chdir  Usage: Changes the working directory. Example: chdir /home/somefile/someotherfile.\n")
    print("Command: listdir  Usage: List of all files and folders inside the working directory. Example: listdir .\n")
    print("Command: shutdown  Usage: Shut down or Restart the computer in 1 min. Example: shutdown -s or shutdown -r .\n")
    print("Command: removedirs  Usage: Removes the whole directory. Example: removedirs /home/somefolder/someotherfolder.\n")
    print("Command: remove Usage: Removes a file. Example: remove somefile.txt\n")
    print("Command: makedirs Usage: Make new directories note that the path starts from your current working directory. Example: makedirs /makeafolder/andanotherinside .\n")
    print("Command: create Usage: Creates a new file. Example create newfile.txt\n")
    print("Command: read Usage: Read a file. Example read newfile.txt\n")
    print("Command: write Usage: Write text to a given file !note that you must choose the file and then send the data. Example: write myfile.txt send it and then write the text you want written.\n")
    print("Command: browser Usage: Opens a given URL using the browser. Example: broswer www.youtube.com\n")
    print("Command: kill_browser Usage: closes the browser you previous create with browser command.\n")
    
    
if __name__ == "__main__":
    server()
