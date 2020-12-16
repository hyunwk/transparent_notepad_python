import pyaudio

# detect devices:
p = pyaudio.PyAudio()
host_info = p.get_host_api_info_by_index(0)
device_count = host_info.get('deviceCount')
devices = []

# iterate between devices:
for i in range(0, device_count):
    device = p.get_default_output_device_info(0,i)
    print(i, device['name'])
