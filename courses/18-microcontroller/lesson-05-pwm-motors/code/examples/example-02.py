#!/usr/bin/env python3
"""
Example 02: Servo Angle to PWM Pulse Width Mapping
This script demonstrates the relationship between servo angles and PWM pulse widths,
including calculations for standard servo control.
"""

import numpy as np
import matplotlib.pyplot as plt

class ServoPWMCalculator:
    """Class to handle servo angle to PWM pulse width conversions."""

    def __init__(self, min_pulse=1000, max_pulse=2000, min_angle=0, max_angle=180):
        """
        Initialize servo PWM calculator.

        Args:
            min_pulse (int): Minimum pulse width in microseconds (typically 1000μs for 0°)
            max_pulse (int): Maximum pulse width in microseconds (typically 2000μs for 180°)
            min_angle (int): Minimum angle in degrees
            max_angle (int): Maximum angle in degrees
        """
        self.min_pulse = min_pulse
        self.max_pulse = max_pulse
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.frequency = 50  # Standard servo frequency: 50Hz (20ms period)
        self.period_us = 1000000 / self.frequency  # Period in microseconds

    def angle_to_pulse_width(self, angle):
        """
        Convert servo angle to PWM pulse width.

        Args:
            angle (float): Servo angle in degrees

        Returns:
            float: Pulse width in microseconds
        """
        # Clamp angle to valid range
        angle = max(self.min_angle, min(self.max_angle, angle))

        # Linear interpolation between min and max pulse widths
        pulse_width = self.min_pulse + (angle - self.min_angle) * \
                     (self.max_pulse - self.min_pulse) / (self.max_angle - self.min_angle)

        return pulse_width

    def pulse_width_to_angle(self, pulse_width):
        """
        Convert PWM pulse width to servo angle.

        Args:
            pulse_width (float): Pulse width in microseconds

        Returns:
            float: Servo angle in degrees
        """
        # Clamp pulse width to valid range
        pulse_width = max(self.min_pulse, min(self.max_pulse, pulse_width))

        # Reverse linear interpolation
        angle = self.min_angle + (pulse_width - self.min_pulse) * \
               (self.max_angle - self.min_angle) / (self.max_pulse - self.min_pulse)

        return angle

    def calculate_duty_cycle(self, pulse_width):
        """
        Calculate duty cycle percentage for given pulse width.

        Args:
            pulse_width (float): Pulse width in microseconds

        Returns:
            float: Duty cycle as percentage (0-100)
        """
        duty_cycle = (pulse_width / self.period_us) * 100
        return duty_cycle

    def get_pwm_parameters(self, angle):
        """
        Get complete PWM parameters for a given angle.

        Args:
            angle (float): Servo angle in degrees

        Returns:
            dict: Dictionary containing pulse_width, duty_cycle, and period
        """
        pulse_width = self.angle_to_pulse_width(angle)
        duty_cycle = self.calculate_duty_cycle(pulse_width)

        return {
            'angle': angle,
            'pulse_width_us': pulse_width,
            'duty_cycle_percent': duty_cycle,
            'period_us': self.period_us,
            'frequency_hz': self.frequency
        }

def visualize_servo_pwm_mapping():
    """Visualize the relationship between servo angles and PWM parameters."""
    calculator = ServoPWMCalculator()

    # Generate data for full range of angles
    angles = np.linspace(0, 180, 181)
    pulse_widths = []
    duty_cycles = []

    for angle in angles:
        params = calculator.get_pwm_parameters(angle)
        pulse_widths.append(params['pulse_width_us'])
        duty_cycles.append(params['duty_cycle_percent'])

    # Create plots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # Plot 1: Angle vs Pulse Width
    ax1.plot(angles, pulse_widths, 'b-', linewidth=2)
    ax1.set_title('Servo Angle vs PWM Pulse Width')
    ax1.set_xlabel('Angle (degrees)')
    ax1.set_ylabel('Pulse Width (μs)')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 180)
    ax1.set_ylim(900, 2100)

    # Add reference lines
    ax1.axhline(y=1000, color='r', linestyle='--', alpha=0.7, label='1000μs (0°)')
    ax1.axhline(y=1500, color='g', linestyle='--', alpha=0.7, label='1500μs (90°)')
    ax1.axhline(y=2000, color='orange', linestyle='--', alpha=0.7, label='2000μs (180°)')
    ax1.legend()

    # Plot 2: Angle vs Duty Cycle
    ax2.plot(angles, duty_cycles, 'm-', linewidth=2)
    ax2.set_title('Servo Angle vs PWM Duty Cycle')
    ax2.set_xlabel('Angle (degrees)')
    ax2.set_ylabel('Duty Cycle (%)')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 180)
    ax2.set_ylim(4, 11)

    plt.tight_layout()
    plt.show()

def main():
    """Main function to demonstrate servo PWM calculations."""
    print("Servo Angle to PWM Pulse Width Mapping")
    print("=" * 40)

    # Create calculator with standard servo parameters
    calculator = ServoPWMCalculator()

    # Test common angles
    test_angles = [0, 45, 90, 135, 180]

    print(f"Servo Frequency: {calculator.frequency} Hz")
    print(f"PWM Period: {calculator.period_us} μs")
    print("-" * 60)

    for angle in test_angles:
        params = calculator.get_pwm_parameters(angle)
        print(f"Angle: {params['angle']:3.0f}° | "
              f"Pulse: {params['pulse_width_us']:4.0f}μs | "
              f"Duty: {params['duty_cycle_percent']:5.2f}%")

    print("\nKey Points:")
    print("- Standard servo uses 50Hz PWM (20ms period)")
    print("- 1000μs pulse = 0° (minimum angle)")
    print("- 1500μs pulse = 90° (center position)")
    print("- 2000μs pulse = 180° (maximum angle)")
    print("- Duty cycle ranges from ~5% to ~10%")

    # Interactive calculation
    print("\nTry your own angle:")
    try:
        user_angle = float(input("Enter angle (0-180): "))
        params = calculator.get_pwm_parameters(user_angle)
        print(f"\nFor {params['angle']:.1f}°:")
        print(f"  Pulse Width: {params['pulse_width_us']:.1f} μs")
        print(f"  Duty Cycle: {params['duty_cycle_percent']:.2f}%")
        print(f"  High Time: {params['pulse_width_us']/1000:.3f} ms")
        print(f"  Low Time: {(params['period_us'] - params['pulse_width_us'])/1000:.3f} ms")
    except (ValueError, EOFError):
        print("Skipping interactive input.")

    # Show visualization
    visualize_servo_pwm_mapping()

if __name__ == "__main__":
    main()