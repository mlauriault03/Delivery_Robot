# Concept Validation Demo
# Matthew Lauriault
# 4/24/26


# PUBLIC LIBRARIES
import time

# PRIVATE LIBRARIES
from roboclaw_python.roboclaw_3 import Roboclaw
from drive_control import *


# TEST PROCEDURES

def test_speed(rpm1: int, rpm2: int) -> None:
    d = DriveController(PORT1, BAUDRATE, ADDRESS1)
    try:
        d.setSpeedM1(rpm1)
        print("Stop test by pressing Ctrl+C")
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        d.stop()

def test_position(angle_deg1: float, angle_deg2: float) -> None:
    d = DriveController(PORT1, BAUDRATE, ADDRESS1)
    try:
        d.moveToPositions(angle_deg1, angle_deg2)
        print("Stop test by pressing Ctrl+C")
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        d.stop()


# DEMO PROCEDURE

def demo() -> None:
    # Speed tests:
    # 1. Both at 100 RPM
    test_speed(100, 100)
    # # 2. Both at 150 RPM
    # test_speed(150, 150)
    # # 3. Left at 100 RPM, right at -100 RPM
    # test_speed(100, -100)
    # # 4. Left at -100 RPM, right at 100 RPM
    # test_speed(-100, 100)
    # # 5. Left at 150 RPM, right at 100 RPM
    # test_speed(150, 100)
    # # 6. Left at 100 RPM, right at 150 RPM
    # test_speed(100, 150)

    # # Position tests:
    # # 1. Both 360°
    # test_position(360, 360)
    # # 2. Both 540°
    # test_position(540, 540)
    # # 3. Left 180°, right -180°
    # test_position(180, -180)
    # # 4. Left -180°, right 180°
    # test_position(-180, 180)
    # # 5. Left 360°, right 180°
    # test_position(360, 180)
    # # 6. Left 180°, right 360°
    # test_position(180, 360)



# If this file is run as a script
if __name__ == "__main__":
    demo()

