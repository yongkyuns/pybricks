from pybricks.hubs import PrimeHub
from pybricks.parameters import Axis, Direction, Port
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase

# Rover hardware; wheel diameter and axle track are in millimeters.
HUB = PrimeHub(top_side=Axis.Z, front_side=Axis.X)
DRIVE_LEFT = Motor(Port.B, Direction.COUNTERCLOCKWISE)
DRIVE_RIGHT = Motor(Port.A, Direction.CLOCKWISE)
DRIVE_BASE = DriveBase(DRIVE_LEFT, DRIVE_RIGHT, 56, 82)
LEFT_ATTACHMENT = Motor(Port.C, Direction.CLOCKWISE)
RIGHT_ATTACHMENT = Motor(Port.D, Direction.COUNTERCLOCKWISE)

SPEED = 400
ACCELERATION = 400
TURN_SPEED = 400
TURN_ACCELERATION = 400

# Tree shake: distances in mm, speeds in mm/s, acceleration in mm/s².
SHAKE_SPEED = 240
SHAKE_ACCELERATION = 2500
SHAKE_AMPLITUDE = 20  # Distance of each backward/forward leg in mm.
SHAKE_CYCLES = 3
