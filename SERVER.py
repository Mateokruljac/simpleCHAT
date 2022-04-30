import socket
import threading

HOST = "127.0.0.1" 
PORT = 8005 
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()
print("Server is listening...")

clients = []
nicknames = []

def broadcast (message):
    for client in clients:
        client.send(message)
def  handle (client):

    while True:
        try:
            message = client.recv(1024).decode("utf-8") 
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(index)
            client.close()
            nickname = nicknames.index[index]
            broadcast(f"{nickname} has left the chat!")
           
            nicknames.remove(nickname)
def receive ():
    
    while True:
      
        client, address = server.accept()
        print(f"Connection with address: {address}")
        client.send("NICKNAME".encode("ascii"))
        nickname = client.recv(1024).decode("utf-8")
        nicknames.append(nickname)
        clients.append(client)
        print(f"[NICKNAME] client: {nickname}")
        broadcast(f"{nickname} join to chat!".encode("ascii"))
        
        client.send(b"Connection to the server!\n")
        client.send("If you want to exit a chat type EXIT".encode("ascii"))
      
       
        thread = threading.Thread(target=handle,args=(client,))
        
        thread.start()

receive()
