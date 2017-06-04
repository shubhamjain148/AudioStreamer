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


HOST = '192.168.0.110'                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


data = s.recv(CHUNK)
print type(data)
i=1
while data != '':
    data = s.recv(CHUNK)
    print i
    stream.write(data)
    i=i+1
    print i
    frames.append(data)

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

stream.stop_stream()
stream.close()
p.terminate()
