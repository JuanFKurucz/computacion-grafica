import glob
from time import time
from obj import Object


class Animation:
    def __init__(self, name, frames=0, sound=None):
        self.name = name
        self.frames = frames
        self.current_frame = 0
        self.objs = {}
        self.start_time = 0
        self.sound = sound

    def load_animation(self, file):
        file_index = file.split(".")[-2].split("_")[-1]
        self.objs[file_index] = Object.load_obj(file)

    def load_animations(self, dir, prefix):
        for name in glob.glob(f"{dir}/*{prefix}*.obj"):
            self.load_animation(name)

    @property
    def current_obj(self):
        self.current_frame = int((time() - self.start_time) * self.frames % len(self.objs))
        return self.objs[str(self.current_frame)]
