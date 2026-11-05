import threading
import time
import os
from gtts import gTTS

class AudioFeedback:
    def __init__(self, cooldown=3.0):
        self.is_playing = False
        self.last_alert_time = 0
        self.cooldown = cooldown 

    def _play_sound(self, text):
        self.is_playing = True
        try:
            tts = gTTS(text=text, lang='en')
            filename = "alert.mp3"
            tts.save(filename)
            
            # macOS uses afplay, Linux uses mpg123, Windows can use os.startfile
            if os.name == 'posix':
                os.system(f"afplay {filename}" if 'darwin' in os.uname().sysname.lower() else f"mpg123 -q {filename}")
            else:
                os.system(f"start {filename}")
        except Exception as e:
            print(f"Audio failed: {e}")
        finally:
            self.is_playing = False

    def play_alert(self, text):
        current_time = time.time()
        # Only trigger if not currently speaking and cooldown has passed
        if not self.is_playing and (current_time - self.last_alert_time) > self.cooldown:
            self.last_alert_time = current_time
            thread = threading.Thread(target=self._play_sound, args=(text,))
            thread.start()