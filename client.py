import socket
import threading

def receive(sock):
    while True:
        try:    
            data = sock.recv(1024).decode()
            print(data)
        except KeyboardInterrupt:
            return

def send(sock, user_name):
    while True:
        try:
            msg = input()
            sock.sendall(f"{user_name}: {msg}".encode())
        except KeyboardInterrupt:
            return

def client():
    try:
        print("Please Enter a User Name")
        user_name = input()
        c_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c_sock.connect(("", 50007))
    
        receiving = threading.Thread(target=receive, args=(c_sock,))
        sending = threading.Thread(target=send, args=(c_sock, user_name))
    
        receiving.start()
        sending.start()
    
        receiving.join()
        sending.join()
    except KeyboardInterrupt:
        c_sock.close()

client()
