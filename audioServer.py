import socket
import pyaudio
import wave
import threading
import signal
import time

class TimeoutException(Exception):   # Custom exception class
    pass

def timeout_handler(signum, frame):   # Custom signal handler
    raise TimeoutException

#record
CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 100

HOST = 'localhost'    # The remote host
PORT = 50007              # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)


frames = []
k = None

name = "closer2.wav"
wf = wave.open(name,'rb')
z = 0
stream = None

class clientJob(threading.Thread):
 
    def __init__(self,conn):
        threading.Thread.__init__(self)
 
        # The shutdown_flag is a threading.Event object that
        # indicates whether the thread should be terminated.
        self.shutdown_flag = threading.Event()
        self.conn = conn
        # ... Other thread setup code here ...
 
    def run(self):
        conn = self.conn
        wf2 = wave.open('closer2.wav','rb')
        wf2.setpos(k)
        data = wf2.readframes(CHUNK)
        while not self.shutdown_flag.is_set() and data:
            try:
                conn.sendall(data)
                data = wf2.readframes(CHUNK)
            except:
                print "Client exited"
                conn.close()
                return
        if self.shutdown_flag.is_set():
            print "sending server exited"
            conn.sendall("Server exited")
        else:
            conn.sendall("Song ended on server")             
        conn.close()  

class serverJob(threading.Thread):
    def __init__(self, wf):
        threading.Thread.__init__(self)

        # The shutdown_flag is a threading.Event object that
        # indicates whether the thread should be terminated.
        self.shutdown_flag = threading.Event()
        self.wf = wf
        # ... Other thread setup code here ...
 
    def run(self):
        global k
        global name
        p = pyaudio.PyAudio()
        wf = self.wf
        stream = p.open(format =
                p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True,
                frames_per_buffer=CHUNK)
        data = wf.readframes(CHUNK)
        k = wf.tell()

        while not self.shutdown_flag.is_set() and data:
            stream.write(data)
            data = wf.readframes(CHUNK)
            k = wf.tell()

        stream.stop_stream()
        stream.close()
        p.terminate() 
        if self.shutdown_flag.is_set():
            print "Server Closed"
        else:
            print "song end in server"
clients = []
try: 
    server = serverJob(wf)
    server.start()
    while True:
        conn, addr = s.accept()
        print 'Connected by', addr
        client = clientJob(conn)
        client.start()
        clients.append(client)
except KeyboardInterrupt:
        server.shutdown_flag.set()
        for client in clients:
            client.shutdown_flag.set()
            client.join()
        server.join()
        



print("*closed")