from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xml.etree.ElementTree as ET

xmlDatabase = "db.xml"

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/RPC2",)

def addNote(topic, text, timestamp):
    try: 
        tree = ET.parse(xmlDatabase)
        root = tree.getroot()
    except ET.ParseError as e:
        print(e)
        return("Failed to parse XML file.")
    
    topicElement = None

    # Try to find if topic already exists
    for tpc in root:
        if tpc.get("name") == topic:
            topicElement = tpc
            break

    # If topic doesn't exist, create new one
    if topicElement == None:
        topicElement = ET.SubElement(root, "topic", name=topic)

    note = ET.SubElement(topicElement, "note", timestamp=timestamp)

    textElement = ET.SubElement(note, "text")
    textElement.text = str(text)

    # ET.dump(note)

    tree.write(xmlDatabase)
    return "Note added succesfully."

def getNotes(topic):
    try: 
        tree = ET.parse(xmlDatabase)
        root = tree.getroot()
    except ET.ParseError as e:
        print(e)
        return("Failed to parse XML file.")
    notes = []

    # Search for matching topics
    for tpc in root.findall("topic"):
        if tpc.get("name") == topic:

            # Matching topic found, search for notes under the topic
            notes = []
            for note in tpc.findall("note"):
                textElement = note.find("text")
                if textElement != None and textElement.text != None:
                    notes.append(textElement.text.strip())
            if notes:
                return notes
            else:
                return ["No notes found under topic"]
    return ["No such topic"]

def createDatabase():
    root = ET.Element("data")
    tree = ET.ElementTree(root)
    tree.write(xmlDatabase)

def server():
    with SimpleXMLRPCServer(("localhost", 8080), requestHandler=RequestHandler) as server:
        createDatabase()
        server.register_function(addNote, "addNote")
        server.register_function(getNotes, "getNotes")

        print("Server running on port 8080")
        server.serve_forever()

if __name__ == "__main__":
    server()
