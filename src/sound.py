import time

from pygame import mixer


class Sound:
    sounds = {}

    def __init__(self, name, volume, loop):
        self.name = name
        self.volume = volume
        self.active = False
        self.playing = False
        self.loop = loop

    def start(self):
        if not self.active:
            self.active = True
            sound_channel = mixer.find_channel(True)
            sound_channel.set_volume(self.volume)
            if self.loop:
                self.play(loop=self.loop)

    def play(self, loop=False):
        if self.active and not self.playing:
            self.playing = True
            self.start_time = time.time()
            sound_channel = mixer.find_channel(True)
            loops = -1 if loop else 0
            sound_channel.play(self.sounds[self.name], loops=loops)
            if not loop:
                self.playing = False

    def stop(self):
        self.active = False

