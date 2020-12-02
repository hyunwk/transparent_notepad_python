import sounddevice as sd
from scipy.io.wavfile import write
import os
from stt_etri import play_audio
def record():
    fs = 16000 # this is the frequency sampling; also: 4999, 64000
    seconds = 2  # Duration of recording
    #sd.default.device = 'digital output'

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    print("Starting: Speak now!")
    sd.wait()  # Wait until recording is finished
    print("finished")
    write('output.wav', fs, myrecording)  # Save as WAV file

    os.startfile("output.wav")
    play_audio()
