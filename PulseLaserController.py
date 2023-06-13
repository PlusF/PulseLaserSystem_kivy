import time
import serial
from ConfigLoader import ConfigLoader
from DebugClass import DebugSerial


class PulseLaserController:
    def __init__(self, cl: ConfigLoader):
        # DEBUGモードの場合は形だけのクラスを使う
        if cl.mode == 'DEBUG':
            self.ser = DebugSerial()
        elif cl.mode == 'RELEASE':
            self.ser = serial.Serial(port=cl.port_laser, baudrate=cl.baudrate_laser)
        time.sleep(1)

    def emit(self, frq: int) -> bool:
        # 16~10000 Hzのみ許容する
        if 16 <= frq <= 10000:
            self.ser.write(f'{frq}\n'.encode())
            return True
        else:
            return False

    def stop(self):
        # -1を送るとstopする仕様（金田が策定）
        self.ser.write('-1\n'.encode())

    def quit(self):
        self.ser.close()
