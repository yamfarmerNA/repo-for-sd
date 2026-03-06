# control/pid.py

import time

class PID:
    def __init__(self, Kp, Ki, Kd, output_limits=(-100, 100)):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.min_output, self.max_output = output_limits

        self.integral = 0
        self.previous_error = 0
        self.previous_time = time.time()

    def update(self, error):
        current_time = time.time()
        dt = current_time - self.previous_time

        if dt <= 0:
            return 0

        # PID terms
        P = self.Kp * error

        self.integral += error * dt
        I = self.Ki * self.integral

        derivative = (error - self.previous_error) / dt
        D = self.Kd * derivative

        output = P + I + D

        # Clamp output
        output = max(self.min_output, min(self.max_output, output))

        # Save state
        self.previous_error = error
        self.previous_time = current_time

        return output

    def reset(self):
        self.integral = 0
        self.previous_error = 0