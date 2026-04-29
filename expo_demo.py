# Expo Demo
# Matthew Lauriault
# 4/28/26


# PUBLIC LIBRARIES
import time

# PRIVATE LIBRARIES
from drive_control import *

# TEST PARAMETERS
SPEED_INC = 50  # RPM
POS_INC = 90    # degrees
POS = [0, -45, 45, -90, 90, -135, 135, -180, -360-45, 360+45, -360-90, 360+90, -360-135, 360+135, -540]
D0 = 0.7    # delay offset
D1 = 0.003  # delay gain per position angle difference


# PROCEDURES

def align_shaft_M2(d: DriveController) -> None:
    print("\nAligning M2 shaft...")
    speed = int(input("Press Enter to skip alignment. Otherwise, enter speed in RPM to turn M2: ") or 0)
    while speed:
        input(f"Press Enter to start turning M2 at {speed} RPM.")
        d.setSpeedM2(speed)  # Slow speed to allow for alignment
        input("Press Enter when white strip on outputf shaft is on top...")
        d.stop()
        speed = int(input("Press Enter if aligned. Otherwise, enter speed to use next: ") or 0)
    print("M2 shaft aligned.")


# DEMO PROCEDURE

def demo() -> None:
    d = DriveController(PORT1, BAUDRATE, ADDRESS1)
    print("Press Ctrl+C at any time to stop demo.")
    speedM1_dir = 1 # 1 = toward +, -1 = toward -
    speedM1 = 20
    i = 0
    posM2 = POS[i] # 0°
    try:
        # Align M2 shaft for position demo + reset its encoders
        align_shaft_M2(d)
        print("Resetting encoders...")
        d.resetEncoders()
        # Forever loop
        while True:
            # Update index of M2 position list
            if i >= (len(POS) - 1):
                i = 0
            else:
                i += 1
            # Calculate delay based on position difference
            pos_diff = abs(POS[i] - posM2)
            delay = round(D0 + D1*pos_diff , 3)
            print(f"Pos diff: {pos_diff}° \tdelay: {delay}s") # debugging info
            # Update current M2 position
            posM2 = POS[i]
            # Set M2 position
            d.moveToPosM2(posM2)
            # Update speed
            if i % 2 == 0:
                # Update current M1 speed
                if (abs(speedM1) + abs(SPEED_INC)) > MAX_RPM:
                    speedM1_dir *= -1 # toggle
                speedM1 += (SPEED_INC * speedM1_dir)
                # Set M1 speed
                d.setSpeedM1(speedM1)
            # Wait for M2 to change position
            time.sleep(delay)
    except KeyboardInterrupt:
        print("\nStopping Demo...")
    except Exception as e:
        print(f"\nError during demo: {e}")
    finally:
        d.stop()



# If this file is run as a script
if __name__ == "__main__":
    demo()