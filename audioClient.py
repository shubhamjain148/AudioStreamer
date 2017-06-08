import socket
import pyaudio
import wave
import time

CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 4
WAVE_OUTPUT_FILENAME = "server_outputCloser.wav"
WIDTH = 2
frames = []


p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)


HOST = 'localhost'                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


data = s.recv(CHUNK)
print type(data)
i=1
while data != '' and data!="Server exited" and data!="Song ended on server":
    stream.write(data)
    data = s.recv(CHUNK)
    frames.append(data)

if data!="Server exited":
    print "Song ended on serer"
else:
    print data
print "closing"
stream.stop_stream()
stream.close()
p.terminate()
