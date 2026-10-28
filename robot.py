from pybricks.parameters import Color
from pybricks.tools import run_task

from Cage import cage
from Tree import tree
from Rock import rock
from KeyAndCane import mission
from Drone import drone
from BigBuilding import bioarchitecture
from text_library import print_drivebase_settings
from hub_control import add_program, start


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
