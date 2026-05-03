#!/usr/bin/env python3
"""
Example 01: PWM Waveform Generation and Duty Cycle Visualization
This script demonstrates how to generate PWM waveforms with different duty cycles
and visualize them using matplotlib.
"""

import numpy as np
import matplotlib.pyplot as plt

def generate_pwm_waveform(duty_cycle, frequency=1000, duration=0.01):
    """
    Generate a PWM waveform with specified duty cycle and frequency.

    Args:
        duty_cycle (float): Duty cycle as a decimal (0.0 to 1.0)
        frequency (float): PWM frequency in Hz
        duration (float): Duration of waveform to generate in seconds

    Returns:
        tuple: (time_array, pwm_signal)
    """
    # High sample rate for smooth visualization
    sample_rate = 100000  # 100 kHz sampling
    num_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, num_samples)

    # Calculate period and high time
    period = 1.0 / frequency
    high_time = duty_cycle * period

    # Generate PWM signal using modulo operation
    pwm_signal = np.where((t % period) < high_time, 1.0, 0.0)

    return t, pwm_signal

def calculate_average_voltage(duty_cycle, vcc=5.0):
    """
    Calculate the average voltage of a PWM signal.

    Args:
        duty_cycle (float): Duty cycle as decimal (0.0 to 1.0)
        vcc (float): Supply voltage

    Returns:
        float: Average voltage
    """
    return duty_cycle * vcc

def main():
    """Main function to demonstrate PWM waveforms."""
    print("PWM Waveform Generation and Analysis")
    print("=" * 40)

    # Define duty cycles to demonstrate
    duty_cycles = [0.1, 0.25, 0.5, 0.75, 0.9]
    frequency = 1000  # 1 kHz

    # Create subplots for each duty cycle
    fig, axes = plt.subplots(len(duty_cycles), 1, figsize=(12, 10))
    fig.suptitle(f'PWM Waveforms at {frequency} Hz', fontsize=16)

    for i, dc in enumerate(duty_cycles):
        t, signal = generate_pwm_waveform(dc, frequency)
        avg_voltage = calculate_average_voltage(dc)

        # Plot only first few periods for clarity
        samples_to_show = 2000  # Show ~2ms of signal
        axes[i].plot(t[:samples_to_show] * 1000, signal[:samples_to_show], 'b-', linewidth=2)
        axes[i].set_title(f'Duty Cycle: {dc*100:.0f}% (Avg Voltage: {avg_voltage:.2f}V)')
        axes[i].set_xlabel('Time (ms)')
        axes[i].set_ylabel('Voltage (V)')
        axes[i].set_ylim(-0.1, 1.1)
        axes[i].grid(True, alpha=0.3)
        axes[i].set_xlim(0, 2)  # Show 2ms window

        print(f"Duty Cycle: {dc*100:3.0f}% | Average Voltage: {avg_voltage:5.2f}V | "
              f"High Time: {dc*1000/frequency:6.3f}ms")

    plt.tight_layout()
    plt.show()

    # Demonstrate frequency effect on perceived brightness/speed
    print("\nFrequency Effects:")
    print("- Low frequency (<100Hz): Visible flicker for LEDs, audible noise for motors")
    print("- Medium frequency (200-1000Hz): Good for most applications")
    print("- High frequency (>5kHz): Quiet operation, reduced EMI, but higher switching losses")

if __name__ == "__main__":
    main()