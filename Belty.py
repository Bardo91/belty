import RPi.GPIO as GPIO
import time as time

class BeltControl:
   def __init__(self, servo_pin: int = 35):
      self._servo_pin: int = servo_pin

      GPIO.setmode(GPIO.BOARD)
      GPIO.setup(servo_pin, GPIO.OUT)

      self.servo = GPIO.PWM(servo_pin,500)

   def __del__(self):
      self.servo.start(0)
      self.servo.stop()

   def left(self):
      self.servo.start(80)

   def right(self):
      self.servo.start(30)

   def stop(self):
      self.servo.start(0)


if __name__ == "__main__":
   ctl: BeltControl = BeltControl()

   ctl.stop()

   for i in range(5):
      ctl.left()
      time.sleep(2)
      ctl.right()
      time.sleep(2)
      
   ctl.stop()