import socket
import pyaudio
import wave
import time
import struct

CHUNK = 1024*4
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
                frames_per_buffer=1024*4)

multicast_group = '224.0.0.251'
server_address = ('', 9999)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
sock.bind(server_address)



# Tell the operating system to add the socket to the multicast group
# on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

i=1
while True:
    data, address = sock.recvfrom(CHUNK)
    # print data
    # print i
    i+=1
    print len(data) 
    sent = sock.sendto(data, address)
    stream.write(data)
print "closing"
stream.stop_stream()
stream.close()
p.terminate()
