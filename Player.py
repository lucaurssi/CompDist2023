# Comp Dist 2023
# Igor Lovatto Resende 10439099
# Luca Gomes Urssi, 10425396

# Jogo Distribuido - Server

import socket

HOST = "" # leave empty, allows connections from any IP
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

ip_address = socket.gethostbyname(socket.gethostname())
#print(f"Server IP Address: {ip_address}")

choice = input(" 1. Host a game \n 2. Join a game \n 3. Exit \n")


match choice:
    case '1':
        print(f"Server IP Address: {ip_address}")
        input("Press Enter to initiate Server.")
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen() 
            
            conn, addr = s.accept()
            
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)
     
    case '2':
        HOST = input("Enter the server IP: ")  # The server's hostname or IP address

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(b"Hello, world")
            data = s.recv(1024)

        print(f"Received {data!r}")
     
    case '3':
         print("Closing game.")
    case _:
        print("Invalid input, closing game.")


