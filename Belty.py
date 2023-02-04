import pigpio
import time as time


class BeltControl:
    def __init__(self, servo_pin: int = 19):
        self.servo_pin: int = servo_pin

        self.pi_control = pigpio.pi()

    def __del__(self):
        self.stop()

    def left(self):
        self.pi_control.set_servo_pulsewidth(self.servo_pin, 1500)

    def right(self):
        self.pi_control.set_servo_pulsewidth(self.servo_pin, 500)

    def stop(self):
        self.pi_control.set_servo_pulsewidth(self.servo_pin, 0)
        self.pi_control.stop()


class CameraControl:
    def __init__(self, pan_pin: int = 13, tilt_pin: int = 21):
        self.pan_pin = pan_pin
        self.tilt_pin = tilt_pin

        self.pi_control = pigpio.pi()
        
    def __del__(self):
        self.stop()

    # Move camera
    # \param pan: value from 0 to 100
    # \param tilt: value from 0 to 100
    def move(self, pan: int, tilt: int):
        self.pi_control.set_servo_pulsewidth(self.pan_pin, self._map_value(pan, 500, 2500))
        self.pi_control.set_servo_pulsewidth(self.tilt_pin, self._map_value(tilt, 800, 2000))

    def stop(self):
        self.pi_control.stop()

    def _map_value(self, val, min, max):
        return min + val/100.0*(max - min)


if __name__ == "__main__":
    ctl: BeltControl = BeltControl()

    ctl.stop()

    for i in range(5):
        ctl.left()
        time.sleep(2)
        ctl.right()
        time.sleep(2)

    ctl.stop()
