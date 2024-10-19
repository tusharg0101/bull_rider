import pyaudio
import wave
import pyautogui

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

# Capture a screenshot using pyautogui, excluding the menu bar if possible
def capture_screenshot(filename):
    try:
        # Take a screenshot of the entire visible screen
        screenshot = pyautogui.screenshot()

        # Save the screenshot in the provided filename
        screenshot.save(filename)
        print(f"Screenshot saved as {filename}")
    except Exception as e:
        print(f"Error during capturing screenshot: {str(e)}")
