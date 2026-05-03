#!/usr/bin/env python3
"""
Solution 01: PWM Waveform Generation and Duty Cycle Visualization
Complete solution with enhanced features and analysis.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List

def generate_pwm_waveform(duty_cycle: float, frequency: float = 1000,
                         duration: float = 0.01) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate a PWM waveform with specified duty cycle and frequency.

    Args:
        duty_cycle (float): Duty cycle as a decimal (0.0 to 1.0)
        frequency (float): PWM frequency in Hz
        duration (float): Duration of waveform to generate in seconds

    Returns:
        tuple: (time_array, pwm_signal)
    """
    # Validate inputs
    if not 0 <= duty_cycle <= 1:
        raise ValueError("Duty cycle must be between 0 and 1")
    if frequency <= 0:
        raise ValueError("Frequency must be positive")
    if duration <= 0:
        raise ValueError("Duration must be positive")

    # High sample rate for smooth visualization (10x the PWM frequency minimum)
    sample_rate = max(100000, int(frequency * 100))
    num_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, num_samples, endpoint=False)

    # Calculate period and high time
    period = 1.0 / frequency
    high_time = duty_cycle * period

    # Generate PWM signal using vectorized operations
    pwm_signal = ((t % period) < high_time).astype(float)

    return t, pwm_signal

def calculate_average_voltage(duty_cycle: float, vcc: float = 5.0) -> float:
    """
    Calculate the average voltage of a PWM signal.

    Args:
        duty_cycle (float): Duty cycle as decimal (0.0 to 1.0)
        vcc (float): Supply voltage

    Returns:
        float: Average voltage
    """
    if vcc < 0:
        raise ValueError("Supply voltage must be non-negative")
    return duty_cycle * vcc

def analyze_pwm_effectiveness(duty_cycle: float, frequency: float) -> dict:
    """
    Analyze PWM effectiveness for different applications.

    Args:
        duty_cycle (float): Duty cycle as decimal
        frequency (float): PWM frequency in Hz

    Returns:
        dict: Analysis results for different applications
    """
    results = {
        'led_flicker_visible': frequency < 100,
        'motor_audible_noise': frequency < 20000,
        'efficiency_rating': 'High' if frequency > 1000 else 'Medium' if frequency > 100 else 'Low',
        'recommended_applications': []
    }

    if frequency >= 200:
        results['recommended_applications'].append('LED Dimming')
    if 1000 <= frequency <= 20000:
        results['recommended_applications'].append('DC Motor Control')
    if abs(frequency - 50) < 1:
        results['recommended_applications'].append('Servo Control')

    return results

def main():
    """Main function demonstrating comprehensive PWM analysis."""
    print("Advanced PWM Waveform Generation and Analysis")
    print("=" * 50)

    # Test multiple scenarios
    test_cases = [
        {'duty_cycle': 0.25, 'frequency': 100, 'label': 'Low Freq LED'},
        {'duty_cycle': 0.5, 'frequency': 1000, 'label': 'Medium Freq Motor'},
        {'duty_cycle': 0.75, 'frequency': 20000, 'label': 'High Freq Quiet'},
        {'duty_cycle': 0.5, 'frequency': 50, 'label': 'Servo Standard'},
    ]

    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()

    for i, case in enumerate(test_cases):
        t, signal = generate_pwm_waveform(case['duty_cycle'], case['frequency'])
        avg_voltage = calculate_average_voltage(case['duty_cycle'])
        analysis = analyze_pwm_effectiveness(case['duty_cycle'], case['frequency'])

        # Plot waveform (show 2-3 periods for clarity)
        periods_to_show = 3
        period_duration = 1.0 / case['frequency']
        end_time = min(periods_to_show * period_duration, t[-1])
        mask = t <= end_time

        axes[i].plot(t[mask] * 1000, signal[mask], 'b-', linewidth=2)
        axes[i].set_title(f"{case['label']}\n"
                         f"Duty: {case['duty_cycle']*100:.0f}%, "
                         f"Freq: {case['frequency']}Hz\n"
                         f"Avg Voltage: {avg_voltage:.2f}V")
        axes[i].set_xlabel('Time (ms)')
        axes[i].set_ylabel('Voltage (V)')
        axes[i].set_ylim(-0.1, 1.1)
        axes[i].grid(True, alpha=0.3)

        print(f"\n{case['label']}:")
        print(f"  Duty Cycle: {case['duty_cycle']*100:6.1f}%")
        print(f"  Frequency:  {case['frequency']:8.0f} Hz")
        print(f"  Avg Voltage: {avg_voltage:8.2f} V")
        print(f"  LED Flicker: {'Yes' if analysis['led_flicker_visible'] else 'No'}")
        print(f"  Motor Noise: {'Yes' if analysis['motor_audible_noise'] else 'No'}")
        print(f"  Efficiency:  {analysis['efficiency_rating']}")
        if analysis['recommended_applications']:
            print(f"  Recommended: {', '.join(analysis['recommended_applications'])}")

    plt.tight_layout()
    plt.show()

    # Interactive frequency sweep
    print("\nFrequency Sweep Analysis:")
    frequencies = [50, 100, 500, 1000, 5000, 10000, 20000]
    duty_cycle = 0.5

    freq_analysis = []
    for freq in frequencies:
        analysis = analyze_pwm_effectiveness(duty_cycle, freq)
        freq_analysis.append({
            'frequency': freq,
            'led_ok': not analysis['led_flicker_visible'],
            'motor_quiet': not analysis['motor_audible_noise'],
            'efficiency': analysis['efficiency_rating']
        })

    print(f"{'Frequency (Hz)':>12} {'LED OK':>8} {'Motor Quiet':>12} {'Efficiency':>12}")
    print("-" * 45)
    for item in freq_analysis:
        print(f"{item['frequency']:12} {'✓' if item['led_ok'] else '✗':>8} "
              f"{'✓' if item['motor_quiet'] else '✗':>12} {item['efficiency']:>12}")

if __name__ == "__main__":
    main()