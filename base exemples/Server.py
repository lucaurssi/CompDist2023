
# Comp Dist 2023
# Igor Lovatto Resende 10439099
# Luca Gomes Urssi, 10425396

# Jogo Distribuido - Server

import socket

HOST = "" # leave empty, allows connections from any IP
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

## getting the IP address using socket.gethostbyname() method
ip_address = socket.gethostbyname(socket.gethostname())
print(f"Server IP Address: {ip_address}")

input("Press enter to initiate the server.")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    
    s.listen() 
    
    # by running the command 'netstat -an' now, you can find a line with 0.0.0.0:PORT ,
    # where PORT is the number input above,
    # this shows that the server is listenning to that especific port for connections.
    
    conn, addr = s.accept()
    
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
            

# the server stopped listenning here
# end of "with" statement

