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



class CameraControl:
   def __init__(self, pan_pin: int = 33, tilt_pin: int = 32):
      self.pan_pin = pan_pin
      self.tilt_pin = tilt_pin

      GPIO.setmode(GPIO.BOARD)
      GPIO.setup(self.pan_pin, GPIO.OUT)
      GPIO.setup(self.tilt_pin, GPIO.OUT)

      self.servo_pan = GPIO.PWM(self.pan_pin,500)
      self.servo_tilt = GPIO.PWM(self.tilt_pin,500)

   def __del__(self):
      self.stop()

   def move(self, pan: int, tilt: int):
      self.servo_pan.start(pan)
      self.servo_tilt.start(tilt)

   def stop(self):
      self.servo_pan.stop()
      self.servo_tilt.stop()

if __name__ == "__main__":
   ctl: BeltControl = BeltControl()

   ctl.stop()

   for i in range(5):
      ctl.left()
      time.sleep(2)
      ctl.right()
      time.sleep(2)
      
   ctl.stop()