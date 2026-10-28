from pybricks.parameters import Color, Button
from library import initialize_robot, prepare_mission
from robot_config import HUB
from pybricks.tools import wait

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
