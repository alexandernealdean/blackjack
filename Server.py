import socket
import threading
import random

#Opening server connection and defining variables
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostname(), 1243))

server.listen(5)
clients = []
nicknames = []
scores = []
readyArr = []
stayArr = []
highest = 0
roll = "s"

# Send message to all clients
def broadcast(message):
    for client in clients:
        client.send(message)

#Send message to all clients except for the one passed
def broadcastallbut(message, client):
    newclients = clients.copy()
    newclients.remove(client)
    for newclient in newclients:
        newclient.send(message)

#Send message only to the client passed
def broadcastonly(message, client):
    client.send(message)

# receive all connections
def receive():
    while True:
        try:
            client, address = server.accept()

            print("Connected with: " + str(address))

            client.send("NICK:".encode("utf-8"))
            nickname = client.recv(1024).decode("utf-8")
            nicknames.append(nickname)
            clients.append(client)
            scores.append(0)
            readyArr.append("n")
            stayArr.append("h")

            client.send(("Type r and press enter to ready!").encode("utf-8"))

            print("Nickname of client is: " + nickname)
            broadcastallbut((nickname + " joined! Waiting for them to ready...").encode("utf-8"), client)

            #threading
            ready_thread = threading.Thread(target=handleready, args=(client,))
            ready_thread.start()
        except:
            pass

# handle ready check inputs
def handleready(client):
    while True:
        try:
            response = client.recv(1024)
            if not response:
                clients.remove(client)
                nicknames.remove(clients.index(client))
                scores.remove(clients.index(client))
                readyArr.remove(clients.index(client))
                stayArr.remove(clients.index(client))

            if response.decode("utf-8") == "r" or response.decode("utf-8") == "n":
                readyArr[clients.index(client)] = response.decode("utf-8")

            if response.decode("utf-8") == "r":
                if "n" in readyArr:
                    broadcastonly(("You readied.").encode("utf-8"), client)
                    broadcastallbut((nicknames[clients.index(client)] + " readied. Please type r and press enter to ready").encode("utf-8"), client)
                else:
                    broadcast(("Everyone ready!").encode("utf-8"))
                    broadcast(("How to play: ").encode("utf-8"))
                    broadcast(("The goal of the game is to get as close as you can to 21 without going over.\nIf you go over you lose.").encode("utf-8"))
                    broadcast(("On your turn you may type h or s to perform an action.\nType h to roll 2 dice and add it to your total score or\nType s to stay if you don't want to roll anymore").encode("utf-8"))
                    broadcast(("\nOnce everyone has stayed whoever got the closest to 21 without going over will be the winner").encode("utf-8"))
                    broadcast(("\nTo begin take your turns one after another. Choose who goes first. \nType either h or s").encode("utf-8"))
                play_thread = threading.Thread(target=handleplay, args=(client,))
                play_thread.start()
                threading.current_thread().join()
        except:
            break


# determines if the handle play method runs
def readycheck(readyArr, readyresponse, client):
    if readyresponse.decode("utf-8") == "r" or readyresponse == "n":
        readyArr[clients.index(client)] = readyresponse.decode("utf-8")
    if "n" in readyArr:
        print("Not all players are ready. Please wait...")
    else:
        return True


# handle play inputs
def handleplay(client):
    while True:
        try:
            response = client.recv(1024)
            if response.decode("utf-8") == "r" or response.decode("utf-8") == "n":
                readyArr[clients.index(client)] = response.decode("utf-8")
            if "n" in readyArr:
                broadcast("Not all players are ready. Please wait...")
            else:
                #threading
                roll_thread = threading.Thread(target=play, args=(response.decode("utf-8"), nicknames[clients.index(client)]))
                roll_thread.start()
        except:
            broadcast(("SOMEONE FORCIBLY LEFT. PLEASE RESTART SERVER.").encode("utf-8"))
            break

