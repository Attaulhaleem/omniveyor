from motor import *

ACTIONS = {
    "idle": (STATES["release"], STATES["release"], STATES["release"]),
    "up_right": (STATES["release"], STATES["forward"], STATES["backward"]),
    "right": (STATES["forward"], STATES["release"], STATES["backward"]),
    "down_right": (STATES["forward"], STATES["backward"], STATES["release"]),
    "down_left": (STATES["release"], STATES["backward"], STATES["forward"]),
    "left": (STATES["backward"], STATES["release"], STATES["forward"]),
    "up_left": (STATES["backward"], STATES["forward"], STATES["release"]),
    "clockwise": (STATES["forward"], STATES["forward"], STATES["forward"]),
    "anti_clockwise": (STATES["backward"], STATES["backward"], STATES["backward"]),
}


class Module:
    """A module of the Omniveyor. Consists of 3 motors controlled by the L293D Motor Driver Shield."""

    # see shield schematic [M3 and M4 were replaced on my shield] (http://wiki.sunfounder.cc/images/f/ff/L293D_schematic.png)
    # output format [4A, 2A, 1A, 1B, 2B, 3B, 4B, 3A]
    PIN_CONFIG = ((2, 3), (1, 4), (7, 5))  # motor pins on shift register output

    def __init__(self, position, action=ACTIONS["idle"]):
        """Initialize a module.

        Args:
            position (tuple[int, int]): (x, y) position of module in pi camera frame.
            action (tuple[tuple[int, int], tuple[int, int], tuple[int, int]], optional): Current action performed by the module. Defaults to ACTIONS["idle"].
        """
        self.position = position
        self.motors = [
            Motor(self.PIN_CONFIG[i], self.get_motor_positions(position)[i])
            for i in range(3)
        ]
        self.set_action(action)

    def get_motor_positions(self, position):
        """Get the 3 motor positions in pi camera frame from the module center position.

        Args:
            position (tuple[int, int]): Module center position in pi camera frame.

        Returns:
            tuple[tuple[int, int], tuple[int, int], tuple[int, int]]: A tuple of 3 motor positions.
        """
        return ((0, 0), (0, 0), (0, 0))

    def set_action(self, action):
        """Set module action and corresponding motor states. Also update shift register data.

        Args:
            action (tuple[tuple[int, int], tuple[int, int], tuple[int, int]]): Any action in ACTIONS.

        Raises:
            Exception: Action is not in ACTIONS.
        """
        if action not in ACTIONS.values():
            raise Exception("Invalid module action!")
        for i, motor in enumerate(self.motors):
            motor.set_state(action[i])
        # set action before encoding data for SR
        self.action = action
        self.encode_sr_byte()

    def encode_sr_byte(self):
        """Encode the motor states as data for writing to shift register."""
        # initialize empty byte
        data_list = [0 for _ in range(8)]
        for motor in self.motors:
            for i in range(2):
                data_list[motor.pins[i]] = motor.state[i]
        self.sr_byte = data_list

    def is_below_package(self, bbox):
        """Identify which motors lie under the bounding box.

        Args:
            bbox (tuple[int, int, int, int]): The bounding box (x, y, w, h) of the package.
        """
        # TODO: implement angled boxes
        for motor in self.motors:
            if (
                motor.position[0] >= bbox.x
                and motor.position[0] < bbox.x + bbox.w
                and motor.position[1] >= bbox.y
                and motor.position[1] < bbox.y + bbox.h
            ):
                return True
        return False
