import os
import rumps
import requests
import threading
from pydub import AudioSegment
from pydub.playback import play
from utils import record_audio, save_audio, capture_screenshot

class BullRiderApp(rumps.App):
    def __init__(self):
        super(BullRiderApp, self).__init__("Bull Rider", icon="./icons/bull_rider.png")
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

    def get_tutorial_state(self):
        try:
            response = requests.get("http://127.0.0.1:8084/tutorial_state")
            return response.json()["tutorial_active"]
        except Exception as e:
            print(f"Error getting tutorial state: {str(e)}")
            return False

    def set_tutorial_state(self, state):
        try:
            response = requests.post("http://127.0.0.1:8084/tutorial_state", json={"state": state})
            return response.json()["tutorial_active"]
        except Exception as e:
            print(f"Error setting tutorial state: {str(e)}")
            return False

    def get_current_step(self):
        try:
            response = requests.get("http://127.0.0.1:8084/current_step")
            return response.json()["current_step"]
        except Exception as e:
            print(f"Error getting current step: {str(e)}")
            return 0

    def set_current_step(self, step):
        try:
            response = requests.post("http://127.0.0.1:8084/current_step", json={"step": step})
            return response.json()["current_step"]
        except Exception as e:
            print(f"Error setting current step: {str(e)}")
            return 0

    def start_tutorial(self, _):
        if not self.get_tutorial_state():
            self.set_tutorial_state(True)
            self.set_current_step(0)
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
                capture_screenshot(screenshot_path)

                # Now send the file paths as strings to the FastAPI backend
                self.upload_file_paths(audio_path, screenshot_path)

                # Once the backend sends the output.wav file, start the dynamic listening process
                self.play_and_listen_again()

            except Exception as e:
                rumps.alert(f"Error during saving process: {str(e)}")

    def play_and_listen_again(self):
        try:
            current_step = self.get_current_step()
            output_wav_path = os.path.join(self.output_folder, f'output_{current_step}.wav')
            
            # Play the output.wav file asynchronously
            audio_thread = threading.Thread(target=self._play_audio_and_listen, args=(output_wav_path,))
            audio_thread.start()

        except Exception as e:
            rumps.alert(f"Error during playback or listening: {str(e)}")

    def _play_audio_and_listen(self, output_wav_path):
        try:
            # Play the output.wav file
            audio = AudioSegment.from_wav(output_wav_path)
            play(audio)

            # Audio has finished playing, now play the listening sound
            self.play_listening_sound()

            # Start listening for the next step
            if self.get_tutorial_state():
                self.start_recording()
            else:
                self.set_tutorial_state(False)
                self.set_current_step(0)

        except Exception as e:
            rumps.alert(f"Error during audio playback: {str(e)}")

    def play_listening_sound(self):
        # Play a sound effect to indicate the system is listening
        listening_sound_path = os.path.abspath('./sounds/listening_sound.wav')
        if os.path.exists(listening_sound_path):
            audio = AudioSegment.from_wav(listening_sound_path)
            play(audio)
        else:
            print("Listening sound not found.")

    def upload_file_paths(self, audio_file_path, image_file_path):
        url = "http://127.0.0.1:8084/tutorial"
        try:
            # Send the file paths as strings in the request
            data = {
                'audio_file_path': audio_file_path,
                'image_file_path': image_file_path
            }
            response = requests.post(url, json=data)
            if response.status_code == 200:
                print(f"Files paths sent successfully. Backend response: {response.json()}")
            else:
                print(f"Failed to send file paths. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error sending file paths: {str(e)}")

    @rumps.clicked("Quit")
    def quit_app(self, _):
        if self.is_recording_flag:
            self.is_recording_flag = False
            if self.audio_thread:
                self.audio_thread.join()
        self.set_tutorial_state(False)
        self.set_current_step(0)
        rumps.quit_application()

    def _is_recording(self):
        return self.is_recording_flag

if __name__ == "__main__":
    BullRiderApp().run()
