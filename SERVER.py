import socket
import threading

HOST = "127.0.0.1" 
PORT = 8005 server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()
print("Server is listening...")

clients = []
nicknames = []

def broadcast (message):
    for client in clients:
        client.send(message)
 handle (client):

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
        broadcast(f"{nickname} join to chat!".encode("ascii")) # prikaže se drugima
        
        # client.send....server nas obavještava da se klijent pridružio chatu
        client.send(b"Connection to the server!\n")
        client.send("If you want to exit a chat type EXIT".encode("ascii"))
      
        # odnosi se na svakog klijenta posebno, jer svaki klijent može nešto poslati, zato se piše jedan
        #iako je omogućeno sudjelovanje više korsnika radi se struktura za jednog jer svi klijenti kad se
        #priključe ulaze u While loop i po istoj shemi rade
        # stavljanjem thread(niti) upravo omogućavamo korisniku handle, tj da unese poruku 
        #koristeći niti ubrzavamo proces slanja i primanja između korisnika
        thread = threading.Thread(target=handle,args=(client,))
        # ne treba join()
        thread.start()
       
#zašto pozivamo samo receive
#ostalo je sadržano tu
receive()
