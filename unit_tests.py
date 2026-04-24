# Unit tests for RoboClaw motor controller functionality
# Matthew Lauriault
# 4/20/26


# PUBLIC LIBRARIES
import time

# PRIVATE LIBRARIES
from roboclaw_python.roboclaw_3 import Roboclaw

# CONSTANTS
ENC_PPR = 751.8  # pulses (increments) per revolution at the output shaft

# PARAMETERS - ROBOCLAWS
PORT = "COM10"
BAUDRATE = 115200
ADDRESS = 0x80   # 0x80 = 128 in decimal

# PARAMETERS - DRIVE MOTORS
ACCEL = 2000    # PPS^2
DECCEL = 2000   # PPS^2
MAX_RPM = 200   # (2506 PPS) True max is 223 RPM, but limit to 200 for safety


# HELPER FUNCTIONS

def rpm_to_pps(rpm: float) -> int:
    """Convert RPM to pulses per second (PPS) for RoboClaw commands"""
    if abs(rpm) > MAX_RPM:
        raise ValueError(f"RPM must be between -{MAX_RPM} and {MAX_RPM}")
    pps = int((rpm / 60) * ENC_PPR)
    return pps

def angle_to_pulses(angle_deg: float) -> int:
    """Convert an angle in degrees to encoder pulses"""
    pulses = int((angle_deg / 360) * ENC_PPR)
    return pulses


def stop_motors(rc: Roboclaw) -> None:
    rc.ForwardBackwardM1(ADDRESS, 64)  # 64 = stop
    rc.ForwardBackwardM2(ADDRESS, 64)  # 64 = stop

def reset_encoders() -> None:
    rc = Roboclaw(comport=PORT, rate=BAUDRATE)
    rc.Open()
    rc.ResetEncoders(ADDRESS)


# TESTS

# Motor 1 Forward/Reverse Test
def testSpeed1():
    rc = Roboclaw(comport=PORT, rate=BAUDRATE)
    rc.Open()
    try:
        # Forward
        rc.ForwardBackwardM1(ADDRESS, 80)   # 64 = stop, >64 forward
        time.sleep(5)

        # Stop
        stop_motors(rc)
        time.sleep(1)

        # Reverse
        rc.ForwardBackwardM1(ADDRESS, 48)   # <64 reverse
        time.sleep(5)

        # Stop
        stop_motors(rc)
        time.sleep(1)

    finally:
        rc.ForwardBackwardM1(ADDRESS, 64)

# Motor 1 Full Speed Test
def testSpeed2():
    rc = Roboclaw(comport=PORT, rate=BAUDRATE)
    rc.Open()
    try:
        # Forward
        rc.ForwardBackwardM1(ADDRESS, 127)   # 64 = stop, >64 forward
        time.sleep(5)

        # Stop
        stop_motors(rc)
        time.sleep(1)

    finally:
        rc.ForwardBackwardM1(ADDRESS, 64)


# Motor 1 Speed Control Test
def testSpeed3():
    rc = Roboclaw(comport=PORT, rate=BAUDRATE)
    rc.Open()
    try:
        rpm = 100
        pps = rpm_to_pps(rpm)
        print(f"Setting speed to {rpm} RPM, which is {pps} PPS")
        rc.SpeedM1(ADDRESS, pps)

        time.sleep(20)

    finally:
        print("Stopping...")
        stop_motors(rc)

# Encoder 1 Test
def testEncoders():
    rc = Roboclaw(comport=PORT, rate=BAUDRATE)
    rc.Open()
    try:
        # Reset Encoders
        rc.ResetEncoders(ADDRESS)
        time.sleep(1)

        # Move to position 1000
        rc.ForwardBackwardM1(ADDRESS, 100)
        
        # Read encoder value until it reaches target count
        enc1_val = 0
        while enc1_val < 1000:
            enc1_val = rc.ReadEncM1(ADDRESS)[1]
            print(f"Encoder 1 value: {enc1_val}")
            time.sleep(0.5)
    
        stop_motors(rc)

    finally:
        stop_motors(rc)

# Motor 1 Distance Control Test
def testDistance():
    rc = Roboclaw(comport=PORT, rate=BAUDRATE)
    rc.Open()
    try:
        # Reset Encoders
        rc.ResetEncoders(ADDRESS)
        time.sleep(1)

        # Read encoder value before movement
        enc1 = rc.ReadEncM1(ADDRESS)
        print(f"Encoder: {enc1}")

        # Move forward by <distance> counts at <speed>
        speed=1000
        distance=3000
        buffer=1
        print(f"Moving forward {distance} counts at speed {speed}...")
        result = rc.SpeedDistanceM1(ADDRESS, speed, distance, buffer)
        print(f"Command result: {result}")

        time.sleep(2)

        # Read encoder value after movement
        enc1 = rc.ReadEncM1(ADDRESS)
        print(f"Encoder: {enc1}")

    finally:
        print("Stopping...")
        stop_motors(rc)

# Motor 1 Position Control Test
def testPosition():
    rc = Roboclaw(comport=PORT, rate=BAUDRATE)
    rc.Open()
    try:
        # Reset Encoders
        rc.ResetEncoders(ADDRESS)
        time.sleep(1)

        # Read encoder value before movement
        enc1 = rc.ReadEncM1(ADDRESS)
        print(f"Encoder: {enc1}")

        # Rotate 1 revolution forward
        rc.SpeedAccelDeccelPositionM1(
            ADDRESS,
            accel=ACCEL,
            deccel=DECCEL,
            speed=rpm_to_pps(150),
            position=int(ENC_PPR),
            buffer=1
        )
        time.sleep(5)

        # Rotate 1 revolution backward
        # rc.SpeedDistanceM1(ADDRESS, speed=5000, distance=-ENC_PPR, buffer=1)
        # time.sleep(5)

        # Read encoder value after movement
        enc1 = rc.ReadEncM1(ADDRESS)
        print(f"Encoder: {enc1}")

    finally:
        print("Stopping...")
        stop_motors(rc)

def testPort():
    rc = Roboclaw(comport=PORT, rate=BAUDRATE)
    rc.Open()
    print(f"Port: {rc.comport}")
    print(f"Type: {type(rc.comport)}")

def testReadEncoders():
    rc = Roboclaw(comport=PORT, rate=BAUDRATE)
    rc.Open()
    enc1 = rc.ReadEncM1(ADDRESS)
    print(f"Encoder: {enc1}")



# If this file is run as a script
if __name__ == "__main__":
    # testSpeed3()
    # testEncoders()
    # testDistance()
    # testPosition()
    # reset_encoders()
    # testPort()
    testReadEncoders()
