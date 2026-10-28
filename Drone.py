from prelude import *

async def drone():
    await drive_with_speed(180, 630)
    await DRIVE_BASE.turn(-45)
    await DRIVE_BASE.turn(45)
    await DRIVE_BASE.straight(-620)
