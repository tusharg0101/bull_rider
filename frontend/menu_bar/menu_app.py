import os
import rumps
import requests
import threading
from pydub import AudioSegment
from pydub.playback import play
from utils import record_audio, save_audio, capture_screenshot
import time

class BullRiderApp(rumps.App):
    def __init__(self):
        super(BullRiderApp, self).__init__("Bull Rider", icon="./icons/bull_rider.png")
        # Define the folder for saving files, using absolute path for reliability
        self.output_folder = os.path.abspath('./temp_audio')  
        os.makedirs(self.output_folder, exist_ok=True)  # Ensure folder exists

        # Define menu items
        self.start_tutorial_item = rumps.MenuItem(title="Start Tutorial", callback=self.start_tutorial)
        self.end_recording_item = rumps.MenuItem(title="End Recording", callback=None)  # Disabled initially

        self.menu = [
            self.start_tutorial_item,
            self.end_recording_item,
            "Call API",
            "About",
            "Quit"
        ]
        
        self.is_recording_flag = False
        self.audio_frames = []
        self.audio_thread = None
        self.env_active = False  # To track if a tutorial session is active

    def start_tutorial(self, _):
        # Start a new tutorial session
        if not self.env_active:
            self.env_active = True
            self.start_recording()

    def start_recording(self):
        if not self.is_recording_flag:
            self.is_recording_flag = True
            self.audio_frames = []
            try:
                # Disable the Start button, enable the End button
                self.start_tutorial_item.set_callback(None)
                self.end_recording_item.set_callback(self.end_recording)
                self.end_recording_item.state = True

                # Start the audio recording in a new thread
                self.audio_thread = threading.Thread(target=record_audio, args=(self.audio_frames, self._is_recording))
                self.audio_thread.start()
            except Exception as e:
                rumps.alert(f"Error starting recording: {str(e)}")

    def end_recording(self, _=None):
        if self.is_recording_flag:
            self.is_recording_flag = False
            if self.audio_thread:
                self.audio_thread.join()  # Wait for the audio thread to finish

            try:
                # Re-enable the Start button, disable the End button
                self.start_tutorial_item.set_callback(self.start_tutorial)
                self.end_recording_item.set_callback(None)
                self.end_recording_item.state = False

                # Save audio
                audio_path = os.path.join(self.output_folder, 'recorded_audio.wav')
                save_audio(audio_path, self.audio_frames)

                # Capture the screenshot and save in the same folder
                screenshot_path = os.path.join(self.output_folder, 'screenshot.png')
                capture_screenshot(screenshot_path)  # Ensure the format is consistent with the file extension

                # Now send the files to the FastAPI backend
                self.upload_files(audio_path, screenshot_path)

                # Once the backend sends the output.wav file, play it and listen for next step
                self.play_and_listen_again()

            except Exception as e:
                rumps.alert(f"Error during saving process: {str(e)}")

    def play_and_listen_again(self):
        try:
            # Assuming the output file is returned and available
            output_wav_path = os.path.join(self.output_folder, 'output.wav')
            
            # Play the output.wav file
            audio = AudioSegment.from_wav(output_wav_path)
            play(audio)

            # After playing, wait for a bit before starting to listen again
            time.sleep(1)  # You can adjust the delay if needed
            self.play_listening_sound()

            # Start listening for the next step
            if self.env_active:
                self.start_recording()

        except Exception as e:
            rumps.alert(f"Error during playback or listening: {str(e)}")

    def play_listening_sound(self):
        # Play a sound effect to indicate the system is listening
        listening_sound_path = os.path.join(self.output_folder, 'listening_sound.wav')
        if os.path.exists(listening_sound_path):
            audio = AudioSegment.from_wav(listening_sound_path)
            play(audio)

    def upload_files(self, audio_file_path, image_file_path):
        url = "http://127.0.0.1:8084/tutorial"  # The endpoint to upload files to FastAPI
        try:
            with open(audio_file_path, 'rb') as audio_file, open(image_file_path, 'rb') as image_file:
                files = {
                    'audio_file': ('recorded_audio.wav', audio_file, 'audio/wav'),
                    'image_file': ('screenshot.png', image_file, 'image/png')  # Correct format
                }
                response = requests.post(url, files=files)
                if response.status_code != 200:
                    rumps.alert(f"Failed to upload files. Status code: {response.status_code}")
        except Exception as e:
            rumps.alert(f"Error uploading files: {str(e)}")

    @rumps.clicked("Quit")
    def quit_app(self, _):
        if self.is_recording_flag:
            self.is_recording_flag = False
            if self.audio_thread:
                self.audio_thread.join()  # Ensure the thread is finished before quitting
        self.env_active = False
        rumps.quit_application()

    def _is_recording(self):
        return self.is_recording_flag

if __name__ == "__main__":
    BullRiderApp().run()
