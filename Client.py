import socket
import threading

#Getting nickname from user
nickname = input("Choose a nickname: ")

#Connecting client to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostname(), 1243))

#Receiving data from the server
def receive():
    while True:
        try:
            msg = client.recv(1024).decode("utf-8")
            if msg == "NICK:":
                client.send(nickname.encode("utf-8"))
            else:
                print(msg)
        except:
            print("Game Over")
            client.close()
            break
#Writing data to the server
def write():
    while True:
        msg = input()
        client.send(msg.encode("utf-8"))


#threading
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()


