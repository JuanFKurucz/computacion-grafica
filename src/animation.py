import glob
from time import time
from obj import Object


class Animation:
    def __init__(self, frames=0):
        self.frames = frames
        self.current_frame = 0
        self.objs = {}
        self.start_time = 0

    def loadAnimation(self, file):
        file_index = file.split(".")[-2].split("_")[-1]
        if not file_index:
            file_index = "0"
        self.objs[file_index] = Object.loadObj(file)

    def loadAnimations(self, dir, prefix):
        for name in glob.glob(f"{dir}/{prefix}*"):
            self.loadAnimation(name)

    def getCurrentObj(self):
        self.current_frame = int((time() - self.start_time) * self.frames % len(self.objs))
        return self.objs[str(self.current_frame)]
