import rumps
import requests

class SimpleMenuBarApp(rumps.App):
    def __init__(self):
        super(SimpleMenuBarApp, self).__init__("API Tester", icon=None)
        self.menu = ["Call API", "About"]

    @rumps.clicked("Call API")
    def call_api(self, _):
        response = requests.get('http://127.0.0.1:8000/')  # FastAPI runs on port 8000
        rumps.alert(f"API Response: {response.json()['message']}")

    @rumps.clicked("About")
    def about(self, _):
        rumps.alert("This is a simple macOS menu bar app using FastAPI and rumps.")

if __name__ == "__main__":
    SimpleMenuBarApp().run()
