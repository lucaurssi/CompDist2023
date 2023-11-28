# Comp Dist 2023
# Igor Lovatto Resende 10439099
# Luca Gomes Urssi, 10425396
#
# Jogo Distribuido

import socket
from threading import Thread
import os

# clears the terminal screen
def clear(): os.system('cls' if os.name=='nt' else 'clear')


def connection(s, conn, addr):# connection to client
    global in_lobby
    
    with conn: # while inside this, mantain the connection with the client 
        
        # if a user try to connect after the lobby is closed
        if not in_lobby: 
            return
        
        # setting nickname for the user
        nick = conn.recv(1024)
        nick = nick.decode('ascii')
        print(f"Connected by {addr} as {nick}")
        
        # confirmation
        data = (f"Hello there {nick}!")
        conn.sendall(data.encode('utf-8'))
        
        # main loop for the connection
        while True:
            data = conn.recv(1024) # waits for user input, TO DO: settimeout()
            if not data:
                break
            
            # logging messages in server
            print(f"Received: '{data.decode('ascii')}' from user: {nick}")
            
            # checking for command 'play', TO DO: move this to master  
            if in_lobby and data.decode('ascii') == "play" :
                in_lobby = False
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
                    s2.connect((socket.gethostbyname(socket.gethostname()), PORT))
                    
            
            # TO DO
            # send message from here to master if necessary for the game
            
            
            conn.sendall(data) # confirmation that the message was received
        
        # here the connection has closed
        print(f"User {nick} Disconnected. {addr}")




def client():
    nick = input("Your nickname: ")
    global HOST
    HOST = input("Enter the server IP: ")  # The server's hostname or IP address
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        try:
            s.settimeout(1)
            s.connect((HOST, PORT))
            s.sendall(nick.encode('utf-8'))
            data = s.recv(1024)
        except:
            print("Connection to server failed")
            return
        
        while(True):
            message = input("message to send: ")
            if(message == "exit"):
                break
            s.sendall(message.encode('utf-8'))
            
            data = s.recv(1024)


HOST = "" # leave empty on server, allows connections from any IP
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
connections = [] # server side threads that mantain connection to clients

in_lobby = True

clear()
choice = input(" 1. Host a game \n 2. Join a game \n 3. Exit \n")
clear()

match choice:
    case '1':
        print("<Server>\n")
        print(f"Server IP Address: {socket.gethostbyname(socket.gethostname())}")
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            
            # this loop keep accepting new connections to users
            while in_lobby:
                s.listen() 
                conn, addr = s.accept()
                connections.append(Thread(target=connection, args=(s, conn, addr)))
                connections[-1].start()
            
            # a player used the 'play' command a left the loop
            print("Game started")
            
            
            # TO DO: insert game's server side stuff here
            
            
            # wait for all connections to end, TO DO: force end connections after certain time, timeout ?
            for i in connections:
                i.join()
        
        print("All players disconnected")
    
    case '2':
        print("<Client>\n")
        
        client_thread = Thread(target=client)
        client_thread.start()
        
        
        # TO DO: insert game here
        
        
        client_thread.join()
    
    case '3':
         print("Closing game.")
         exit(0)
    case _:
        print("Invalid input, closing game.")
        exit(0)


# inportant print to check if any thread is loose,
# the program wont end if it is, but it will show the print bellow
print("End of program")