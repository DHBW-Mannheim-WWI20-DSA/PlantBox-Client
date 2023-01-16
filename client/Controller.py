from simple_pid import PID


class Controller:
    # Setup PID controller
    def __init__(self, kp, ki, kd, setpoint):
        self.pid = PID(kp, ki, kd, setpoint=setpoint)

    # Get PID output
    def get_output(self, current_value):
        return self.pid(current_value)

    # Get PID setpoint
    def get_setpoint(self):
        return self.pid.setpoint

    # Set PID setpoint
    def set_setpoint(self, setpoint):
        self.pid.setpoint = setpoint

    # Set PID parameters
    def set_parameters(self, kp, ki, kd):
        self.pid.tunings = (kp, ki, kd)

    # Get PID parameters
    def get_parameters(self):
        return self.pid.tunings


if __name__ == "__main__":
    # Test PID controller
    controller = Controller(10, 0.35, 2, 1)
    for i in range(1000):
        print(controller.get_output(i))
