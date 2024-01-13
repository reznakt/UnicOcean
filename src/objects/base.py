from core import Direction


class OceanObject:
    skin: list[list[str]]
    anchor: tuple[int, int]
    depth: int
    """ Z-index of the object, the higher the less overshadowed """

    def __init__(self, anchor_coordinates: tuple[int, int], depth: int = 0):
        self.anchor = anchor_coordinates
        self.depth = depth


class MovingObject(OceanObject):
    DEFAULT_MOVE_INDEX = 10
    MAX_SPEED = 10
    direction: Direction
    speed: int
    move_index = DEFAULT_MOVE_INDEX

    def __init__(
        self,
        anchor_coordinates: tuple[int, int],
        skin: list[list[str]],
        direction: Direction,
        speed: int = 1,
    ):
        super().__init__(anchor_coordinates)
        self.skin = skin
        self.direction = direction
        self.speed = min(self.MAX_SPEED, speed)

    def move(self) -> None:
        """Moves the object in the given direction."""
        self.move_index -= self.speed
        if self.move_index > 0:
            return

        else:
            self.move_index += self.DEFAULT_MOVE_INDEX

        row_delta, col_delta = self.direction.value
        row, col = self.anchor
        self.anchor = (row + row_delta, col + col_delta)


class Fish(MovingObject):
    skin_left: list[list[str]]
    """ Skin for the fish swimming in the left direction """
    skin_right: list[list[str]]
    """ Skin for the fish swimming in the right direction """
    carnivorous: bool

    def __init__(
        self,
        anchor_coordinates: tuple[int, int],
        skin: list[list[str]],
        direction: Direction,
        speed: int,
        skin_left: list[list[str]],
        skin_right: list[list[str]],
        carnivorous: bool,
    ):
        super().__init__(anchor_coordinates, skin, direction, speed)
        self.skin_left = skin_left
        self.skin_right = skin_right
        self.skin = skin_left if direction == Direction.LEFT else skin_right
        self.carnivorous = carnivorous

    def change_direction(self) -> None:
        """Changes the direction of the fish."""
        went_left = self.direction == Direction.LEFT
        self.direction = Direction.RIGHT if went_left else Direction.LEFT
        self.skin = self.skin_right if went_left else self.skin_left


class StaticObject(OceanObject):
    def __init__(self, anchor_coordinates: tuple[int, int], skin: list[list[str]]):
        super().__init__(anchor_coordinates)
        self.skin = skin