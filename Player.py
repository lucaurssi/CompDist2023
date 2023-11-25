# Comp Dist 2023
# Igor Lovatto Resende 10439099
# Luca Gomes Urssi, 10425396
#
# Jogo Distribuido

import socket
from threading import Thread

HOST = "" # leave empty, allows connections from any IP
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen() 
        
        conn, addr = s.accept()
        
        with conn: # connected to client
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                print(f"Received {data!r}")
                if not data:
                    break
                conn.sendall(data)


def client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while(True):
            message = input("message to send: ")
            if(message == "exit"):
                break
            s.sendall(message.encode('utf-8'))
            
            data = s.recv(1024)

choice = input(" 1. Host a game \n 2. Join a game \n 3. Exit \n")

match choice:
    case '1':
        ip_address = socket.gethostbyname(socket.gethostname())
        print(f"Server IP Address: {ip_address}")
        server_thread = Thread(target=server)
        server_thread.start()
        
    case '2':
        HOST = input("Enter the server IP: ")  # The server's hostname or IP address
        client_thread = Thread(target=client)
        client_thread.start()
     
    case '3':
         print("Closing game.")
         exit(0)
    case _:
        print("Invalid input, closing game.")
        exit(0)

print("thread created")






match choice:
    case '1':
        server_thread.join()
    case '2':
        client_thread.join()

print("thread closed")