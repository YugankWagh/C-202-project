from tkinter import *
import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

client.connect((ip_address, port))

class GUI:
    def __init__(self):
        self.window = Tk()
        self.window.withdraw()

        self.login = Toplevel()
        self.login.title("Login")
        self.login.resizable(False, False)
        self.login.configure(width=400, height=300)

        self.label = Label(self.login, text="Please login to continue", font=("Arial", 12))
        self.label.place(x=100, y=50)
        self.name_label = Label(self.login, text="Enter your nickname:", font=("Arial", 12))
        self.name_label.place(x=50, y=100)

        self.name_entry = Entry(self.login, width=20)
        self.name_entry.place(x=200, y=100)

        self.go = Button(self.login, text="Login", font=("Helvetica 14 bold", 12), command=lambda: self.goAhead(self.name_entry.get()))
        self.go.place(x=150, y=150)

        self.window.mainloop()

    def goAhead(self, name):
        self.login.destroy()
        self.name = name
        rcv = threading.Thread(target=self.receive)
        rcv.start()

    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if message == 'NICKNAME':
                    client.send(self.name.encode('utf-8'))
                else:
                    pass
            except:
                print("An error occurred!")
                client.close()
                break
    

gui = GUI()