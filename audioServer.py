import socket
import pyaudio
import wave
import time
from thread import *


#record
CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 100

HOST = '192.168.0.105'    # The remote host
PORT = 50007              # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)


frames = []
k = None
p = pyaudio.PyAudio()


wf = wave.open('closer2.wav','rb')
z = 0
stream = None

def clientThread(conn, t, wf2):
    
    wf2 = wave.open('closer2.wav','rb')
    # print t
    wf2.setpos(k)
    data = wf2.readframes(CHUNK)
    while data:
        conn.sendall(data)
        data = wf2.readframes(CHUNK)
    conn.sendall("")
    print "song end in client"
    conn.close()

read = 0
def serverThread(wf):
    global k
    stream = p.open(format =
            p.get_format_from_width(wf.getsampwidth()),
            channels = wf.getnchannels(),
            rate = wf.getframerate(),
            output = True,
            frames_per_buffer=CHUNK)
    data = wf.readframes(CHUNK)
    k = wf.tell()
    while data:
        stream.write(data)
        data = wf.readframes(CHUNK)
        k = wf.tell()
    print "song end in server"

start_new_thread(serverThread, (wf,))

while True:
    conn, addr = s.accept()
    print 'Connected by', addr
    start_new_thread(clientThread, (conn, k, wf))


stream.stop_stream()
stream.close()
p.terminate() 
print("*closed")