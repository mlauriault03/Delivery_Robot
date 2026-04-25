# Drive Control Library
# Matthew Lauriault
# 4/23/26


# PUBLIC LIBRARIES
import time

# PRIVATE LIBRARIES
from roboclaw_python.roboclaw_3 import Roboclaw

# CONSTANTS
ENC_PPR = 751.8     # pulses (increments) per revolution at the output shaft

# PARAMETERS - ROBOCLAWS
BAUDRATE = 115200
PORT1 = "COM10"
PORT2 = ""
PORT3 = ""
ADDRESS1 = 0x80     # 0x80 = 128 in decimal
ADDRESS2 = 0x81
ADDRESS3 = 0x82

# PARAMETERS - DRIVE MOTORS
ACCEL = 2000        # PPS^2
DECCEL = 2000       # PPS^2
DEFAULT_RPM = 150   # (1879.5 PPS)
MAX_RPM = 200       # (2506 PPS) True max is 223 RPM, but limit to 200 for safety


# CONVERSIONS

def rpm_to_pps(rpm: float) -> int:
    """Convert RPM to pulses per second (PPS)"""
    if abs(rpm) > MAX_RPM:
        raise ValueError(f"RPM must be between -{MAX_RPM} and {MAX_RPM}")
    pps = int((rpm / 60) * ENC_PPR)
    return pps

def angle_to_pulses(angle_deg: float) -> int:
    """Convert an angle in degrees to encoder pulses"""
    pulses = int((angle_deg / 360) * ENC_PPR)
    return pulses


# CONTROLLER CLASS

class DriveController:

    def __init__(self, port: str, baudrate: int, address: int):
        self.port = port
        self.baudrate = baudrate
        self.address = address
        self.encM1 = 0
        self.encM2 = 0
        self.rc = Roboclaw(comport=port, rate=baudrate)
        self.rc.Open()

    # CONFIG SETTINGS
    # TODO: copy from Motion Studio
    # TODO: make function to set those parameters all at once to make it easy for the user

    # SPEED CONTROL
    
    def stop(self) -> None:
        self.rc.ForwardBackwardM1(self.address, 64)  # 64 = stop
        self.rc.ForwardBackwardM2(self.address, 64)  # 64 = stop

    def setSpeedM1(self, rpm: float) -> None:
        pps = rpm_to_pps(rpm)
        print(f"Setting speed to {rpm} RPM ({pps} PPS)")
        self.rc.SpeedM1(self.address, pps)

    def setSpeedM2(self, rpm: float) -> None:
        pps = rpm_to_pps(rpm)
        print(f"Setting speed to {rpm} RPM ({pps} PPS)")
        self.rc.SpeedM2(self.address, pps)

    def setSpeeds(self, rpm1: float, rpm2: float) -> None:
        pps1 = rpm_to_pps(rpm1)
        pps2 = rpm_to_pps(rpm2)
        print(f"Setting speed 1 to {rpm1} RPM ({pps1} PPS) and speed 2 to {rpm2} RPM ({pps2} PPS)")
        self.rc.SpeedM1M2(self.address, pps1, pps2)

    # POSITION CONTROL

    def moveToPosM1(self, angle_deg: float, rpm: float = DEFAULT_RPM) -> None:
        pulses = angle_to_pulses(angle_deg)
        pps = rpm_to_pps(rpm)
        print(f"Moving M1 to {angle_deg}° ({pulses} P) at {rpm} RPM ({pps} PPS)")
        self.rc.SpeedAccelDeccelPositionM1(self.address, ACCEL, pps, DECCEL, pulses, 1)

    def moveToPosM2(self, angle_deg: float, rpm: float = DEFAULT_RPM) -> None:
        pulses = angle_to_pulses(angle_deg)
        pps = rpm_to_pps(rpm)
        print(f"Moving M2 to {angle_deg}° ({pulses} P) at {rpm} RPM ({pps} PPS)")
        self.rc.SpeedAccelDeccelPositionM2(self.address, ACCEL, pps, DECCEL, pulses, 1)
    
    def moveToPositions(self, angle_deg1: float, angle_deg2: float, rpm1: float = DEFAULT_RPM, rpm2: float = DEFAULT_RPM) -> None:
        pulses1 = angle_to_pulses(angle_deg1)
        pulses2 = angle_to_pulses(angle_deg2)
        pps1 = rpm_to_pps(rpm1)
        pps2 = rpm_to_pps(rpm2)
        print(f"Moving M1 to {angle_deg1}° ({pulses1} P) at {rpm1} RPM ({pps1} PPS) and M2 to {angle_deg2}° ({pulses2} P) at {rpm2} RPM ({pps2} PPS)")
        self.rc.SpeedAccelDeccelPositionM1M2(self.address, ACCEL, pps1, DECCEL, pulses1, ACCEL, pps2, DECCEL, pulses2, 1)

    # ENCODERS

    def updateEncM1(self):
        self.encM1 = self.rc.ReadEncM1(self.address)
        print(f"Encoder M1: {self.encM1}")

    def updateEncM2(self):
        self.encM2 = self.rc.ReadEncM2(self.address)
        print(f"Encoder M2: {self.encM2}")

    def updateEncoders(self):
        self.updateEncM1()
        self.updateEncM2()

    def setEncM1(self, pulses: int) -> None:
        self.encM1 = pulses
        self.rc.SetEncM1(self.address, pulses)

    def setEncM2(self, pulses: int) -> None:
        self.encM2 = pulses
        self.rc.SetEncM2(self.address, pulses)

    def resetEncoders(self) -> None:
        self.encM1 = 0
        self.encM2 = 0
        self.rc.ResetEncoders(self.address)