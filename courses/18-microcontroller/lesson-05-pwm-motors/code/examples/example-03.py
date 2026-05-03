#!/usr/bin/env python3
"""
Example 03: Motor Speed PID Control Simulation
This script simulates PID control for DC motor speed using PWM output.
It demonstrates how feedback control can maintain desired motor speed
despite changing loads or disturbances.
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class PIDController:
    """PID Controller implementation for motor speed control."""
    kp: float  # Proportional gain
    ki: float  # Integral gain
    kd: float  # Derivative gain
    setpoint: float  # Desired speed
    dt: float = 0.01  # Time step

    def __post_init__(self):
        self.integral = 0.0
        self.prev_error = 0.0
        self.output_history = []
        self.error_history = []

    def compute(self, measured_value: float) -> float:
        """
        Compute PID output based on measured value.

        Args:
            measured_value (float): Current measured motor speed

        Returns:
            float: PID controller output (PWM duty cycle 0-100%)
        """
        # Calculate error
        error = self.setpoint - measured_value

        # Proportional term
        proportional = self.kp * error

        # Integral term
        self.integral += error * self.dt
        integral = self.ki * self.integral

        # Derivative term
        derivative = self.kd * (error - self.prev_error) / self.dt
        self.prev_error = error

        # Calculate total output
        output = proportional + integral + derivative

        # Clamp output to valid PWM range (0-100%)
        output = max(0.0, min(100.0, output))

        # Store history for analysis
        self.output_history.append(output)
        self.error_history.append(error)

        return output

class SimpleMotorModel:
    """Simple DC motor model for simulation purposes."""

    def __init__(self, max_speed=1000.0, time_constant=0.1):
        """
        Initialize motor model.

        Args:
            max_speed (float): Maximum motor speed at 100% PWM
            time_constant (float): Motor response time constant
        """
        self.max_speed = max_speed
        self.time_constant = time_constant
        self.current_speed = 0.0
        self.speed_history = []

    def update(self, pwm_duty_cycle: float, load_disturbance: float = 0.0) -> float:
        """
        Update motor speed based on PWM input and disturbances.

        Args:
            pwm_duty_cycle (float): PWM duty cycle (0-100%)
            load_disturbance (float): External load disturbance (-100 to 100)

        Returns:
            float: New motor speed
        """
        # Convert PWM to target speed
        target_speed = (pwm_duty_cycle / 100.0) * self.max_speed

        # Apply load disturbance (reduces effective speed)
        effective_target = target_speed + load_disturbance

        # First-order system response
        self.current_speed += (effective_target - self.current_speed) * (0.01 / self.time_constant)

        # Ensure speed doesn't go negative
        self.current_speed = max(0.0, self.current_speed)

        self.speed_history.append(self.current_speed)
        return self.current_speed

def simulate_pid_control():
    """Simulate PID motor speed control with various scenarios."""
    # Simulation parameters
    simulation_time = 10.0  # seconds
    dt = 0.01  # time step
    time_steps = int(simulation_time / dt)
    time_array = np.linspace(0, simulation_time, time_steps)

    # Create PID controller and motor model
    pid = PIDController(kp=2.0, ki=0.5, kd=0.1, setpoint=800.0, dt=dt)
    motor = SimpleMotorModel(max_speed=1000.0, time_constant=0.2)

    # Simulate control loop
    speeds = []
    pwm_outputs = []
    setpoints = []

    for i, t in enumerate(time_array):
        # Get current speed
        current_speed = motor.current_speed

        # Apply load disturbance at specific times
        load_disturbance = 0.0
        if 3.0 <= t < 4.0:
            load_disturbance = -200.0  # Sudden load increase
        elif 6.0 <= t < 7.0:
            load_disturbance = 150.0   # Load decrease

        # Update motor with current PWM output
        if i == 0:
            motor.update(0.0, load_disturbance)
        else:
            motor.update(pwm_outputs[-1], load_disturbance)

        # Get updated speed
        current_speed = motor.current_speed

        # Compute new PWM output
        pwm_output = pid.compute(current_speed)

        # Store data
        speeds.append(current_speed)
        pwm_outputs.append(pwm_output)
        setpoints.append(pid.setpoint)

    # Create plots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # Plot 1: Motor Speed vs Time
    ax1.plot(time_array, speeds, 'b-', linewidth=2, label='Actual Speed')
    ax1.plot(time_array, setpoints, 'r--', linewidth=2, label='Setpoint')
    ax1.set_title('Motor Speed Control with PID')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Speed (RPM)')
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    # Add disturbance markers
    ax1.axvspan(3.0, 4.0, alpha=0.2, color='red', label='Load Disturbance')
    ax1.axvspan(6.0, 7.0, alpha=0.2, color='green', label='Load Relief')

    # Plot 2: PWM Output vs Time
    ax2.plot(time_array, pwm_outputs, 'm-', linewidth=2)
    ax2.set_title('PWM Duty Cycle Output')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('PWM Duty Cycle (%)')
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 100)

    plt.tight_layout()
    plt.show()

    return time_array, speeds, pwm_outputs, setpoints

def compare_pid_tuning():
    """Compare different PID tuning parameters."""
    simulation_time = 5.0
    dt = 0.01
    time_steps = int(simulation_time / dt)
    time_array = np.linspace(0, simulation_time, time_steps)

    # Different PID configurations
    pid_configs = [
        {"name": "Aggressive", "kp": 5.0, "ki": 1.0, "kd": 0.5},
        {"name": "Conservative", "kp": 1.0, "ki": 0.1, "kd": 0.05},
        {"name": "Overshoot", "kp": 3.0, "ki": 0.0, "kd": 0.0},  # P-only
    ]

    plt.figure(figsize=(12, 8))

    for config in pid_configs:
        pid = PIDController(
            kp=config["kp"],
            ki=config["ki"],
            kd=config["kd"],
            setpoint=800.0,
            dt=dt
        )
        motor = SimpleMotorModel(max_speed=1000.0, time_constant=0.2)

        speeds = []
        for t in time_array:
            current_speed = motor.current_speed
            motor.update(pid.output_history[-1] if pid.output_history else 0.0)
            pwm_output = pid.compute(motor.current_speed)
            speeds.append(motor.current_speed)

        plt.plot(time_array, speeds, linewidth=2, label=config["name"])

    # Plot setpoint
    plt.plot(time_array, [800.0] * len(time_array), 'k--', linewidth=2, label='Setpoint')

    plt.title('PID Tuning Comparison')
    plt.xlabel('Time (s)')
    plt.ylabel('Motor Speed (RPM)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()

def main():
    """Main function to demonstrate motor PID control simulation."""
    print("Motor Speed PID Control Simulation")
    print("=" * 35)

    print("PID Controller Parameters:")
    print("- Kp (Proportional): Reacts to current error")
    print("- Ki (Integral): Eliminates steady-state error")
    print("- Kd (Derivative): Dampens oscillations")
    print()

    print("Simulation Scenarios:")
    print("1. Basic PID control with load disturbances")
    print("2. Comparison of different PID tuning strategies")
    print()

    # Run basic simulation
    print("Running basic PID control simulation...")
    time_array, speeds, pwm_outputs, setpoints = simulate_pid_control()

    # Calculate performance metrics
    steady_state_error = abs(setpoints[-1] - speeds[-1])
    overshoot = max(speeds) - setpoints[0] if max(speeds) > setpoints[0] else 0

    print(f"\nPerformance Metrics:")
    print(f"- Steady-state error: {steady_state_error:.2f} RPM")
    print(f"- Maximum overshoot: {overshoot:.2f} RPM")
    print(f"- Settling time: ~{len([s for s in speeds if abs(s - 800) < 20]) * 0.01:.2f} s")

    # Run tuning comparison
    print("\nRunning PID tuning comparison...")
    compare_pid_tuning()

    print("\nKey Takeaways:")
    print("- PID control maintains desired speed despite disturbances")
    print("- Proper tuning is crucial for good performance")
    print("- PWM provides the control signal to the motor driver")
    print("- Real systems need careful consideration of sampling rate and delays")

if __name__ == "__main__":
    main()