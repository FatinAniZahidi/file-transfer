import os
import sys
import threading
import socket
import tqdm
import time

def animation(msg):
        for char in msg:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(0.1)

class Server:
    start = 'Welcome To Secure File Transfer\n'
    animation(start)
    print('\t___________________________________________\n')
    S1 = '\tServer\n'
    animation(S1)

    #create socket (TCP Protocol)
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.Terima_connections()
    
    
    def Terima_connections(self):
        ip = str(input('\tPlease Enter Server Ip Address : '))
        port = int(input('\tPleaase Enter Desired Port Number : '))

        self.sock.bind((ip,port))  #associate the socket with specific ip address and port number
        self.sock.listen(100)  #server listen for incoming connection
        print('\n')

        while 1:
            c, addr = self.sock.accept()   #accept connection rqest from the  client
            print('-------------------------------------')
            print('\tSuccessfully Connected to :' + addr[0])  #print client ip address
            print('-------------------------------------')

            #create thread
            threading.Thread(target=self.handle_client,args=(c,addr,)).start()
            
    def handle_client(self,c,addr):
        New = c.recv(1024)  #receive input user from client
        if New.decode() == "y":   #if new user
            with open("login.txt", "a+") as register:
                username = c.recv(1024).decode()
                password = c.recv(1024).decode()
                
                #save new username & password into login.txt file
                register.seek(0)
                register.write(username)
                register.write(":")

                register.write(password)
                register.write('\n')

                #
                c.send("continue".encode())

            #receive username & password new registered user 
            with open("login.txt", "r") as login:
                username = c.recv(1024).decode()
                password = c.recv(1024).decode()

                #check either the login info exist in login.txt or not
                jumpa = "tak jumpa";
                for line in login:
                    creds = line.strip()
                    if creds.split(":")[0] in username and creds.split(":")[1] in password:
                        jumpa = "tak jumpa";

                if jumpa == "jumpa":
                    c.send(("\tWelcome New User : %s" % (username)).encode())
                else:
                    c.send("Not-a-user".encode())
                    #c.close()

        else:   #if not a new user
            with open("login.txt", "r") as login:
                username = c.recv(1024).decode()
                password = c.recv(1024).decode()

                jumpa = "tak jumpa";
                for line in login:
                    creds = line.strip()
                    if creds.split(":")[0] in username and creds.split(":")[1] in password:
                        jumpa = "jumpa";

                if jumpa == "jumpa":
                    c.send(("\tWelcome back: %s" % (username)).encode())
                else:
                    c.send("Not-a-user".encode())
                    #c.close()

        while 1:
            #server received file name from server
            data = c.recv(1024).decode()

            if not os.path.exists(data):
                c.send("Sorry Your File Does Not Exist In The Server!!".encode())
                continue
            else:
                c.send("File Exist".encode())
                print('\tSending...',data)

                #server send file to the client
                if data != '':
                    file = open(data,'rb')
                    data = file.read(1024)
                    #//encrypted_data = f.encrypt(data)
                    while data:
                        c.send(data)
                        data = file.read(1024)
                continue

server = Server()
