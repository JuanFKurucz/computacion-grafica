from model import Model


class Player(Model):
    def __init__(self, assets_folder, animations_prefix, texture_path):
        super().__init__(assets_folder, animations_prefix, texture_path)

        self.jumping = False
        self.crouching = False

    def jump(self):
        if not self.jumping:
            self.changeAnimation("jump")
        else:
            self.changeAnimation()
        self.jumping = not self.jumping

    def crouch(self):
        if not self.crouching:
            self.changeAnimation("crouch_stand")
        else:
            self.changeAnimation()

        self.crouching = not self.crouching

    def update(self):
        # if self.jumping:
        pass

