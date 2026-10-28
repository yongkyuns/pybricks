from prelude import *

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
