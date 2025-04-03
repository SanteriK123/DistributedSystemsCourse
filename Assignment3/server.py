import socket
import threading

# Some premade channels in dictionary
channels = {"chat1": [], "chat2": [], "chat3": []}
clients = {}

def sendMessage(message, channel, sender=None):
    if channel in channels:
        for client in channels[channel]:
            if client != sender:
                try:
                    client.send(message.encode("utf-8"))
                except:
                    removeClient(client)

def handleClient(client):
    try:
        # Get nickname and add client to clients
        nickname = client.recv(1024).decode("utf-8")
        clients[client] = nickname
        print(f"{nickname} connected!")
        
        # Get channel name and either create it or join it
        channel = client.recv(1024).decode("utf-8")
        if channel not in channels:
            print(f"Creating a new channel {channel}")
            channels[channel] = []
        channels[channel].append(client)
        client.send(f"Succesfully joined channel {channel}".encode("utf-8"))

        sendMessage(f"{nickname} has joined the chat!", channel, client)

        # Main loop for messaging and switching channels
        while True: 
            message = client.recv(1024).decode("utf-8")
            if message.startswith("/join "):
                newChannel = message.split(" ", 1)[1]

                if newChannel != channel:
                    # Leave old channel
                    if client in channels[channel]:
                        channels[channel].remove(client)

                    # Join new channel
                    if newChannel not in channels:
                        channels[newChannel] = []
                    channels[newChannel].append(client)
                    channel = newChannel
                    sendMessage(f"{nickname} switched to {channel}.", channel)
                    print(f"{nickname} switched to {channel}.")
            elif message.startswith("/private"):
                prefix, recipient, privateMessage = message.split(" ", 2)
                handlePrivateMessage(client, recipient, privateMessage)
            elif message.startswith("/msg "):
                newMessage = message.split(" ", 1)[1]
                print(newMessage)
                sendMessage(f"{nickname}: {newMessage}", channel, client)
            elif message == "/exit":
                print(f"User {client} has left the chat")
                break
    except:
        print("An error occured.")
    finally:
        removeClient(client)
        client.close()

# Send private messages
def handlePrivateMessage(sender, recipientName, message):
    for client, nickname in clients.items():
        if nickname == recipientName:
            try:
                client.send(f"Private from {clients[sender]}: {message}".encode("utf-8"))
                return
            except:
                removeClient(client)
    sender.send("User not found.".encode("utf-8"))

# Remove a client from clients
def removeClient(client):
    for channel in channels:
        if client in channels[channel]:
            channels[channel].remove(client)
    if client in clients:
        del clients[client]
    return

def serverStart():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("localhost", 5050))
    server.listen()

    print("Server started, awaiting connections from clients")
    try:
        while True:
            connection, address = server.accept()
            thread = threading.Thread(target=handleClient, args=(connection,))
            thread.start()
    except KeyboardInterrupt:
        print("\nShutting down server.")
    finally:
        server.close()

if __name__ == "__main__":
    serverStart()