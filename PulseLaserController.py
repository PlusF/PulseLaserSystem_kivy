import time
import serial


class PulseLaserController:
    def __init__(self, ser: serial.Serial):
        """
        initialization
        :param ser: opened port for communication
        :type ser: serial.Serial
        """
        self.ser = ser
        time.sleep(1)

    def set_frq(self, frq: int) -> bool:
        # 16~10000 Hzのみ許容する
        if 16 <= frq <= 10000:
            self.ser.write(f'{frq}\n'.encode())
            return True
        else:
            return False

    def stop(self):
        self.ser.write('-1\n'.encode())
