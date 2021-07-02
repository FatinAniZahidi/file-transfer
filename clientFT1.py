import socket #import socket library
import os     #
import tqdm
import time
import sys
import getpass

def animation(msg):
        for char in msg:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(0.1)

class Client:
    start = '\t\tWelcome To Secure File Transfer\n'
    animation(start)
    print('-------------------------------------------------------------------')
    cl = '\tClient\n'
    animation(cl)
    
    #create socket (TCP Protocol)
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connect_to_server()
 
    #create a connection to the server
    def connect_to_server(self):
        self.target_ip = input(str('\tPlease Enter Ip Address : '))
        self.target_port = input('\tPlease Enter Port Number : ')

        #receive connection from server
        self.sock.connect((self.target_ip,int(self.target_port)))

        self.main()

    def main(self):
        #verify a new user
        New = input('\tAre you a new user?(y/n) :')
        self.sock.send(New.encode())   #send input user to server
        if New == 'y':   #if new user
            username = input('\tUsername :')
            self.sock.send(username.encode())

            password = getpass.getpass('\tPassword : ', stream=None)
            self.sock.send(password.encode())

            #register new user
            register = self.sock.recv(1024)

            if register.decode() == "continue":
                print('\t\t%Login Again%')

                #login new registered user
                username = input('\tUsername: ')
                self.sock.send(username.encode())

                password = getpass.getpass('\tPassword : ', stream=None)
                self.sock.send(password.encode())

                #if the username and password does not exist in the login.txt
                login = self.sock.recv(1024)
                if login.decode() == "Not-a-user":
                    print("\tNot a user. Connection will be terminate.")

                    self.sock.shutdown(socket.SHUT_RDWR)
                    self.sock.close()
                    sys.exit()
                else:
                    print(login.decode())  #print welcome new user

        else:   #if not a new user
            print('\t\t%Login%')
            username = input('\tUsername: ')
            self.sock.send(username.encode())

            password = getpass.getpass('\tPassword : ', stream=None)
            self.sock.send(password.encode())

            #if username and password does not exist in login.txt
            login = self.sock.recv(1024)
            if login.decode() == "Not-a-user":
                print("\tNot a user. Connection will be terminate.")

                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
                sys.exit()
            else:
                print(login.decode())  #print welcome back
		
        print("\t|Enter 'exit' To Terminate Connection.| ")
        while 1:
            #input requested file name 
            file_name = input('\tPlease Enter File Name On Server : ')
            if file_name == "exit":
                sys.exit()

            else:
                self.sock.send(file_name.encode())  #client send file name to server

            confirm = self.sock.recv(1024)
            if confirm.decode() == "File Doesn't Exist In The Server":
                exist = "\tFile Doesn't Exist At Server.\n"
                animation(exist)
                continue

            else:   #if file exist in the server
                write_name = file_name
                if os.path.exists(write_name): os.remove(write_name)

                #file download from the sever
                with open(write_name,'wb') as file:
                    while 1:
                        data = self.sock.recv(1024)

                        if not data:
                            break

                        file.write(data)
                        break

                success = '\tFile Successfully Downloaded.\n'
                animation(success)
                continue

client = Client()
