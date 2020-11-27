import os
import sys
import time
import socket
import pyaudio
from signal import signal, SIGINT
from sys import exit
import subprocess
import threading
from threading import Thread
def voice():
    if voice_tf == "n":
        exit()       
    class Client:
        def __init__(self):
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            while 1:
                try:
                    self.target_ip = vt
                    self.target_port = int(vtp)
                    self.s.connect((self.target_ip, self.target_port))
                    break
                except:
                    logo()
                    print("Oof! Couldn't connect to voice server. Try Again.")
                    time.sleep(5)
            chunk_size = 1024 # 512
            audio_format = pyaudio.paInt16
            channels = 1
            rate = 20000
            self.p = pyaudio.PyAudio()
            self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=chunk_size)
            self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)
            logo()
            print("Connected to voice Server! Say Something!")
            print("Please wait for IRC chat... Finishing up connection...")
            devnull = os.open(os.devnull, os.O_WRONLY)
            old_stderr = os.dup(2)
            sys.stderr.flush()
            os.dup2(devnull, 2)
            os.close(devnull)
            receive_thread = threading.Thread(target=self.receive_server_data).start()
            self.send_data_to_server()
        def receive_server_data(self):
            while True:
                try:
                    data = self.s.recv(1024)
                    self.playing_stream.write(data)
                except:
                    pass
        def send_data_to_server(self):
            while True:
                try:
                    data = self.recording_stream.read(1024)
                    self.s.sendall(data)
                except:
                    pass
    client = Client()
def handler(signal_received, frame):
    if os.name =="nt": 
        os.system("cls")
    else: 
        os.system("clear")
    print('SIGINT or CTRL-C detected. Exiting gracefully. Bye!')
    exit(0)
def load(): 
    load_str = "Connecting..."
    ls_len = len(load_str) 
    animation = "|/-\\"
    anicount = 0
    counttime = 0        
    i = 0                     
    while (counttime != 30): 
        time.sleep(0.075)  
        load_str_list = list(load_str)  
        x = ord(load_str_list[i]) 
        y = 0                             
        if x != 32 and x != 46:              
            if x>90: 
                y = x-32
            else: 
                y = x + 32
            load_str_list[i]= chr(y) 
        res =''              
        for j in range(ls_len): 
            res = res + load_str_list[j] 
        sys.stdout.write("\r"+res + animation[anicount]) 
        sys.stdout.flush() 
        load_str = res 
        anicount = (anicount + 1)% 4
        i =(i + 1)% ls_len 
        counttime = counttime + 1
    if os.name =="nt": 
        os.system("cls")
    else: 
        os.system("clear")
def logo():
    if os.name =="nt": 
	    os.system("cls")
    else: 
	    os.system("clear")
    print ('''
     __     _     ___ _           _   
  /\ \ \___| |_  / __\ |__   __ _| |_ 
 /  \/ / _ \ __|/ /  | '_ \ / _` | __|
/ /\  /  __/ |_/ /___| | | | (_| | |_ 
\_\ \/ \___|\__\____/|_| |_|\__,_|\__|
Netcat Chat Client - Created by X1pe0

''')
def chat():
    devnull = open(os.devnull,"w")
    retval = subprocess.call(["dpkg","-s","rlwrap"],stdout=devnull,stderr=subprocess.STDOUT)
    devnull.close()
    if retval != 0:
        logo()
        print ('')
        print ("Package rlwrap not installed.")
        while True:
            print ('Would you like me to install for you?')
            yn = raw_input('Y/N?> ')
            if yn == 'y':
                os.system('sudo apt-get -y install rlwrap')
                break
            elif yn == 'n':
                os.system('clear')
                logo()
                print ('')
                print ('rlwrap is needed. Please install to use this script.')
                time.sleep(5)
                os.system('clear')
                exit()
            else:
                print ('Unknown option.')
    logo()
    if chat_tf == "y":
        host = vt
        port = vtp
    else:
        host = chatip
        port = chatport    
    try:
        if voice_tf == "y":
            time.sleep(30)
        os.system('''rlwrap -S "> " nc %s %s'''%(host,int(port)))
    except:
        print ('Unknown value entered...')
        time.sleep(5)
        exit()
if __name__ == '__main__':
    signal(SIGINT, handler)
    logo()
    voice_tf = input("Would you like to connect with voice? (y/n): ")
    if voice_tf == "n":
        pass
    else:
        vt = input ("IP of voice server: ")
        vtp = input ("Port of voice server: ")
    logo()
    if voice_tf == "n":
        chat_tf = "n"
        chatip = input ("IRC IP: ")
        chatport = input ("IRC Port: ")
    else:
        chat_tf = input("Does IRC chat have the same IP/Port? (y/n): ")
        if chat_tf == "n":
            chatip = input ("IRC IP: ")
            chatport = input ("IRC Port: ")
    load() 
    Thread(target = chat).start()
    Thread(target = voice).start()
