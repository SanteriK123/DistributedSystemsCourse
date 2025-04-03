import socket
import threading

def receiveMessages(sock):
    while True:
        try:
            message = sock.recv(1024).decode("utf-8")
            if not message:
                break
            print(message)
        except:
            print("Disconnected from server.")
            sock.close()
            break

def startClient():
    # Create a socket that connects to the server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # ip = input("Give the server ip to connect to:")
    client.connect(("localhost", 5050))

    # Set nickname
    nickname = input("Enter your nickname: ")
    client.send(nickname.encode("utf-8"))

    # Ask channel to join
    channelName = input("Enter which channel you want to join: ")
    client.send(channelName.encode("utf-8"))

    # Start the thread
    threading.Thread(target=receiveMessages, args=(client,), daemon=True).start()

    print("Type directly to command line to send message to all people in channel")
    print("'/join *channel* -> Switches to channel or create if it doesnt exist'")
    print("'/private *user* *message*' -> Send private message to user")
    print("'/exit' -> Exit and disconnect from the chat")

    # Main loop for client to send messages to server
    while True:
        message = input(">")
        if message.startswith("/join "):
            client.send(message.encode("utf-8"))
        elif message.startswith("/private "):
            client.send(message.encode("utf-8"))
        elif message == "/exit":
            print("Disconnecting.")
            client.send("/exit".encode("utf-8"))
            break
        else:
            # Normal chat message
            client.send(message.encode("utf-8"))

    client.close()
if __name__ == "__main__":
    startClient()