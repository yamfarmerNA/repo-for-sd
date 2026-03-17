# control/pid.py
# Convert tracking errors into drone velocity commands
import time

class PID:
    ''' Each controller computes an output value based on the current error.
    '''
    def __init__(self, Kp, Ki, Kd, output_limits=(-100, 100)):
        '''
        Initialize the PID controller.

        Parameters
        ----------
        Kp : float
            Proportional gain

        Ki : float
            Integral gain

        Kd : float
            Derivative gain

        output_limits : tuple
            Minimum and maximum allowed output

        integral_limit : float
            Prevents the integral term from growing too large
            (integral windup protection)
        '''
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        
        # Output limits to keep commands safe
        self.min_output, self.max_output = output_limits

        # PID internal state variables
        self.integral = 0
        self.previous_error = 0
        self.previous_time = time.time()

    def update(self, error):
        '''
        Compute the PID output for the current error.

        Parameters
        ----------
        error : float
            Difference between desired value and current value

        Returns
        -------
        output : float
            Control command computed by the PID controller
        '''
        current_time = time.time()
        dt = current_time - self.previous_time

        # Prevent division by zero if called too quickly
        if dt <= 0:
            return 0

        # PID terms ---------
        
        # Responds immediately to the current error
        P = self.Kp * error

        # Accumulates past errors over time
        # Helps remove steady-state error
        self.integral += error * dt
        I = self.Ki * self.integral

        # Predicts future error based on rate of change
        derivative = (error - self.previous_error) / dt
        D = self.Kd * derivative

        output = P + I + D

        # Clamp output
        output = max(self.min_output, min(self.max_output, output))

        # Save state for next update cycle
        self.previous_error = error
        self.previous_time = current_time

        return output

    def reset(self):
        """
        Reset the internal PID state for when restarting control loops.
        """
        self.integral = 0
        self.previous_error = 0
