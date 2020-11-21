from model import Model


class Player(Model):
    def __init__(
        self,
        name,
        assets_folder,
        animations_prefix,
        texture_path,
        initial_position,
        size,
        speed,
        default_sound,
        back,
    ):
        super().__init__(
            name,
            assets_folder,
            animations_prefix,
            texture_path,
            initial_position,
            size,
            speed,
            default_sound,
            back,
        )

        self.actions = {
            "jump": {"active": False},
            "crouch": {"active": False},
            "attack": {"active": False},
            "wave": {"active": False},
            "salute": {"active": False},
            "point": {"active": False},
        }

        self.movement = []

    def add_move(self, move):
        self.change_animation("run")
        self.movement.append(move)
        for model in self.child_models:
            model.add_move(move)

    def remove_move(self, move):
        if move in self.movement:
            self.movement.remove(move)
            if len(self.movement) == 0:
                self.change_animation()
        for model in self.child_models:
            model.remove_move(move)

    def get_movement(self):
        return (
            self.movement
            if all([not self.actions[action]["active"] for action in self.actions])
            else []
        )

    def do_action(self, action_name):
        action = self.actions[action_name]
        if not action["active"]:
            for other_action in self.actions:
                self.actions[other_action]["active"] = False
            self.change_animation(action_name)
        else:
            animation = "run" if len(self.movement) else None
            self.change_animation(animation)

        self.actions[action_name]["active"] = not action["active"]
        for model in self.child_models:
            model.do_action(action_name)

