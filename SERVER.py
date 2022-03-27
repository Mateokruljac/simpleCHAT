import socket
import threading

HOST = "127.0.0.1" #localhost -> mogli smo ga napisati i direkt u bind, ali meni ovako ljepše izgleda
PORT = 8005 #ista stvar kao i host
                               #address family
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#tcp
server.bind((HOST,PORT))
server.listen()
print("Server is listening...")

# u ove prazne liste dodajemo klijente i njihove nadimke
clients = []
nicknames = []

#tko može poslati poruku i komu se emitira? svaki klijent koji je aktivan
def broadcast (message):
    for client in clients:
        client.send(message)
#print što se prikazuje na serveru a broadcast štp se emitira ostalim klijentima
def handle (client):
    #koliko klijent može unositi poruka? KOLIKO HOĆE!
    while True:
        try:
            #ako uspije unijeti, ostali je primaju,dekodiraju
            message = client.recv(1024).decode("utf-8") #  koliko je velika poruka?
            broadcast(message)
        except:# no što ako ipak nije tako? što raditi? moramo iznaciti klijenta?
            #Ali kako znati kojega izbaciti?
            index = clients.index(client)
            clients.remove(index)
            client.close()
            nickname = nicknames.index[index]
            broadcast(f"{nickname} has left the chat!")
            # zašto broadcast a ne print?
            # zato što drugim klijentima stigne također poruka da je ovaj napustio server
            nicknames.remove(nickname)
def receive ():
    #primiti poruku #koliko dugo...cijelo vrijeme dok se šalje
    while True:
        #server prihvaća klijente i njihovu addressu
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