#!/usr/bin/env python3
"""
Solution 02: Advanced Servo PWM Mapping with Calibration Support
Complete solution for servo angle to PWM pulse width conversion with calibration features.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Dict, Optional

class AdvancedServoPWMCalculator:
    """
    Advanced servo PWM calculator with calibration and multiple servo type support.
    """

    # Common servo specifications
    SERVO_TYPES = {
        'standard': {'min_pulse': 1000, 'max_pulse': 2000, 'min_angle': 0, 'max_angle': 180},
        'wide_angle': {'min_pulse': 500, 'max_pulse': 2500, 'min_angle': -90, 'max_angle': 270},
        'continuous': {'min_pulse': 1000, 'max_pulse': 2000, 'min_angle': -100, 'max_angle': 100},  # Speed control
        'micro': {'min_pulse': 900, 'max_pulse': 2100, 'min_angle': 0, 'max_angle': 180},
    }

    def __init__(self, servo_type: str = 'standard', custom_params: Optional[Dict] = None):
        """
        Initialize advanced servo PWM calculator.

        Args:
            servo_type (str): Type of servo ('standard', 'wide_angle', 'continuous', 'micro')
            custom_params (dict): Custom parameters to override defaults
        """
        if servo_type in self.SERVO_TYPES:
            params = self.SERVO_TYPES[servo_type].copy()
        else:
            raise ValueError(f"Unknown servo type: {servo_type}. "
                           f"Available types: {list(self.SERVO_TYPES.keys())}")

        if custom_params:
            params.update(custom_params)

        self.min_pulse = params['min_pulse']
        self.max_pulse = params['max_pulse']
        self.min_angle = params['min_angle']
        self.max_angle = params['max_angle']
        self.frequency = 50.0  # Standard servo frequency
        self.period_us = 1000000 / self.frequency
        self.servo_type = servo_type

        # Calibration offsets (can be adjusted based on actual servo measurements)
        self.pulse_offset = 0
        self.angle_offset = 0

    def set_calibration_offsets(self, pulse_offset: int = 0, angle_offset: float = 0.0):
        """Set calibration offsets for fine-tuning."""
        self.pulse_offset = pulse_offset
        self.angle_offset = angle_offset

    def angle_to_pulse_width(self, angle: float) -> float:
        """
        Convert servo angle to PWM pulse width with calibration.

        Args:
            angle (float): Servo angle in degrees

        Returns:
            float: Pulse width in microseconds
        """
        # Apply angle offset
        corrected_angle = angle + self.angle_offset

        # Clamp to valid range
        corrected_angle = max(self.min_angle, min(self.max_angle, corrected_angle))

        # Linear interpolation
        pulse_width = self.min_pulse + (corrected_angle - self.min_angle) * \
                     (self.max_pulse - self.min_pulse) / (self.max_angle - self.min_angle)

        # Apply pulse offset
        pulse_width += self.pulse_offset

        return pulse_width

    def pulse_width_to_angle(self, pulse_width: float) -> float:
        """
        Convert PWM pulse width to servo angle with calibration.

        Args:
            pulse_width (float): Pulse width in microseconds

        Returns:
            float: Servo angle in degrees
        """
        # Apply pulse offset correction
        corrected_pulse = pulse_width - self.pulse_offset

        # Clamp to valid range
        corrected_pulse = max(self.min_pulse, min(self.max_pulse, corrected_pulse))

        # Reverse linear interpolation
        angle = self.min_angle + (corrected_pulse - self.min_pulse) * \
               (self.max_angle - self.min_angle) / (self.max_pulse - self.min_pulse)

        # Apply angle offset correction
        angle -= self.angle_offset

        return angle

    def calculate_duty_cycle(self, pulse_width: float) -> float:
        """Calculate duty cycle percentage."""
        duty_cycle = (pulse_width / self.period_us) * 100
        return duty_cycle

    def get_pwm_parameters(self, angle: float) -> Dict:
        """Get complete PWM parameters for a given angle."""
        pulse_width = self.angle_to_pulse_width(angle)
        duty_cycle = self.calculate_duty_cycle(pulse_width)

        return {
            'angle': angle,
            'corrected_angle': angle + self.angle_offset,
            'pulse_width_us': pulse_width,
            'duty_cycle_percent': duty_cycle,
            'period_us': self.period_us,
            'frequency_hz': self.frequency,
            'servo_type': self.servo_type
        }

    def validate_servo_parameters(self, tolerance: float = 0.1) -> Dict:
        """
        Validate servo parameters by checking key reference points.

        Args:
            tolerance (float): Acceptable tolerance for validation

        Returns:
            dict: Validation results
        """
        results = {
            'center_point_valid': False,
            'range_valid': False,
            'duty_cycle_range_valid': False,
            'issues': []
        }

        # Check center point (90 degrees for standard servos)
        center_angle = (self.min_angle + self.max_angle) / 2
        center_params = self.get_pwm_parameters(center_angle)
        expected_center_pulse = (self.min_pulse + self.max_pulse) / 2

        if abs(center_params['pulse_width_us'] - expected_center_pulse) <= tolerance:
            results['center_point_valid'] = True
        else:
            results['issues'].append(f"Center point mismatch: "
                                   f"expected {expected_center_pulse:.1f}μs, "
                                   f"got {center_params['pulse_width_us']:.1f}μs")

        # Check range
        min_params = self.get_pwm_parameters(self.min_angle)
        max_params = self.get_pwm_parameters(self.max_angle)

        if (abs(min_params['pulse_width_us'] - (self.min_pulse + self.pulse_offset)) <= tolerance and
            abs(max_params['pulse_width_us'] - (self.max_pulse + self.pulse_offset)) <= tolerance):
            results['range_valid'] = True
        else:
            results['issues'].append("Range validation failed")

        # Check duty cycle range
        min_duty = min_params['duty_cycle_percent']
        max_duty = max_params['duty_cycle_percent']

        if 2.0 <= min_duty <= 15.0 and 2.0 <= max_duty <= 15.0:
            results['duty_cycle_range_valid'] = True
        else:
            results['issues'].append(f"Duty cycle out of typical range: "
                                   f"{min_duty:.2f}% to {max_duty:.2f}%")

        results['overall_valid'] = (results['center_point_valid'] and
                                  results['range_valid'] and
                                  results['duty_cycle_range_valid'])

        return results

def demonstrate_servo_types():
    """Demonstrate different servo types and their characteristics."""
    servo_types = ['standard', 'wide_angle', 'continuous', 'micro']

    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()

    for i, servo_type in enumerate(servo_types):
        calculator = AdvancedServoPWMCalculator(servo_type)

        # Generate data for full range
        angles = np.linspace(calculator.min_angle, calculator.max_angle, 100)
        pulse_widths = [calculator.angle_to_pulse_width(angle) for angle in angles]
        duty_cycles = [calculator.calculate_duty_cycle(pw) for pw in pulse_widths]

        # Plot pulse width vs angle
        axes[i].plot(angles, pulse_widths, 'b-', linewidth=2)
        axes[i].set_title(f'{servo_type.title()} Servo\n'
                         f'Range: {calculator.min_angle}° to {calculator.max_angle}°\n'
                         f'Pulse: {calculator.min_pulse}-{calculator.max_pulse}μs')
        axes[i].set_xlabel('Angle (degrees)')
        axes[i].set_ylabel('Pulse Width (μs)')
        axes[i].grid(True, alpha=0.3)

        # Add reference lines
        axes[i].axhline(y=calculator.min_pulse, color='r', linestyle='--', alpha=0.5)
        axes[i].axhline(y=calculator.max_pulse, color='r', linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.show()

def calibrate_servo_example():
    """Example of servo calibration process."""
    print("Servo Calibration Example")
    print("=" * 25)

    # Create calculator for standard servo
    calculator = AdvancedServoPWMCalculator('standard')

    print("Initial parameters (uncalibrated):")
    test_angles = [0, 90, 180]
    for angle in test_angles:
        params = calculator.get_pwm_parameters(angle)
        print(f"  {angle:3}° → {params['pulse_width_us']:6.1f}μs ({params['duty_cycle_percent']:5.2f}%)")

    # Simulate calibration measurements
    # Let's say we measured that 90° actually needs 1520μs instead of 1500μs
    measured_center_pulse = 1520.0
    expected_center_pulse = 1500.0
    pulse_offset = measured_center_pulse - expected_center_pulse

    calculator.set_calibration_offsets(pulse_offset=pulse_offset)

    print(f"\nAfter calibration (pulse offset: {pulse_offset:+.1f}μs):")
    for angle in test_angles:
        params = calculator.get_pwm_parameters(angle)
        print(f"  {angle:3}° → {params['pulse_width_us']:6.1f}μs ({params['duty_cycle_percent']:5.2f}%)")

    # Validate parameters
    validation = calculator.validate_servo_parameters()
    print(f"\nValidation Results:")
    print(f"  Overall Valid: {validation['overall_valid']}")
    print(f"  Center Point:  {validation['center_point_valid']}")
    print(f"  Range Valid:   {validation['range_valid']}")
    print(f"  Duty Cycle:    {validation['duty_cycle_range_valid']}")
    if validation['issues']:
        print("  Issues:")
        for issue in validation['issues']:
            print(f"    - {issue}")

def main():
    """Main function demonstrating advanced servo PWM mapping."""
    print("Advanced Servo PWM Mapping Solution")
    print("=" * 38)

    # Demonstrate different servo types
    print("\nDemonstrating different servo types...")
    demonstrate_servo_types()

    # Show calibration example
    print("\n" + "="*50)
    calibrate_servo_example()

    # Interactive mode
    print("\n" + "="*50)
    print("Interactive Servo Calculator")

    try:
        servo_type = input("Enter servo type (standard/wide_angle/continuous/micro) [standard]: ").strip()
        if not servo_type:
            servo_type = 'standard'

        if servo_type not in AdvancedServoPWMCalculator.SERVO_TYPES:
            print(f"Unknown type '{servo_type}', using 'standard'")
            servo_type = 'standard'

        calculator = AdvancedServoPWMCalculator(servo_type)

        while True:
            user_input = input(f"\nEnter angle ({calculator.min_angle} to {calculator.max_angle}) or 'quit': ")
            if user_input.lower() in ['quit', 'q', 'exit']:
                break

            try:
                angle = float(user_input)
                params = calculator.get_pwm_parameters(angle)
                print(f"\nResults for {params['angle']:.1f}°:")
                print(f"  Pulse Width: {params['pulse_width_us']:.1f} μs")
                print(f"  Duty Cycle:  {params['duty_cycle_percent']:.2f}%")
                print(f"  Period:      {params['period_us']:.0f} μs ({params['frequency_hz']:.0f} Hz)")

                # Show what this means practically
                high_time_ms = params['pulse_width_us'] / 1000
                low_time_ms = (params['period_us'] - params['pulse_width_us']) / 1000
                print(f"  High Time:   {high_time_ms:.3f} ms")
                print(f"  Low Time:    {low_time_ms:.3f} ms")

            except ValueError:
                print("Please enter a valid number or 'quit'")

    except KeyboardInterrupt:
        print("\nGoodbye!")

if __name__ == "__main__":
    main()