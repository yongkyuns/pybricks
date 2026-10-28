from prelude import *

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
