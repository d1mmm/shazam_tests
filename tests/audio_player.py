import threading
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio



class AudioPlayer:
    def __init__(self, file_path):
        self.audio = AudioSegment.from_file(file_path)
        self.playback = None

    def play(self):
        self.playback = _play_with_simpleaudio(self.audio)

    def stop(self):
        if self.playback:
            self.playback.stop()


def play_audio_in_thread(player):
    audio_thread = threading.Thread(target=player.play)
    audio_thread.start()
    return audio_thread