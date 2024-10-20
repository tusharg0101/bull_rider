import pyaudio
import wave
import mss
import mss.tools
from PIL import Image
import os

# Record audio using pyaudio
def record_audio(audio_frames, is_recording):
    chunk = 1024  # Record in chunks of 1024 samples
    format = pyaudio.paInt16  # 16 bits per sample
    channels = 1  # Mono audio
    rate = 44100  # Sample rate

    p = pyaudio.PyAudio()
    try:
        stream = p.open(format=format,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)

        print("Recording audio...")
        while is_recording():
            data = stream.read(chunk, exception_on_overflow=False)
            audio_frames.append(data)

        # Stop and close the stream once recording is stopped
        stream.stop_stream()
        stream.close()
    finally:
        p.terminate()

# Save audio to a file
def save_audio(filename, audio_frames):
    p = pyaudio.PyAudio()
    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(audio_frames))
    wf.close()
    print(f"Audio saved as {filename}")

# Capture a screenshot using mss
def capture_screenshot(filename):
    try:
        with mss.mss() as sct:
            sct.shot(output=filename)  # Capture the screen and save it to the specified file
            
        image = Image.open(filename)

        width, height = image.size
        new_size = (width//4, height//4)
        resized_image = image.resize(new_size)

        resized_image.save(filename, optimize=True, quality=50)

        print(f"Screenshot saved as {filename}")
    except Exception as e:
        print(f"Error during capturing screenshot: {str(e)}")
