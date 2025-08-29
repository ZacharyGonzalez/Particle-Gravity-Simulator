import pyaudiowpatch as pyaudio
import time
import numpy as np
import threading
from collections import deque

DURATION = 5.0
CHUNK_SIZE = 512    
p=pyaudio.PyAudio()
buffer = deque()

def get_playback_device(p):
        try:
            wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
        except OSError:
            exit()
        default_speakers = p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])
        if not default_speakers["isLoopbackDevice"]:
            for loopback in p.get_loopback_device_info_generator():
                if default_speakers["name"] in loopback["name"]:
                    return loopback
        return default_speakers

default_speakers=get_playback_device(p)
def callback(in_data, frame_count, time_info, status):
    audio_data = np.frombuffer(in_data, dtype=np.int16)
    rms = np.sqrt(np.mean(audio_data.astype(np.float32)**2))
    print(f"Chunk received, RMS: {rms:.2f}")
    audio_data = (audio_data * 0.0).astype(np.int16).tobytes()
    return (audio_data, pyaudio.paContinue)

def create_input_stream():
    with p.open(format=pyaudio.paInt16,
        channels=default_speakers["maxInputChannels"],
        rate=int(default_speakers["defaultSampleRate"]),
        frames_per_buffer=CHUNK_SIZE,
        input=True,
        input_device_index=default_speakers["index"],
        stream_callback=callback    
        ) as in_stream:
            in_stream.start_stream()
            time.sleep(DURATION)

def create_output_stream():
    with p.open(format=pyaudio.paInt16,
        channels=default_speakers["maxInputChannels"],
        rate=int(default_speakers["defaultSampleRate"]),
        frames_per_buffer=CHUNK_SIZE,
        output=True) as out_stream:
            out_stream.start_stream()
            time.sleep(DURATION)

if __name__ == "__main__":
    threads=[]
    t = threading.Thread(target=create_input_stream,args=())
    threads.append(t)
    t = threading.Thread(target=create_output_stream,args=())
    threads.append(t)

    for t in threads:
        t.start()   