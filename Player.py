# Comp Dist 2023
# Igor Lovatto Resende 10439099
# Luca Gomes Urssi, 10425396
#
# Jogo Distribuido

import socket
from threading import Thread
import os

def clear(): os.system('cls' if os.name=='nt' else 'clear')


def connection(s, conn, addr):# connected to client
    global in_lobby
    
    with conn: 
            if not in_lobby: 
                return
            
            
            nick = conn.recv(1024)
            nick = nick.decode('ascii')
            print(f"Connected by {addr} as {nick}")
            
            data = ("Hello there !")
            conn.sendall(data.encode('utf-8'))
            
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Received: '{data.decode('ascii')}' from user: {nick}")
                
                if in_lobby and data.decode('ascii') == "play" :
                    in_lobby = False
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
                        s2.connect((socket.gethostbyname(socket.gethostname()), PORT))
                        
                conn.sendall(data)
            print(f"User {nick} Disconnected. {addr}")


def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        
        while in_lobby:
            s.listen() 
            conn, addr = s.accept()
            connections.append(Thread(target=connection, args=(s, conn, addr)))
            connections[-1].start()
        
        print("Game started")
        
        for i in connections:
            i.join()
        
        print("All players disconnected")


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
connections = []
in_lobby = True

clear()
choice = input(" 1. Host a game \n 2. Join a game \n 3. Exit \n")
clear()

match choice:
    case '1':
        print("<Server>\n")
        ip_address = socket.gethostbyname(socket.gethostname())
        print(f"Server IP Address: {ip_address}")
        server_thread = Thread(target=server)
        server_thread.start()
        
    case '2':
        print("<Client>\n")
        client_thread = Thread(target=client)
        client_thread.start()
        
        # insert game here
     
    case '3':
         print("Closing game.")
         exit(0)
    case _:
        print("Invalid input, closing game.")
        exit(0)


match choice:
    case '1':
        server_thread.join()
    case '2':
        client_thread.join()

print("End of program")