import socket
import pyaudio
import wave
import threading
import signal
import time
import struct

class TimeoutException(Exception):   # Custom exception class
    pass

def timeout_handler(signum, frame):   # Custom signal handler
    raise TimeoutException

#record
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 100

multicast_group = ('224.0.0.251', 9999)

# Create the datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set a timeout so the socket does not block indefinitely when trying
# to receive data.
sock.settimeout(0.2)

# Set the time-to-live for messages to 1 so they do not go past the
# local network segment.
ttl = struct.pack('b', 10)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
frames = []
k = None

name = "closer2.wav"
z = 0
stream = None
clients = []
conns = []

p = pyaudio.PyAudio()
wf = wave.open(name,'rb')
stream = p.open(format =
        p.get_format_from_width(wf.getsampwidth()),
        channels = wf.getnchannels(),
        rate = wf.getframerate(),
        output = True,
        frames_per_buffer=CHUNK)

i = 0
while True:
    try:
        data = wf.readframes(CHUNK)
        while data:
            # print i
            i+=1
            print len(data)
            # print "^data"
            sent = sock.sendto(data, multicast_group)
            # print "sent" + str(sent)
            data2, address = sock.recvfrom(4096)
            
            # if data2 == data:
            #     print str(i) + " same"
            # else:
            #     print str(i) + "not same"
            time.sleep(0.01)
            # print address
            stream.write(data)
            data = wf.readframes(CHUNK)
        break
        # k = wf.tell()
    except Exception as e:
        print "Here in Exception"
        time.sleep(0.5)
        print e
    except OSError as o:
        print "here in OSError"
        print o


stream.stop_stream()
stream.close()
p.terminate() 

# class clientJob(threading.Thread):
 
#     def __init__(self,conn):
#         threading.Thread.__init__(self)
 
#         self.shutdown_flag = threading.Event()
#         self.changeFlag = threading.Event()
#         self.conn = conn
 
#     def run(self):
#         global conns
#         print "Starting new client thread"
#         conn = self.conn
#         wf2 = wave.open('closer2.wav','rb')
#         wf2.setpos(k)
#         data = wf2.readframes(CHUNK)
#         while not self.changeFlag.is_set() and not self.shutdown_flag.is_set() and data:
#             try:
#                 conn.sendall(data)
#                 data = wf2.readframes(CHUNK)
#             except:
#                 conns.remove(conn)
#                 print "Client exited"
#                 conn.close()
#                 return
#         if self.shutdown_flag.is_set():
#             print "sending server exited"
#             conn.sendall("Server exited")
#         elif self.changeFlag.is_set():
#             conn.sendall("Song changed on server")
#             self.changeFlag.clear()
#             print "returning from client"
#             return
#         else:
#             conn.sendall("Song ended on server")             
#         conn.close()  

# class serverJob(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)

#         self.shutdown_flag = threading.Event()
#         self.changeFlag = threading.Event()
 
#     def run(self):
#         global k
#         global name
#         print "Starting new server thread"
#         k = 0
#         p = pyaudio.PyAudio()
#         wf = wave.open(name,'rb')
#         stream = p.open(format =
#                 p.get_format_from_width(wf.getsampwidth()),
#                 channels = wf.getnchannels(),
#                 rate = wf.getframerate(),
#                 output = True,
#                 frames_per_buffer=CHUNK)
#         data = wf.readframes(CHUNK)
#         k = wf.tell()

#         while not self.changeFlag.is_set() and not self.shutdown_flag.is_set() and data:
#             stream.write(data)
#             data = wf.readframes(CHUNK)
#             k = wf.tell()

#         stream.stop_stream()
#         stream.close()
#         p.terminate() 
#         if self.shutdown_flag.is_set():
#             print "Server Closed"
#         elif self.changeFlag.is_set():
#             print "Changing Song"
#             self.changeFlag.clear()
#             return
#         else:
#             print "song end in server"

# while True:
#     try: 
#         clients = []
#         server = serverJob()
#         server.start()
#         time.sleep(2)
#         for conn in conns:
#             client = clientJob(conn)
#             client.start()
#             clients.append(client)
#         while True:
#             conn, addr = s.accept()
#             conns.append(conn)
#             print 'Connected by', addr
#             client = clientJob(conn)
#             client.start()
#             clients.append(client)
#     except KeyboardInterrupt:
#             # server.shutdown_flag.set()
#             # for client in clients:
#             #     client.shutdown_flag.set()
#             #     client.join()
#             # server.join()
#             print "Changing"
#             server.changeFlag.set()
#             for client in clients:
#                 client.changeFlag.set()
#             server.join()
#             for client in clients:
#                 client.join()
#             time.sleep(2)
        



print("*closed")