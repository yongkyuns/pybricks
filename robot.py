"""SPIKE Prime rover missions in one Pybricks program.

LEFT/RIGHT select, CENTER starts, and BLUETOOTH stops the program.
"""

from pybricks.hubs import PrimeHub
from pybricks.parameters import Axis, Button, Color, Direction, Port, Stop
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from pybricks.tools import multitask, run_task, wait


# Robot configuration

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


# Shared helpers

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


async def print_drivebase_settings():
    print('Default drivebase settings that are overridden in the config file')
    print('Speed, Acceleration, Turn, Turn Accel')
    print(DRIVE_BASE.settings())


# Missions

async def cage():
    await shake()


async def tree():
    await DRIVE_BASE.straight(-10)
    #Move towards the tree
    await LEFT_ATTACHMENT.run_until_stalled(150)
    await DRIVE_BASE.straight(650)
    await LEFT_ATTACHMENT.run_angle(500, -60)
    await DRIVE_BASE.turn(90)
    await DRIVE_BASE.straight(250)
    await DRIVE_BASE.turn(-90)
    await DRIVE_BASE.straight(-80)
    await wait(500)
    await RIGHT_ATTACHMENT.run_until_stalled(-1000)
    await wait(300)
    await RIGHT_ATTACHMENT.run_angle(600, 100)
    await drive_straight(600, 300, 135)
    await wait(700)
    await RIGHT_ATTACHMENT.run_angle(1000, 80)
    #Remove vine
    await wait(200)
    await RIGHT_ATTACHMENT.run_angle(1000, -150)
    await wait(200)
    await DRIVE_BASE.straight(-140)
    #Move to platform position
    await RIGHT_ATTACHMENT.run_angle(1000, 30)
    await DRIVE_BASE.turn(-90)
    await RIGHT_ATTACHMENT.run_angle(1000, -30)
    await DRIVE_BASE.straight(70)
    await DRIVE_BASE.turn(90)
    await wait(100)
    await LEFT_ATTACHMENT.run_until_stalled(-500)
    await LEFT_ATTACHMENT.run_angle(300, -10)
    await DRIVE_BASE.straight(50)
    #Lift platform + root
    await wait(200)
    await LEFT_ATTACHMENT.run_angle(1500, 100)
    for i in range(2):
        await RIGHT_ATTACHMENT.run_angle(900, 110)
        await DRIVE_BASE.straight(10)
    for i in range(2):
        await RIGHT_ATTACHMENT.run_angle(900, 50)
        await DRIVE_BASE.straight(10)
    #Move out
    await wait(500)
    await DRIVE_BASE.straight(-20)
    await DRIVE_BASE.straight(20)
    await wait(800)
    await multitask(
        RIGHT_ATTACHMENT.run_angle(800, -80),
        DRIVE_BASE.straight(12)
    )
    await DRIVE_BASE.straight(-80)
    await RIGHT_ATTACHMENT.run_until_stalled(1000)
    await LEFT_ATTACHMENT.run_until_stalled(-200)
    #Complete root mission
    await multitask(
        DRIVE_BASE.straight(50),
        LEFT_ATTACHMENT.run_until_stalled(-200)
    )
    await wait(100)
    await LEFT_ATTACHMENT.run_angle(850, 100)
    #Biocentric Architecture Skylight
    await DRIVE_BASE.turn(90)
    await DRIVE_BASE.straight(300)


async def drone():
    await drive_with_speed(180, 630)
    await DRIVE_BASE.turn(-45)
    await DRIVE_BASE.turn(45)
    await DRIVE_BASE.straight(-620)


async def rock():
    await DRIVE_BASE.straight(-10)
    await drive_with_speed(200, 305)
    await RIGHT_ATTACHMENT.run_angle(100, -115)
    await DRIVE_BASE.straight(-200)
    await DRIVE_BASE.turn(45)
    await DRIVE_BASE.straight(425)
    await RIGHT_ATTACHMENT.run_angle(230, 45)
    await multitask(
        drive_with_speed(-220, -500),
        RIGHT_ATTACHMENT.run_angle(100, 30)
    )


async def bioarchitecture():
    #Move to mission model
    await DRIVE_BASE.straight(-5)
    await DRIVE_BASE.straight(80)
    await DRIVE_BASE.turn(70)
    await LEFT_ATTACHMENT.run_until_stalled(200)
    await DRIVE_BASE.straight(420)
    await LEFT_ATTACHMENT.run_angle(300, -117)
    await DRIVE_BASE.straight(100)
    await DRIVE_BASE.turn(-12)
    await LEFT_ATTACHMENT.run_angle(200, -20)
    await wait(100)
    await LEFT_ATTACHMENT.run_angle(200, 32)
    await wait(600)
    await DRIVE_BASE.turn(15)
    await DRIVE_BASE.straight(290)
    await DRIVE_BASE.turn(-33)
    await RIGHT_ATTACHMENT.run_angle(400, -100)
    await DRIVE_BASE.straight(95)
    await RIGHT_ATTACHMENT.run_angle(300, 80)
    await LEFT_ATTACHMENT.run_angle(100, 30)
    await DRIVE_BASE.turn(75)
    await DRIVE_BASE.straight(630)


