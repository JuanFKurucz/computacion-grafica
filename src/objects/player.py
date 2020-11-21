from model import Model


class Player(Model):
    def __init__(self, name, assets_folder, animations_prefix, texture_path):
        super().__init__(name, assets_folder, animations_prefix, texture_path)

        self.jumping = False
        self.crouching = False

        self.movement = []

    def add_move(self, move):
        self.change_animation("run")
        self.movement.append(move)
        for model in self.child_models:
            model.add_move(move)

    def remove_move(self, move):
        self.movement.remove(move)
        if len(self.movement) == 0:
            self.change_animation()
        for model in self.child_models:
            model.remove_move(move)

    def jump(self):
        if not self.jumping:
            self.change_animation("jump")
        else:
            self.change_animation()
        self.jumping = not self.jumping
        for model in self.child_models:
            model.jump()

    def crouch(self):
        if not self.crouching:
            self.change_animation("crouch_stand")
        else:
            self.change_animation()

        self.crouching = not self.crouching
        for model in self.child_models:
            model.crouch()
