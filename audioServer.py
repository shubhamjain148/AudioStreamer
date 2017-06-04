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

HOST = '192.168.0.110'    # The remote host
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
    # print (wf2.getsampwidth())
    # print wf2.getnchannels()
    # print wf2.getframerate()
    # print t
    # print CHUNK
    # print wf2.getframerate()
    # temp = (t*wf2.getframerate())/CHUNK
    # print temp
    print t
    wf2.setpos(t)
    for i in range(0, int(wf2.getframerate()/CHUNK*RECORD_SECONDS)):
        data = wf2.readframes(CHUNK)
        conn.sendall(data)

read = 0
def serverThread(wf):
    global k
    stream = p.open(format =
            p.get_format_from_width(wf.getsampwidth()),
            channels = wf.getnchannels(),
            rate = wf.getframerate(),
            output = True,
            frames_per_buffer=CHUNK)
    for i in range(0, int(wf.getframerate()/CHUNK*RECORD_SECONDS)):
        data = wf.readframes(CHUNK)
        k = wf.tell()
        stream.write(data)

start_new_thread(serverThread, (wf,))

while True:
    conn, addr = s.accept()
    print 'Connected by', addr
    start_new_thread(clientThread, (conn, k, wf))




stream.stop_stream()
stream.close()
p.terminate()
conn.close()
 
print("*closed")