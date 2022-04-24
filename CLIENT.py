import threading
import socket
from better_profanity import profanity

HOST = "127.0.0.1"
PORT = 8005
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((HOST,PORT))

nickname = input("Choose a nickname: ")

def receive():
    while True: 
      try:
         message = client.recv(1024).decode("utf-8")
         if message == "NICKNAME": 
             client.send(bytes(nickname,"utf-8"))
         else:
              print(message)
      except:
          print("!!!!Error!!!!")
          client.close()
          break 
          
def write():
   
    while True:
     
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