#handle dice roll / determine winners
def play(roll, nickname):
    try:
        if roll == 'h':
            stayArr[nicknames.index(nickname)] = "h"
            d1 = random.randint(1, 6)
            d2 = random.randint(1, 6)
            total = d1 + d2
            scores[nicknames.index(nickname)] += total

            if scores[nicknames.index(nickname)] > 21:

                broadcast(("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n").encode("utf-8"))
                broadcastonly(("You HIT").encode("utf-8"), clients[nicknames.index(nickname)])
                broadcastallbut(("\n" + nickname + " HITS").encode("utf-8"), clients[nicknames.index(nickname)])
                broadcast(("\nThe total score is:\n").encode("utf-8"))

                for nick in nicknames:
                    broadcast((nick + ": " + str(scores[nicknames.index(nick)]) + "\n").encode("utf-8"))

                highest = 0
                for score in scores:
                    if score > highest and score <= 21:
                        highest = score
                # Print who won
                if highest > 0:
                    broadcast(("\nThe WINNER is: " + nicknames[scores.index(highest)] + "\n").encode("utf-8"))
                elif highest == 0 or highest > 21:
                    broadcast(("\nNOBODY WINS! YOU BUNCH OF LOSERS!\n").encode("utf-8"))

                broadcast(("\nNEW GAME!\n").encode("utf-8"))
                broadcast(("How to play: ").encode("utf-8"))
                broadcast(("The goal of the game is to get as close as you can to 21 without going over.\nIf you go over you lose.").encode("utf-8"))
                broadcast(("On your turn you may type h or s to perform an action.\nType h to roll 2 dice and add it to your total score or\nType s to stay if you don't want to roll anymore").encode("utf-8"))
                broadcast(("\nOnce everyone has stayed whoever got the closest to 21 without going over will be the winner").encode("utf-8"))
                broadcast(
                    (
                        "\nTo begin take your turns one after another. Choose who goes first. \nType either h or s").encode(
                        "utf-8"))

                for i in range(len(scores)):
                    scores[i] = 0

                return

            broadcast(("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n").encode("utf-8"))
            broadcastonly(("You HIT").encode("utf-8"), clients[nicknames.index(nickname)])
            broadcastallbut(("\n" + nickname + " HITS").encode("utf-8"), clients[nicknames.index(nickname)])
            broadcast(("\nThe total score is:\n").encode("utf-8"))

            for nick in nicknames:
                broadcast((nick + ": " + str(scores[nicknames.index(nick)]) + "\n").encode("utf-8"))

        elif roll == 's':
            stayArr[nicknames.index(nickname)] = "s"
            broadcast(("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n").encode("utf-8"))
            broadcastonly(("You STAY").encode("utf-8"), clients[nicknames.index(nickname)])
            broadcastallbut(("\n" + nickname + " STAYS").encode("utf-8"), clients[nicknames.index(nickname)])
            broadcast(("\nThe total score is:\n").encode("utf-8"))
            for nick in nicknames:
                broadcast((nick + ": " + str(scores[nicknames.index(nick)]) + "\n").encode("utf-8"))
            if "h" not in stayArr:
                # print scores again
                broadcast(("\n\n\n\n----Final Scores----\n").encode("utf-8"))
                for nick in nicknames:
                    broadcast((nick + ": " + str(scores[nicknames.index(nick)]) + "\n").encode("utf-8"))
                # Find the winner
                highest = 0
                for score in scores:
                    if score > highest and score <= 21:
                        highest = score

                # Print who won
                if highest >= 0:
                    broadcast(("\nThe WINNER is: " + nicknames[scores.index(highest)] + "\n").encode("utf-8"))
                elif highest == 0 or highest > 21:
                    broadcast(("\nNOBODY WINS! YOU BUNCH OF LOSERS!\n").encode("utf-8"))

                for i in range(len(scores)):
                    scores[i] = 0

                broadcast(("\nNEW GAME!\n").encode("utf-8"))
                broadcast(("How to play: ").encode("utf-8"))
                broadcast(("The goal of the game is to get as close as you can to 21 without going over.\nIf you go over you lose.").encode("utf-8"))
                broadcast(( "On your turn you may type h or s to perform an action.\nType h to roll 2 dice and add it to your total score or\nType s to stay if you don't want to roll anymore").encode("utf-8"))
                broadcast(("\nOnce everyone has stayed whoever got the closest to 21 without going over will be the winner").encode("utf-8"))
                broadcast(("\nTo begin take your turns one after another. Choose who goes first. \nType either h or s").encode("utf-8"))
    except:
        broadcast(("SOMEONE FORCIBLY LEFT. PLEASE RESTART SERVER.").encode("utf-8"))
        pass

print("Server is listening...")

#threading
rec_thread = threading.Thread(target=receive)
rec_thread.start()
