from prelude import *

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
