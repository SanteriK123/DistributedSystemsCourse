import xmlrpc.client
import datetime

def main():
    proxy = xmlrpc.client.ServerProxy("http://localhost:8080")

    while True:
        print("1.) Add a note")
        print("2.) Get notes from a topic")
        print("All other inputs will exit program")

        choice = input("Enter choice: ")
        if choice == "1":

            # Get topic, text and timestamp and send it over to server 
            topicAndText = input("Give topic and text in format topic+text: ")
            topic = topicAndText.split("+")[0]
            text = topicAndText.split("+")[1]
            timestamp = datetime.datetime.now().strftime("%m/%d/%Y - %H:%M:%S")
            response = proxy.addNote(topic, text, timestamp)
            print(response)
        elif choice == "2":

            topic = input("Give a topic: ")
            response = proxy.getNotes(topic)
            print(response)
        else:
            break

if __name__ == "__main__":
    main()