# Comp Dist 2023
# Igor Lovatto Resende 10439099
# Luca Gomes Urssi, 10425396
#
# Jogo Distribuido

# TO DO: 
#   find out why the server is not closing
#   open the lobby again (so someone who lost connection can connect back)
#   cry
#   ...
#   profit

import os
import socket
from threading import Thread, Lock
from time import sleep

# clears the terminal screen
def clear(): os.system('cls' if os.name=='nt' else 'clear')


def connection(s, conn, IP):# connection to client
    global in_lobby
    global in_game
    global player_glossary
    global player_amount
    global lock
    global connected_players
    failed = False # local
    
    conn.settimeout(10)
    player_amount += 1
    player = []
    
    with conn: # while inside this, mantain the connection with the client 
        
        # if a user try to connect after the lobby is closed
        if not in_lobby: 
            player_amount -= 1
            return
        
        try:
            # setting nickname for the user
            nick = conn.recv(1024)
            nick = nick.decode('ascii')
            
            player = [nick, IP]
            if player in player_glossary:
                print(f"User {nick} reconnected. {IP}")
                data = (f"Welcome back {nick}!")
             
            else: 
                player_glossary.append(player)
                print(f"Connected by {IP} as {nick}")
                data = (f"Hello there {nick}!")
            
            # confirmation
            conn.sendall(data.encode('utf-8'))
        except:
            failed = True

        if not failed:
            connected_players.append(conn)
        
        # main loop for the connection
        while not failed:
            try:
                data = conn.recv(1024) # waits for user input
                
            except:
                failed = True
                continue
            
            if "ping" in data.decode('ascii'):
                continue
            
            if not data or data.decode('ascii') == "exit":
                break
            
            to_send = f"{nick}: {data.decode('ascii')}"
            
            # logging messages in server
            print(to_send)
            
            lock.acquire()
            message.append(to_send) # message will be taken care of by another thread
            lock.release()
            
            
            # checking for command 'play'
            if in_lobby and data.decode('ascii') == "play" :
                in_game = True
                in_lobby = False
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2: # breaks the master thread loop
                    s2.connect((socket.gethostbyname(socket.gethostname()), PORT))
                    
            
            if in_game and data.decode('ascii') == "lobby" :
                in_lobby = True
                in_game = False
            
        
        if conn in connected_players:
            connected_players.remove(conn)
        
        # here the connection has closed
        if nick:
            print(f"User {nick} Disconnected. {IP}")
        else:
            print(f"Invalid name used on: {IP}")
        
        player_amount -= 1
        
        
        # warn server to close, since there's no other player
        if player_amount < 1:
            in_lobby = False
            in_game = False
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
                    s2.connect((socket.gethostbyname(socket.gethostname()), PORT))


def server_messager():
    global message # "something"
    global connected_players # conn
    global lock
    
    while True:
        if not message:
            for i in connected_players:
                i.sendall(("pong").encode('utf-8'))
            sleep(1)
            continue
        
        lock.acquire()
        to_send = message[0]
        message.pop(0)
        lock.release()
        
        if to_send == "die, mailman":
            break
        
        for i in connected_players:
            i.sendall(to_send.encode('utf-8'))
        


def client():
    global HOST
    global message
    global in_lobby
    global failed
    
    nick = input("Your nickname: ")
    HOST = input("Enter the server IP: ")  # The server's hostname or IP address
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(10)
        
        try: # try to connect
            s.connect((HOST, PORT))
            s.sendall(nick.encode('utf-8')) # send nick
            data = s.recv(1024) # Receives back 'Hello there {nick}!'
            print(data.decode('ascii'))
        except:
            print("Connection to server failed")
            failed = True
            return
        
        
        in_lobby = True # connected
        
        while(True):
            if not message: # wait for message send/ ping pong / receive message
                try:
                    s.sendall(("ping").encode('utf-8'))
                    data = s.recv(1024) # feedback pong
                except:
                    print("Connection to server failed. Press 'Enter' to close.")
                    return
                
                if "pong" not in data.decode('ascii') and not (f"{nick}: " in data.decode('ascii')):
                    print(data.decode('ascii'))
                
                sleep(0.1)
                continue
            
            if message == "exit":
                break
            
            try:
                s.sendall(message.encode('utf-8')) # send message
                message = ""
                
                data = s.recv(1024) # feedback
            except:
                print("Connection to server failed. Press 'Enter' to close.")
                failed = True
                return


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
    



if __name__ == "__main__" :
    HOST = "" # leave empty on server, allows connections from any IP
    PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
    connections = [] # server side threads that mantain connection to clients
    message = ""
    lock = Lock()

    in_game = False
    in_lobby = True
    failed = False

    connected_players = []
    player_glossary = []
    player_amount = 0

    clear()
    choice = input(" 1. Host a game \n 2. Join a game \n 3. Exit \n")
    clear()

    if choice == '1':
        print("<Server>\n")
        print(f"Server IP Address: {get_ip()}")
    
        
        message = []
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            
            mailman = Thread(target=server_messager)
            mailman.start()
            
            while in_lobby or in_game:
            
                # this loop keep accepting new connections to users
                while in_lobby:
                    s.listen(1) 
                    conn, addr = s.accept()
                    connections.append(Thread(target=connection, args=(s, conn, addr[0])))
                    connections[-1].start()
                
                # a player used the 'play' command a left the loop
                
                if player_amount > 0:
                    print("Game started.")
                
                # this is where i would put my game, if i had one
                while in_game:
                    sleep(0.2)
                
                if player_amount > 0:
                    print("Game ended, returning to lobby.")
                
                
            
            
            
            # wait for all connections to end, TO DO: force end connections after certain time, timeout ?
            for i in connections:
                i.join()
            
            message.append("die, mailman")
            mailman.join
        
        print("All players disconnected")
    
    elif choice == '2':
        print("<Client>\n")
        
        client_thread = Thread(target=client)
        client_thread.start()
        
        in_lobby = False
        
        while(True):
            if failed: # thread failed to connect or lost connection
                break
            
            if not in_lobby:   # thread still getting name and IP
                sleep(0.1)
                continue
            
            if message: # wait a bit for the thread to deal with the message
                sleep(0.1)
            
            message = input() # message that the thread will read
            if message == "exit":
                break
        
        
        client_thread.join()
    
    elif choice == '3':
        print("Closing game.")
    else:
        print("Invalid input, closing game.")
    


    # inportant print to check if any thread is loose,
    # the program wont end if it is, but it will show the print bellow
    print("End of program")