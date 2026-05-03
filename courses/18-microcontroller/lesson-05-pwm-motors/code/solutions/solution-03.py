#!/usr/bin/env python3
"""
Solution 03: Advanced Motor Speed PID Control with Real-world Considerations
Complete solution for motor PID control simulation with realistic constraints.
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Callable
import time

@dataclass
class AdvancedPIDController:
    """
    Advanced PID controller with anti-windup, derivative filtering,
    and output constraints.
    """
    kp: float
    ki: float
    kd: float
    setpoint: float
    dt: float = 0.01
    output_min: float = 0.0
    output_max: float = 100.0
    integral_min: float = -100.0
    integral_max: float = 100.0
    derivative_filter_alpha: float = 0.1  # For derivative filtering

    def __post_init__(self):
        self.integral = 0.0
        self.prev_error = 0.0
        self.prev_derivative = 0.0
        self.output_history: List[float] = []
        self.error_history: List[float] = []
        self.integral_history: List[float] = []
        self.derivative_history: List[float] = []

    def compute(self, measured_value: float, feedforward: float = 0.0) -> float:
        """
        Compute PID output with advanced features.

        Args:
            measured_value (float): Current measured value
            feedforward (float): Feedforward term for known disturbances

        Returns:
            float: Controller output
        """
        # Calculate error
        error = self.setpoint - measured_value

        # Proportional term
        proportional = self.kp * error

        # Integral term with anti-windup
        self.integral += error * self.dt

        # Apply integral limits to prevent windup
        self.integral = max(self.integral_min, min(self.integral_max, self.integral))
        integral = self.ki * self.integral

        # Derivative term with filtering (to reduce noise sensitivity)
        raw_derivative = (error - self.prev_error) / self.dt if self.prev_error is not None else 0.0

        # Apply low-pass filter to derivative
        if self.prev_derivative is not None:
            filtered_derivative = (self.derivative_filter_alpha * raw_derivative +
                                 (1 - self.derivative_filter_alpha) * self.prev_derivative)
        else:
            filtered_derivative = raw_derivative

        derivative = self.kd * filtered_derivative

        # Update previous values
        self.prev_error = error
        self.prev_derivative = filtered_derivative

        # Calculate total output with feedforward
        output = proportional + integral + derivative + feedforward

        # Apply output constraints
        output = max(self.output_min, min(self.output_max, output))

        # Store history
        self.output_history.append(output)
        self.error_history.append(error)
        self.integral_history.append(self.integral)
        self.derivative_history.append(filtered_derivative)

        return output

    def reset(self):
        """Reset controller state."""
        self.integral = 0.0
        self.prev_error = 0.0
        self.prev_derivative = 0.0
        self.output_history.clear()
        self.error_history.clear()
        self.integral_history.clear()
        self.derivative_history.clear()

@dataclass
class RealisticMotorModel:
    """
    Realistic DC motor model with friction, load variations,
    and PWM nonlinearity.
    """
    max_speed: float = 1000.0
    time_constant: float = 0.1
    friction_coefficient: float = 0.1
    pwm_nonlinearity: float = 0.1  # PWM response nonlinearity factor
    noise_level: float = 5.0       # Measurement noise level
    disturbance_function: Optional[Callable[[float], float]] = None

    def __post_init__(self):
        self.current_speed = 0.0
        self.speed_history: List[float] = []
        self.true_speed_history: List[float] = []

    def update(self, pwm_duty_cycle: float, time_step: float = 0.01) -> float:
        """
        Update motor speed with realistic effects.

        Args:
            pwm_duty_cycle (float): PWM duty cycle (0-100%)
            time_step (float): Simulation time step

        Returns:
            float: Measured motor speed (with noise)
        """
        # Apply PWM nonlinearity (real motors don't respond linearly at extremes)
        if pwm_duty_cycle < 10:
            effective_pwm = pwm_duty_cycle * (1 + self.pwm_nonlinearity)
        elif pwm_duty_cycle > 90:
            effective_pwm = pwm_duty_cycle - (100 - pwm_duty_cycle) * self.pwm_nonlinearity
        else:
            effective_pwm = pwm_duty_cycle

        # Convert to target speed
        target_speed = (effective_pwm / 100.0) * self.max_speed

        # Apply friction (reduces speed, especially at low PWM)
        friction_loss = self.friction_coefficient * (self.current_speed ** 0.5)

        # Apply external disturbances
        disturbance = 0.0
        if self.disturbance_function:
            disturbance = self.disturbance_function(len(self.speed_history) * time_step)

        # First-order system response with friction and disturbances
        net_target = max(0, target_speed + disturbance - friction_loss)
        self.current_speed += (net_target - self.current_speed) * (time_step / self.time_constant)

        # Store true speed (without measurement noise)
        self.true_speed_history.append(self.current_speed)

        # Add measurement noise (simulate encoder/sensor noise)
        measured_speed = self.current_speed + np.random.normal(0, self.noise_level)

        # Ensure measured speed doesn't go negative
        measured_speed = max(0.0, measured_speed)
        self.speed_history.append(measured_speed)

        return measured_speed

def create_disturbance_function(disturbance_profile: str = 'step') -> Callable[[float], float]:
    """Create disturbance function based on profile."""
    if disturbance_profile == 'step':
        def disturbance(t: float) -> float:
            if 3.0 <= t < 4.0:
                return -200.0
            elif 6.0 <= t < 7.0:
                return 150.0
            else:
                return 0.0
    elif disturbance_profile == 'ramp':
        def disturbance(t: float) -> float:
            if t < 5.0:
                return -50.0 * t
            else:
                return -250.0 + 30.0 * (t - 5.0)
    elif disturbance_profile == 'oscillating':
        def disturbance(t: float) -> float:
            return 100.0 * np.sin(2 * np.pi * 0.5 * t)
    else:
        def disturbance(t: float) -> float:
            return 0.0

    return disturbance

def simulate_advanced_pid_control(
    pid_params: dict,
    motor_params: dict,
    disturbance_profile: str = 'step',
    simulation_time: float = 10.0
) -> Tuple[np.ndarray, List[float], List[float], List[float]]:
    """
    Simulate advanced PID motor control with realistic conditions.
    """
    dt = 0.01
    time_steps = int(simulation_time / dt)
    time_array = np.linspace(0, simulation_time, time_steps)

    # Create controller and motor
    pid = AdvancedPIDController(**pid_params, dt=dt)
    motor = RealisticMotorModel(**motor_params)
    motor.disturbance_function = create_disturbance_function(disturbance_profile)

    # Simulate control loop
    speeds = []
    pwm_outputs = []
    setpoints = []
    true_speeds = []

    for i, t in enumerate(time_array):
        # Get current speed (with noise)
        if i == 0:
            current_speed = motor.update(0.0, dt)
        else:
            current_speed = motor.update(pwm_outputs[-1], dt)

        # Store true speed for comparison
        true_speed = motor.true_speed_history[-1]

        # Handle setpoint changes (ramp up to avoid derivative kick)
        if t < 1.0:
            current_setpoint = pid_params['setpoint'] * (t / 1.0)
            pid.setpoint = current_setpoint
        else:
            current_setpoint = pid_params['setpoint']

        # Compute new PWM output
        # Feedforward term could be used for known load characteristics
        feedforward = 0.0
        if 3.0 <= t < 4.0:
            feedforward = 20.0  # Anticipate load increase

        pwm_output = pid.compute(current_speed, feedforward)

        # Store data
        speeds.append(current_speed)
        pwm_outputs.append(pwm_output)
        setpoints.append(current_setpoint)
        true_speeds.append(true_speed)

    return time_array, speeds, pwm_outputs, setpoints, true_speeds, pid

def compare_control_strategies():
    """Compare different control strategies and tuning approaches."""
    simulation_time = 8.0
    dt = 0.01
    time_array = np.linspace(0, simulation_time, int(simulation_time / dt))

    # Different control strategies
    strategies = [
        {
            'name': 'Aggressive PID',
            'params': {'kp': 3.0, 'ki': 0.8, 'kd': 0.2, 'setpoint': 800.0}
        },
        {
            'name': 'Conservative PID',
            'params': {'kp': 1.0, 'ki': 0.2, 'kd': 0.05, 'setpoint': 800.0}
        },
        {
            'name': 'PI Only',
            'params': {'kp': 2.0, 'ki': 0.5, 'kd': 0.0, 'setpoint': 800.0}
        },
        {
            'name': 'P Only',
            'params': {'kp': 2.0, 'ki': 0.0, 'kd': 0.0, 'setpoint': 800.0}
        }
    ]

    motor_params = {
        'max_speed': 1000.0,
        'time_constant': 0.15,
        'friction_coefficient': 0.15,
        'noise_level': 8.0
    }

    plt.figure(figsize=(15, 10))

    for i, strategy in enumerate(strategies):
        time_array, speeds, pwm_outputs, setpoints, true_speeds, pid = \
            simulate_advanced_pid_control(
                strategy['params'], motor_params, 'step', simulation_time
            )

        # Plot speed response
        plt.subplot(2, 2, i+1)
        plt.plot(time_array, speeds, 'b-', alpha=0.7, label='Measured Speed')
        plt.plot(time_array, true_speeds, 'g--', alpha=0.8, label='True Speed')
        plt.plot(time_array, setpoints, 'r--', linewidth=2, label='Setpoint')
        plt.title(f"{strategy['name']}\nKp={strategy['params']['kp']}, "
                 f"Ki={strategy['params']['ki']}, Kd={strategy['params']['kd']}")
        plt.xlabel('Time (s)')
        plt.ylabel('Speed (RPM)')
        plt.grid(True, alpha=0.3)
        plt.legend()

        # Calculate performance metrics
        steady_state_error = abs(setpoints[-1] - speeds[-1])
        overshoot = max(0, max(speeds) - setpoints[0]) if speeds else 0
        settling_time = sum(1 for s in speeds if abs(s - setpoints[0]) < 20) * dt

        print(f"\n{strategy['name']} Performance:")
        print(f"  Steady-state error: {steady_state_error:.2f} RPM")
        print(f"  Maximum overshoot:  {overshoot:.2f} RPM")
        print(f"  Settling time:      {settling_time:.2f} s")

    plt.tight_layout()
    plt.show()

def main():
    """Main function demonstrating advanced motor PID control."""
    print("Advanced Motor Speed PID Control Solution")
    print("=" * 45)

    print("Key Features Implemented:")
    print("- Anti-windup protection for integral term")
    print("- Derivative filtering to reduce noise sensitivity")
    print("- Output and integral constraints")
    print("- Feedforward control for disturbance rejection")
    print("- Realistic motor model with friction and nonlinearity")
    print("- Measurement noise simulation")
    print("- Multiple disturbance profiles")

    # Run basic simulation
    print("\nRunning basic simulation with step disturbances...")

    pid_params = {'kp': 2.5, 'ki': 0.6, 'kd': 0.15, 'setpoint': 800.0}
    motor_params = {
        'max_speed': 1000.0,
        'time_constant': 0.12,
        'friction_coefficient': 0.12,
        'pwm_nonlinearity': 0.15,
        'noise_level': 6.0
    }

    time_array, speeds, pwm_outputs, setpoints, true_speeds, pid = \
        simulate_advanced_pid_control(pid_params, motor_params, 'step')

    # Create comprehensive plots
    fig, axes = plt.subplots(3, 1, figsize=(12, 12))

    # Speed response
    axes[0].plot(time_array, speeds, 'b-', alpha=0.7, label='Measured Speed')
    axes[0].plot(time_array, true_speeds, 'g--', alpha=0.8, label='True Speed')
    axes[0].plot(time_array, setpoints, 'r--', linewidth=2, label='Setpoint')
    axes[0].set_title('Motor Speed Response')
    axes[0].set_ylabel('Speed (RPM)')
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    # PWM output
    axes[1].plot(time_array, pwm_outputs, 'm-', linewidth=2)
    axes[1].set_title('PWM Duty Cycle Output')
    axes[1].set_ylabel('PWM (%)')
    axes[1].set_ylim(0, 100)
    axes[1].grid(True, alpha=0.3)

    # Control components
    if len(pid.proportional_history := [pid.kp * e for e in pid.error_history]) > 0:
        axes[2].plot(time_array, pid.proportional_history, 'r-', alpha=0.7, label='Proportional')
        axes[2].plot(time_array, [pid.ki * i for i in pid.integral_history], 'g-', alpha=0.7, label='Integral')
        axes[2].plot(time_array, [pid.kd * d for d in pid.derivative_history], 'b-', alpha=0.7, label='Derivative')
        axes[2].set_title('PID Component Contributions')
        axes[2].set_xlabel('Time (s)')
        axes[2].set_ylabel('Component Value')
        axes[2].grid(True, alpha=0.3)
        axes[2].legend()

    plt.tight_layout()
    plt.show()

    # Compare different strategies
    print("\nComparing different control strategies...")
    compare_control_strategies()

    print("\nPractical Implementation Tips:")
    print("1. Start with P-only control, then add I, then D")
    print("2. Use derivative filtering to handle sensor noise")
    print("3. Implement anti-windup to prevent integral saturation")
    print("4. Consider feedforward for known disturbances")
    print("5. Tune in realistic conditions with actual hardware")
    print("6. Account for PWM nonlinearity at low/high duty cycles")
    print("7. Always test with worst-case disturbance scenarios")

if __name__ == "__main__":
    # Monkey patch to store proportional history for plotting
    def compute_with_history(self, measured_value: float, feedforward: float = 0.0) -> float:
        error = self.setpoint - measured_value
        proportional = self.kp * error
        if not hasattr(self, 'proportional_history'):
            self.proportional_history = []
        self.proportional_history.append(proportional)
        return self._original_compute(measured_value, feedforward)

    AdvancedPIDController._original_compute = AdvancedPIDController.compute
    AdvancedPIDController.compute = compute_with_history

    main()