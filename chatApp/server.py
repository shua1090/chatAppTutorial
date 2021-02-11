import socket
import tkinter as tk
from tkinter.constants import DISABLED, END
from message import Message
import pickle
import threading
import sys

# global entry, msgBox

def sendMessage():
    mess = Message(
        userName, entry.get()
    )
    
    msgBox.insert(
        END,
        "\n"+"%s > %s"%(mess.sender, mess.text)
    )

    entry.delete(0, END)
    

    conn.send(
        pickle.dumps(mess, protocol=3)
    )


def receiveMessage():
    while True:
        receivedMessage = conn.recv(512)
        receivedMessage = pickle.loads(receivedMessage)
        msgBox.insert(
            END,
            "\n"+"%s says %s"%(receivedMessage.sender, receivedMessage.text)
        )

def setupGUI():
    window = tk.Tk()

    window.geometry("300x300")

    title = tk.Label(window, text="Chat Application", font=("Arial", 14, "bold"))
    title.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    global entry, msgBox

    entry = tk.Entry(window, width=30)
    entry.place(relx=0.4, rely=0.9, anchor=tk.CENTER)


    send = tk.Button(window, text="Send", font=("Arial", 10), command=sendMessage)
    send.place(relx=0.8, rely=0.9, anchor=tk.CENTER)

    msgBox = tk.Text(window, width=35, height=10, state=DISABLED)#, text="Hello World")
    msgBox.place(relx = 0.5, rely= 0.5, anchor="center")

    window.mainloop()

if __name__ == "__main__":

    userName = input("What is your username? ")

    assert len(sys.argv) != 1

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 5000
    if sys.argv[1] == "client":
        print("Running Client")
        sock.connect(('192.168.86.110', port))
        conn = sock
    else:
        print("Running Server")
        sock.bind(('', port))
        sock.listen(1)
        conn, addr = sock.accept()

    print(conn)

    t = threading.Thread(target=receiveMessage,)
    t.start()
    setupGUI()
    conn.close()
