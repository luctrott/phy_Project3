from TBS1_VL53 import VL53
import time

if __name__ == "__main__":
    vl53 = VL53()
    while True:
        print(vl53.distance_mm())
        time.sleep(1)