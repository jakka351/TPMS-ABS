#!/usr/bin/python3
# -*- coding: utf-8 -*-
#import can
import time
import os
import queue
from threading import Thread
import sys, traceback
import random  # Added for simulation
###############################################
# Constants
SteeringAngleSensorId = 0x90
AntiLockBrakingSystemId = 0x4B0
PSI_MAX = 38.0
PSI_MIN = 0.0
deviation_threshold = 0.05  # Threshold for detecting significant speed deviation
###############################################
# Global variables
q = queue.Queue()
bus = None
message = None
###############################################
# Simulated wheel speeds for testing
def simulate_wheel_speeds():
    # Normal speed for 3 wheels and slightly deflated speed for 1 wheel
    FrontLeftSpeed = random.uniform(50.0, 52.0)  # Normal speed
    FrontRightSpeed = random.uniform(50.0, 52.0)  # Normal speed
    RearLeftSpeed = random.uniform(50.0, 52.0)  # Normal speed
    RearRightSpeed = random.uniform(47.0, 49.0)  # Simulating a deflating tire
    return FrontLeftSpeed, FrontRightSpeed, RearLeftSpeed, RearRightSpeed
###############################################
# Function to calculate tire pressure based on wheel speed variance
def calculate_relative_tyre_pressure(FrontLeftSpeed, FrontRightSpeed, RearLeftSpeed, RearRightSpeed):
    # Calculate the average speed of all four wheels
    average_speed = (FrontLeftSpeed + FrontRightSpeed + RearLeftSpeed + RearRightSpeed) / 4.0
    # Initialize tire pressures
    FrontLeftTyrePressure = calculate_pressure_from_speed_variance(FrontLeftSpeed, average_speed)
    FrontRightTyrePressure = calculate_pressure_from_speed_variance(FrontRightSpeed, average_speed)
    RearLeftTyrePressure = calculate_pressure_from_speed_variance(RearLeftSpeed, average_speed)
    RearRightTyrePressure = calculate_pressure_from_speed_variance(RearRightSpeed, average_speed)
    # Print the results
    print(f"Front Left Tyre Pressure: {FrontLeftTyrePressure:.2f} PSI")
    print(f"Front Right Tyre Pressure: {FrontRightTyrePressure:.2f} PSI")
    print(f"Rear Left Tyre Pressure: {RearLeftTyrePressure:.2f} PSI")
    print(f"Rear Right Tyre Pressure: {RearRightTyrePressure:.2f} PSI")
###############################################
# Function to calculate PSI based on speed variance
def calculate_pressure_from_speed_variance(wheel_speed, average_speed):
    # Calculate the relative speed difference
    speed_diff_ratio = abs(wheel_speed - average_speed) / average_speed
    # If the variance exceeds the threshold, scale the pressure down
    if speed_diff_ratio > deviation_threshold:
        # Scale pressure between 0.0 (fully flat) and 1.0 (normal pressure)
        pressure_scale = max(1.0 - (speed_diff_ratio * 10), 0.0)
    else:
        pressure_scale = 1.0
    # Convert the pressure scale to PSI (38 PSI = fully inflated, 0 PSI = flat)
    psi = PSI_MAX * pressure_scale
    return psi
###############################################
# Simulated main loop for real-world testing
def main():
    global bus, message, q, SteeringAngleSensorId, AntiLockBrakingSystemId
    try:
        while True:
            # Simulate wheel speeds
            FrontLeftSpeed, FrontRightSpeed, RearLeftSpeed, RearRightSpeed = simulate_wheel_speeds()
            # Calculate relative tyre pressures based on wheel speeds
            calculate_relative_tyre_pressure(FrontLeftSpeed, FrontRightSpeed, RearLeftSpeed, RearRightSpeed)
            # Sleep for a moment to simulate real-time updates
            time.sleep(2)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception:
        traceback.print_exc(file=sys.stdout)
        sys.exit()
    except OSError:
        sys.exit()

############################
# TPMS-AntiLockBrakingSystemId
############################
if __name__ == "__main__":
    cleanscreen = lambda: os.system("clear")
    cleanscreen()
    main()
