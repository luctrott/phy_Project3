import board
import busio
import adafruit_vl53l0x

class VL53:
    def __init__(self):
        self._i2c = busio.I2C(board.SCL, board.SDA)
        self._vl53 = adafruit_vl53l0x.VL53L0X(self._i2c)

    def distance_mm(self):
        return self._vl53.range