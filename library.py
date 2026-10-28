from pybricks.parameters import Color, Stop
from pybricks.tools import wait

from robot_config import (
    ACCELERATION, DRIVE_BASE, HUB, SPEED, TURN_ACCELERATION, TURN_SPEED,
    SHAKE_SPEED, SHAKE_ACCELERATION, SHAKE_AMPLITUDE, SHAKE_CYCLES,
)

RAINBOW = [Color.RED, Color.ORANGE, Color.YELLOW, Color.GREEN,
           Color.CYAN, Color.BLUE, Color.VIOLET]


def set_drivebase():
    DRIVE_BASE.settings(
        straight_speed=SPEED,
        straight_acceleration=ACCELERATION,
        turn_rate=TURN_SPEED,
        turn_acceleration=TURN_ACCELERATION,
    )


async def initialize_robot():
    """Enable gyro steering once, after the stationary hub is ready."""
    DRIVE_BASE.stop()
    while not HUB.imu.ready():
        HUB.display.char('E')
        HUB.light.on(Color.RED)
        await wait(50)
    DRIVE_BASE.use_gyro(True)
    set_drivebase()


def prepare_mission():
    """Restore configured speeds and show the running-mission light."""
    DRIVE_BASE.stop()
    set_drivebase()
    HUB.light.animate(RAINBOW, interval=1000)


async def drive_with_speed(speed: int, distance: int):
    DRIVE_BASE.reset(distance=0, angle=DRIVE_BASE.angle())
    DRIVE_BASE.drive(speed, 0)
    try:
        while abs(DRIVE_BASE.distance()) < abs(distance):
            await wait(10)
    finally:
        DRIVE_BASE.stop()


async def drive_straight(speed: int, acceleration: int, distance: int, then=Stop.HOLD):
    old_speed, old_acceleration = DRIVE_BASE.settings()[:2]
    try:
        DRIVE_BASE.settings(straight_speed=speed, straight_acceleration=acceleration)
        await DRIVE_BASE.straight(distance, then=then)
    finally:
        DRIVE_BASE.settings(straight_speed=old_speed, straight_acceleration=old_acceleration)


async def shake(cycles: int = SHAKE_CYCLES):
    """Chain backward/forward moves, stopping only after the final leg."""
    for cycle in range(cycles):
        await drive_straight(
            SHAKE_SPEED, SHAKE_ACCELERATION, -SHAKE_AMPLITUDE, then=Stop.NONE,
        )
        await drive_straight(
            SHAKE_SPEED, SHAKE_ACCELERATION, SHAKE_AMPLITUDE + 3,
            then=Stop.HOLD if cycle == cycles - 1 else Stop.NONE,
        )
