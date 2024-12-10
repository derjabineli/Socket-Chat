import sys
import socket
import selectors
import types

def accept_connection(sel, server, connections):
    conn, addr = server.accept()
    connections.append(conn)
    print(f"Accepted connection from {conn}")
    conn.setblocking(False)
    conn.sendall("Welcome to the server!".encode())
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def process_data(key, mask, sel, connections):
    sock = key.fileobj 
    data = key.data
    if mask & selectors.EVENT_READ:
        try:
            recv_data = sock.recv(1024)
            print(recv_data)
            if recv_data:
                data.outb += recv_data
            else:
                sel.unregister(sock)
                connections.remove(sock)
                sock.close()
        except:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            connections.remove(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            for connection in connections:
                if connection == sock:
                    continue
                else:
                    sent = connection.send(data.outb)
                    if sent == 0:
                        sel.unregister(connection)
                        connection.close()
                        connections.remove(connection)
            data.outb = b""

def main():
    sel = selectors.DefaultSelector()
    HOST = ''
    PORT = 50007
    connections = []

    s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_sock.bind((HOST, PORT))
    s_sock.listen()
    s_sock.setblocking(False)
    sel.register(s_sock, selectors.EVENT_READ, data=None)

    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_connection(sel, key.fileobj, connections)
                else:
                    process_data(key, mask, sel, connections)
    except KeyboardInterrupt:
        print("Chatroom is closing!")
    finally:
        s_sock.close()
main()
