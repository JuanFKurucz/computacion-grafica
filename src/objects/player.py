from model import Model


class Player(Model):
    def __init__(
        self, name, assets_folder, animations_prefix, texture_path, initial_position, size, speed, default_sound
    ):
        super().__init__(
            name, assets_folder, animations_prefix, texture_path, initial_position, size, speed, default_sound
        )

        self.jumping = False
        self.crouching = False

        self.movement = []

    def add_move(self, move):
        self.change_animation("run")
        self.movement.append(move)
        for model in self.child_models:
            model.add_move(move)
        if self.crouching:
            self.crouching = not self.crouching

    def remove_move(self, move):
        if move in self.movement:
            self.movement.remove(move)
            if len(self.movement) == 0:
                self.change_animation()
        for model in self.child_models:
            model.remove_move(move)

    def get_movement(self):
        return self.movement if not self.crouching else []

    def jump(self):
        if not self.jumping:
            self.crouching = False
            self.change_animation("jump")
        else:
            animation = "run" if len(self.movement) else None
            self.change_animation(animation)

        self.jumping = not self.jumping
        for model in self.child_models:
            model.jump()

    def crouch(self):
        if not self.crouching:
            self.change_animation("crouch_stand")
            self.jumping = False
        else:
            animation = "run" if len(self.movement) else None
            self.change_animation(animation)

        self.crouching = not self.crouching
        for model in self.child_models:
            model.crouch()
