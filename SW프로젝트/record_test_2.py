import sys
import pprint

import pyaudio

CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5

p = pyaudio.PyAudio()
count = p.get_device_count()
devices = []
for i in range(count):
    devices.append(p.get_device_info_by_index(i))

for i, dev in enumerate(devices):
    print(
    "%d - %s" % (i, dev['name']))

if len(sys.argv) < 3:
    input_device_index = int(input('Choose src: '))
    output_device_index = int(input('Choose dst: '))
else:
    input_device_index = int(sys.argv[1])
    output_device_index = int(sys.argv[2])

print
'--- src ---'
pprint.pprint(devices[input_device_index])
print
'--- dst ---'
pprint.pprint(devices[output_device_index])

src = p.open(format=FORMAT,
             channels=CHANNELS,
             rate=RATE,
             input=True,
             input_device_index=input_device_index,
             frames_per_buffer=CHUNK)

dst = p.open(format=FORMAT,
             channels=CHANNELS,
             rate=RATE,
             output=True,
             output_device_index=output_device_index,
             frames_per_buffer=CHUNK)

print
""
src_latency = 1000.0 * dst.get_input_latency()
buffer_latency = 1000.0 * CHUNK / RATE
dst_latency = 1000.0 * dst.get_output_latency()
total_latency = buffer_latency + dst_latency + src_latency
print
"Expected delay: %0.1f ms (%0.1f, %0.1f, %0.1f)" % (
    total_latency, src_latency, buffer_latency, dst_latency)

print
"Replicating audio"

while True:
    data = src.read(CHUNK)
    dst.write(data, CHUNK)

print
"* done"

src.stop_stream()
src.close()
dst.stop_stream()
dst.close()
p.terminate()