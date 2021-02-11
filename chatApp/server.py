import socket
import tkinter as tk
from tkinter.constants import DISABLED, END
from message import Message
import pickle
import threading

# global entry, msgBox

def sendMessage(entry, msgBox):
    mess = Message(
        userName, entry.get()
    )
    
    msgBox.insert(
        END,
        "\n"+"%s says %s"%(mess.sender, mess.text)
    )

    entry.delete(0, END)
    
    c.send(
        pickle.dumps(mess, protocol=3)
    )


def receiveMessage():
    while True:
        receivedMessage = c.recv(512)
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


    send = tk.Button(window, text="Send", font=("Arial", 10), command=lambda: sendMessage(entry, msgBox))
    send.place(relx=0.8, rely=0.9, anchor=tk.CENTER)

    msgBox = tk.Text(window, width=35, height=10, state=DISABLED)#, text="Hello World")
    msgBox.place(relx = 0.5, rely= 0.5, anchor="center")

    window.mainloop()

if __name__ == "__main__":

    userName = input("What is your username? ")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 5000
    s.bind(('', port))
    s.listen(1)
    c, addr = s.accept()

    threading.Thread(target=receiveMessage,).start()

    setupGUI()