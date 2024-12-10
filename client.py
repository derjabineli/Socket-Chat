import socket
import threading
import sys

def receive(sock, active):
    sock.settimeout(1.0)
    try:
        while active.is_set():
            try:
                data = sock.recv(1024).decode()
                if data:
                    print(data)
            except socket.timeout:
                continue  
    except Exception as e:
        print(e)

def send(sock, user_name, active):
    try:
        while active.is_set():
            msg = input()
            sock.sendall(f"{user_name}: {msg}".encode())
    except Exception as e:
        print(e)

try:
    print("Please Enter a User Name")
    user_name = input()
    c_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c_sock.connect(("", 50007))
    
    active = threading.Event()
    active.set()
    receiving = threading.Thread(target=receive, args=(c_sock, active))
    sending = threading.Thread(target=send, args=(c_sock, user_name, active))
    
    receiving.daemon = True
    sending.daemon = True
    receiving.start()
    sending.start()
    receiving.join()
    sending.join()


except KeyboardInterrupt:
    c_sock.sendall(b'')
    active.clear()
finally:
    c_sock.close()

