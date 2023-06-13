import time
import serial
from DebugClass import DebugSerial


class PulseLaserController:
    def __init__(self, config_loader):
        if config_loader.mode == 'DEBUG':
            self.ser = DebugSerial()
        elif config_loader.mode == 'RELEASE':
            self.ser = serial.Serial(port=config_loader.port_laser, baudrate=config_loader.baudrate_laser)
        time.sleep(1)

    def emit(self, frq: int) -> bool:
        # 16~10000 Hzのみ許容する
        if 16 <= frq <= 10000:
            self.ser.write(f'{frq}\n'.encode())
            return True
        else:
            return False

    def stop(self):
        self.ser.write('-1\n'.encode())

    def quit(self):
        self.ser.close()
