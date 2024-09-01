import numpy as np

class TirePressureMonitor:
    def __init__(self, base_wheel_speeds, base_pressure_psi):
        """
        Initialize the tire pressure monitor with baseline data.
        
        :param base_wheel_speeds: Dictionary with baseline wheel speeds (RPM) for each tire.
                                  Example: {'FL': 500, 'FR': 500, 'RL': 500, 'RR': 500}
        :param base_pressure_psi: Baseline tire pressure (PSI).
        """
        self.base_wheel_speeds = base_wheel_speeds
        self.base_pressure_psi = base_pressure_psi
        self.pressure_deviation_constant = -0.05  # Hypothetical constant for deviation

    def calculate_pressure(self, current_wheel_speeds):
        """
        Calculate the approximate tire pressure for each tire based on wheel speeds.
        
        :param current_wheel_speeds: Dictionary with current wheel speeds (RPM) for each tire.
                                     Example: {'FL': 495, 'FR': 500, 'RL': 502, 'RR': 499}
        :return: Dictionary with estimated tire pressures.
        """
        pressure_estimates = {}
        
        for tire, current_speed in current_wheel_speeds.items():
            base_speed = self.base_wheel_speeds[tire]
            speed_deviation = current_speed - base_speed
            pressure_change = speed_deviation * self.pressure_deviation_constant
            pressure_estimates[tire] = self.base_pressure_psi + pressure_change
        
        return pressure_estimates

    def detect_pressure_loss(self, pressure_estimates, threshold_psi=2.0):
        """
        Detect any tire that is losing pressure by comparing pressure estimates to the average.
        
        :param pressure_estimates: Dictionary with estimated tire pressures.
                                   Example: {'FL': 30.5, 'FR': 32.0, 'RL': 31.8, 'RR': 32.1}
        :param threshold_psi: The PSI difference threshold to trigger a warning for pressure loss.
        :return: List of tires with potential pressure loss.
        """
        average_pressure = np.mean(list(pressure_estimates.values()))
        low_pressure_tires = []
        
        for tire, pressure in pressure_estimates.items():
            if (average_pressure - pressure) > threshold_psi:
                low_pressure_tires.append(tire)
        
        return low_pressure_tires


# Example usage
if __name__ == "__main__":
    # Baseline values when all tires are properly inflated
    base_wheel_speeds = {'FL': 500, 'FR': 500, 'RL': 500, 'RR': 500}
    base_pressure_psi = 32  # Baseline pressure in PSI
    
    monitor = TirePressureMonitor(base_wheel_speeds, base_pressure_psi)
    
    # Current wheel speeds from CAN data
    current_wheel_speeds = {'FL': 495, 'FR': 500, 'RL': 502, 'RR': 499}
    
    # Calculate the estimated tire pressures
    pressure_estimates = monitor.calculate_pressure(current_wheel_speeds)
    print("Estimated Tire Pressures:", pressure_estimates)
    
    # Detect tires with significant pressure loss
    low_pressure_tires = monitor.detect_pressure_loss(pressure_estimates)
    if low_pressure_tires:
        print("Tires with potential pressure loss:", low_pressure_tires)
    else:
        print("No significant pressure loss detected.")