async def mission():
    await DRIVE_BASE.straight(-10)
    await LEFT_ATTACHMENT.run_until_stalled(70)
    await DRIVE_BASE.straight(400)
    await wait(200)
    await LEFT_ATTACHMENT.run_angle(400, -120)
    await DRIVE_BASE.straight(200)
    #Flick Humungous Fungus
    await LEFT_ATTACHMENT.run_angle(900, 100)
    await DRIVE_BASE.straight(85)
    await DRIVE_BASE.turn(90)
    await multitask(
        DRIVE_BASE.straight(-150),
        LEFT_ATTACHMENT.run_until_stalled(400)
    )
    await LEFT_ATTACHMENT.run_until_stalled(-400)
    await multitask(
        DRIVE_BASE.straight(70),
        LEFT_ATTACHMENT.run_angle(400, -10)
    )
    #Lift Cane
    await LEFT_ATTACHMENT.run_angle(400, 100)
    await DRIVE_BASE.straight(-80)
    await DRIVE_BASE.turn(-45)
    await DRIVE_BASE.straight(220)
    #Dump Keystone Species
    await DRIVE_BASE.straight(-70)
    await RIGHT_ATTACHMENT.run_angle(860, -220)
    #Return home
    await DRIVE_BASE.straight(-140)
    await DRIVE_BASE.turn(-60)
    await LEFT_ATTACHMENT.run_angle(200, 60)
    await DRIVE_BASE.straight(-670)


# Hub menu

ACTIVE_PROGRAM = 0
PROGRAM_LIST = list()
last_button = None
current_button = None

class RobotProgram(object):
    """ A class that holds our RobotPrograms. RobotPrograms have a method
    that is called when a program is launched. Also has as single character that,
    if the robot has a display, will be displayed as well as a color attribute
    that will change the color of the light on the hub. This is used to match the
    color of attachments to the color of the program and provides an additional
    cue to ensure the correct attachements are placed on the robot"""
    def __init__(
        self,
        func:callable,
        character:chr = "E",
        light_color:Color = Color.BLUE):

        self.label:chr = character
        self.color:Color = light_color 
        self.function:callable = func

async def next_program():
    """Selects the next Program"""
    global ACTIVE_PROGRAM
    if ACTIVE_PROGRAM != (len(PROGRAM_LIST) - 1):
        ACTIVE_PROGRAM += 1

async def prior_program():
    """Selects the prior program"""
    global ACTIVE_PROGRAM
    if ACTIVE_PROGRAM != 0:
        ACTIVE_PROGRAM -= 1

async def add_program(func:callable, char:chr = "E", color:Color = Color.BLUE):
    """ Adds a RobotProgram object to the PROGRAM_LIST"""
    PROGRAM_LIST.append(RobotProgram(func, char, color))

async def update_display():
    """Updates the Hub display with the character and button color"""
    current_program = PROGRAM_LIST[ACTIVE_PROGRAM]
    HUB.display.char(current_program.label)
    HUB.light.on(current_program.color)

async def start():
    global last_button, current_button
    HUB.system.set_stop_button(Button.BLUETOOTH)
    await initialize_robot()

    # Main loop/interface that allows for selecting and launching programs
    while True:
        buttons = HUB.buttons.pressed()
        
        # Check to see if the gyro is ready, if not display E/red button
        if HUB.imu.ready():
            # Display the active program/color
            await update_display()

            #only assign current button press once. else ignore.
            current_button = None
            if (len(buttons) == 1):
                current_button = buttons.pop()
            else:
                current_button = None

            if (last_button is None and current_button is None):
                await wait(100)
                continue
            elif (last_button == current_button):
                await wait(100)
                continue
            elif (last_button is None):
                last_button = current_button
                continue
            elif (current_button is None):
                current_button = last_button
                last_button = None
        
            # Check Buttons
            if current_button == Button.LEFT:
                # The left side button goes back to the previous program
                await prior_program()
                await update_display()
            elif Button.RIGHT == current_button:
                # The right side  button advances to the next program
                await next_program()
                await update_display()
            elif Button.CENTER == current_button:
                # The center button launches the currently selected program
                prepare_mission()
                await PROGRAM_LIST[ACTIVE_PROGRAM].function()
            else:
                await wait(10)
        else:
            # If Hub is not ready display an E for Error and wait until hub is ready
            # Place on flat surface to calibrate gyro/remove error state
            HUB.light.on(Color.RED)
            HUB.display.char('E')
            await wait(10)


# Entry point

async def main():
    try:
        await print_drivebase_settings()
        await add_program(cage, 'C', Color.RED)
        await add_program(tree, 'T', Color.YELLOW)
        await add_program(drone, 'D', Color.MAGENTA)
        await add_program(rock, 'R', Color.MAGENTA)
        await add_program(bioarchitecture, 'B', Color.CYAN)
        await add_program(mission, 'K', Color.MAGENTA)
        await start()
    except Exception as e:
        print(f'An error occurred: {e}')


run_task(main())
