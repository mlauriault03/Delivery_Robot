# Concept Validation Demo
# Matthew Lauriault
# 4/24/26


# PUBLIC LIBRARIES
import time

# PRIVATE LIBRARIES
from drive_control import *


# TEST PROCEDURES

def test_speed(d: DriveController, rpm1: int, rpm2: int) -> None:
    input(f"\nSpeed Test: M1 = {rpm1} RPM, M2 = {rpm2} RPM. Press Enter to start...")
    d.setSpeeds(rpm1, rpm2)
    input("Press Enter to stop...")
    d.stop()
    print("Test complete.")

def test_position(d: DriveController, angle_deg1: float, angle_deg2: float) -> None:
    input(f"\nPosition Test: M1 = {angle_deg1}°, M2 = {angle_deg2}°. Press Enter to start...")
    d.moveToPositions(angle_deg1, angle_deg2)
    input("Press Enter to reset...")
    d.moveToPositions(0, 0)
    print("Test complete.")

def align_shaft_M1(d: DriveController) -> None:
    print("\nAligning M1 shaft...")
    speed = 20
    while speed:
        input(f"Press Enter to start turning M1 at {speed} RPM.")
        d.setSpeedM1(speed)  # Slow speed to allow for alignment
        input("Press Enter when white strip on output shaft is on top...")
        d.stop()
        speed = int(input("Press Enter if aligned. Otherwise, enter speed to use next: ") or 0)
    print("M1 shaft aligned.")

def align_shaft_M2(d: DriveController) -> None:
    print("\nAligning M2 shaft...")
    speed = 20
    while speed:
        input(f"Press Enter to start turning M2 at {speed} RPM.")
        d.setSpeedM2(speed)  # Slow speed to allow for alignment
        input("Press Enter when white strip on output shaft is on top...")
        d.stop()
        speed = int(input("Press Enter if aligned. Otherwise, enter speed to use next: ") or 0)
    print("M2 shaft aligned.")


# DEMO PROCEDURE

def demo() -> None:
    d = DriveController(PORT1, BAUDRATE, ADDRESS1)
    print("Press Ctrl+C at any time to stop demo.")
    try:
        # Speed tests:
        # 1. Both at 100 RPM
        test_speed(d, 100, 100)
        # # 2. Both at 150 RPM
        test_speed(d, 150, 150)
        # # 3. Left at 100 RPM, right at -100 RPM
        test_speed(d, 100, -100)
        # # 4. Left at -100 RPM, right at 100 RPM
        test_speed(d, -100, 100)
        # # 5. Left at 150 RPM, right at 100 RPM
        test_speed(d, 150, 100)
        # # 6. Left at 100 RPM, right at 150 RPM
        test_speed(d, 100, 150)

        # # Align shafts for position tests
        align_shaft_M1(d)
        align_shaft_M2(d)
        # Reset encoders before position tests
        print("Resetting encoders...")
        d.resetEncoders()
        
        # Position tests:
        # 1. Both at 360°
        test_position(d, 360, 360)
        # 2. Both at 720°
        test_position(d, 720, 720)
        # 3. Left at 90°, right at -90°
        test_position(d, 90, -90)
        # 4. Left at -90°, right at 90°
        test_position(d, -90, 90)
        # 5. Left at 45°, right at 135°
        test_position(d, 45, 135)
        # 6. Left at 135°, right at 45°
        test_position(d, 135, 45)

        # Wait for last test to complete 
        input("\nAll tests complete. Press Enter to finish demo...")
        print("\nDemo complete.")
    except KeyboardInterrupt:
        print("\nStopping Demo...")
    except Exception as e:
        print(f"\nError during demo: {e}")
    finally:
        d.stop()



# If this file is run as a script
if __name__ == "__main__":
    demo()