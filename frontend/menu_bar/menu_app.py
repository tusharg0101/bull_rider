import os
import rumps
import requests
import threading
from utils import record_audio, save_audio, capture_screenshot

class BullRiderApp(rumps.App):
    def __init__(self):
        super(BullRiderApp, self).__init__("Bull Rider", icon="./icons/bull_rider.png")
        # Define the folder for saving files, using absolute path for reliability
        self.output_folder = os.path.abspath('./temp_audio')  
        os.makedirs(self.output_folder, exist_ok=True)  # Ensure folder exists

        # Define menu items
        self.start_recording_item = rumps.MenuItem(title="Start Recording", callback=self.start_recording)
        self.end_recording_item = rumps.MenuItem(title="End Recording", callback=None)  # Disabled initially

        self.menu = [
            self.start_recording_item,
            self.end_recording_item,
            "Call API",
            "About",
            "Quit"
        ]
        
        self.is_recording_flag = False
        self.audio_frames = []
        self.audio_thread = None

    def start_recording(self, _):
        if not self.is_recording_flag:
            self.is_recording_flag = True
            self.audio_frames = []

            try:
                # Disable the Start button, enable the End button
                self.start_recording_item.set_callback(None)
                self.end_recording_item.set_callback(self.end_recording)
                self.end_recording_item.state = True

                # Start the audio recording in a new thread
                self.audio_thread = threading.Thread(target=record_audio, args=(self.audio_frames, self._is_recording))
                self.audio_thread.start()

                rumps.notification("Bull Rider", "Recording Started", "Audio recording in progress...")
            except Exception as e:
                rumps.alert(f"Error starting recording: {str(e)}")

    def end_recording(self, _):
        if self.is_recording_flag:
            self.is_recording_flag = False
            if self.audio_thread:
                self.audio_thread.join()  # Wait for the audio thread to finish

            try:
                # Re-enable the Start button, disable the End button
                self.start_recording_item.set_callback(self.start_recording)
                self.end_recording_item.set_callback(None)
                self.end_recording_item.state = False

                # Save audio
                audio_path = os.path.join(self.output_folder, 'recorded_audio.wav')
                save_audio(audio_path, self.audio_frames)
                rumps.alert(f"Recording stopped and audio saved as '{audio_path}'")
                
                # Capture the screenshot and save in the same folder
                screenshot_path = os.path.join(self.output_folder, 'screenshot.png')
                capture_screenshot(screenshot_path)  # Ensure the format is consistent with the file extension
                rumps.alert(f"Screenshot saved as '{screenshot_path}'")
                
                # Now send the files to the FastAPI backend
                self.upload_files(audio_path, screenshot_path)

            except Exception as e:
                rumps.alert(f"Error during saving process: {str(e)}")

    def upload_files(self, audio_file_path, image_file_path):
        url = "http://127.0.0.1:8084/tutorial"  # The endpoint to upload files to FastAPI
        try:
            with open(audio_file_path, 'rb') as audio_file, open(image_file_path, 'rb') as image_file:
                files = {
                    'audio_file': ('recorded_audio.wav', audio_file, 'audio/wav'),
                    'image_file': ('screenshot.png', image_file, 'image/png')  # Correct format
                }
                response = requests.post(url, files=files)
                if response.status_code == 200:
                    rumps.alert(f"Files uploaded successfully. Backend response: {response.json()}")
                else:
                    rumps.alert(f"Failed to upload files. Status code: {response.status_code}")
        except Exception as e:
            rumps.alert(f"Error uploading files: {str(e)}")

    @rumps.clicked("Quit")
    def quit_app(self, _):
        if self.is_recording_flag:
            self.is_recording_flag = False
            if self.audio_thread:
                self.audio_thread.join()  # Ensure the thread is finished before quitting
        rumps.quit_application()

    def _is_recording(self):
        return self.is_recording_flag

if __name__ == "__main__":
    BullRiderApp().run()
