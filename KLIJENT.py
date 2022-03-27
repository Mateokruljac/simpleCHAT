import threading
import socket
from better_profanity import profanity
# osnovna građa
HOST = "127.0.0.1"
PORT = 8005
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((HOST,PORT))
# klijent mora imati također opciju primanje poruka od drugih korisnika,
# ali isto tako i unos svoje poruke
#no prvo bira nadimak
nickname = input("Choose a nickname: ")

def receive():
    while True: # iz istog razloga kao i kod servera
      try:
         message = client.recv(1024).decode("utf-8")
         if message == "NICKNAME": #a prva će poruka sigurno biti nickname 
             client.send(bytes(nickname,"utf-8"))
         else:
              print(message)
      except:
          print("!!!!Error!!!!")
          client.close()
          break # gotova while loop i više se ništa ne događa
          
def write():
    #korsinik ispisuje poruku, ali prije poruke pisat će tko šalje
    while True:
      # user unosi poruku, no ako poruka sadrži psovku, server šalje poruku useru da bude pristojan
      write_message = input()
      censor_msg = profanity.censor(write_message,"*")
      if "*" in write_message:
          write_message = write_message.replace("*"," ")
      if "**" in censor_msg and "**" not in write_message:
         print("Please, do not use bad words! Be polite! Thank you!")  
      message = f"{nickname}: {censor_msg}"
      if write_message == "EXIT":
         print(f"{nickname} has left the chat!")
         client.close()
         break
      client.send(bytes(message,"utf-8"))
      
# thread -> isti razlog kao i kod servera 
# ne treba join je ne upravljamo mi direktno, nego puštamo slučaju
thread = threading.Thread(target=receive)
thread.start()
thread = threading.Thread(target=write)
thread.start()

