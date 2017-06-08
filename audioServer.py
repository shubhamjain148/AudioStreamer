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
z = 0
stream = None
clients = []
conns = []
class clientJob(threading.Thread):
 
    def __init__(self,conn):
        threading.Thread.__init__(self)
 
        self.shutdown_flag = threading.Event()
        self.changeFlag = threading.Event()
        self.conn = conn
 
    def run(self):
        global conns
        print "Starting new client thread"
        conn = self.conn
        wf2 = wave.open('closer2.wav','rb')
        wf2.setpos(k)
        data = wf2.readframes(CHUNK)
        while not self.changeFlag.is_set() and not self.shutdown_flag.is_set() and data:
            try:
                conn.sendall(data)
                data = wf2.readframes(CHUNK)
            except:
                conns.remove(conn)
                print "Client exited"
                conn.close()
                return
        if self.shutdown_flag.is_set():
            print "sending server exited"
            conn.sendall("Server exited")
        elif self.changeFlag.is_set():
            conn.sendall("Song changed on server")
            self.changeFlag.clear()
            print "returning from client"
            return
        else:
            conn.sendall("Song ended on server")             
        conn.close()  

class serverJob(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.shutdown_flag = threading.Event()
        self.changeFlag = threading.Event()
 
    def run(self):
        global k
        global name
        print "Starting new server thread"
        k = 0
        p = pyaudio.PyAudio()
        wf = wave.open(name,'rb')
        stream = p.open(format =
                p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True,
                frames_per_buffer=CHUNK)
        data = wf.readframes(CHUNK)
        k = wf.tell()

        while not self.changeFlag.is_set() and not self.shutdown_flag.is_set() and data:
            stream.write(data)
            data = wf.readframes(CHUNK)
            k = wf.tell()

        stream.stop_stream()
        stream.close()
        p.terminate() 
        if self.shutdown_flag.is_set():
            print "Server Closed"
        elif self.changeFlag.is_set():
            print "Changing Song"
            self.changeFlag.clear()
            return
        else:
            print "song end in server"

while True:
    try: 
        clients = []
        server = serverJob()
        server.start()
        time.sleep(2)
        for conn in conns:
            client = clientJob(conn)
            client.start()
            clients.append(client)
        while True:
            conn, addr = s.accept()
            conns.append(conn)
            print 'Connected by', addr
            client = clientJob(conn)
            client.start()
            clients.append(client)
    except KeyboardInterrupt:
            # server.shutdown_flag.set()
            # for client in clients:
            #     client.shutdown_flag.set()
            #     client.join()
            # server.join()
            print "Changing"
            server.changeFlag.set()
            for client in clients:
                client.changeFlag.set()
            server.join()
            for client in clients:
                client.join()
            time.sleep(2)
        



print("*closed")