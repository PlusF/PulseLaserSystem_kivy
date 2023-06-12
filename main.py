from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.base import ExceptionManager, ExceptionHandler
from kivy.clock import Clock
import time

from zaber_motion import Units, Library, LogOutputMode
from zaber_motion.binary import Connection, Device

# メモ：ZaberControllerクラスをインポート
from ZaberController import ZaberController
# from ds102controller import MySerial, DS102Controller
# from PulseLaserController import PulseLaserController
# from ConfigLoader import ConfigLoader
# from CommandWindow import CommandWindow
#from PulseLaserController import PulseLaserController

Window.size = (350, 700)

class MainWindow(BoxLayout):
    delta_x = NumericProperty(100)
    delta_y = NumericProperty(50)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # TODO: IMPLEMENT ME
        # メモ：ZaberControllerクラスのインスタンスを作成
        self.Zaberhandler = ZaberController("COM3")

#ステージ止める
    def stop_all(self):
        self.Zaberhandler.stop_all()
#ステージ移動（速度指定)
    def move_top(self):
        self.Zaberhandler.vel = float(self.ids.speed_input.text)
        self.Zaberhandler.move_top(float(self.ids.speed_input.text))
        pass

    def move_bottom(self):
        self.Zaberhandler.vel = float(self.ids.speed_input.text)
        self.Zaberhandler.move_bottom(float(self.ids.speed_input.text))
        pass

    def move_left(self):
        self.Zaberhandler.vel = float(self.ids.speed_input.text)
        self.Zaberhandler.move_left(float(self.ids.speed_input.text))
        pass

    def move_right(self):
        self.Zaberhandler.vel = float(self.ids.speed_input.text)
        #print(self.ids.speed_input.text)
        self.Zaberhandler.move_right(float(self.ids.speed_input.text))
        pass

    def print_position(self):
        print(f'x position : {self.Zaberhandler.device_x.get_position(unit=self.unit_pos)}')
        print(f'y position : {self.Zaberhandler.device_y.get_position(unit=self.unit_pos)}')
        time.sleep(1)
        pass

# ステージ移動（変位指定)
    def move_rect(self):
        self.Zaberhandler.vel = float(self.ids.speed_input.text)
        self.Zaberhandler.move_right()
        time.sleep(float(self.ids.deltaX.text) / float(self.ids.speed_input.text))
        self.Zaberhandler.stop()
        # self.Zaberhandler.y_relative_position = 0
        # self.Zaberhandler.move_relative()
        # self.Zaberhandler.x_relative_position = 0
        # self.Zaberhandler.y_relative_position = int(self.ids.deltaY.text)
        # self.Zaberhandler.move_relative()
        # self.Zaberhandler.x_relative_position = -int(self.ids.deltaX.text)
        # self.Zaberhandler.y_relative_position = 0
        # self.Zaberhandler.move_relative()
        # self.Zaberhandler.x_relative_position = 0
        # self.Zaberhandler.y_relative_position = -int(self.ids.deltaY.text)
        # self.Zaberhandler.move_relative()
        pass

    def move_line(self):
        self.x_relative_position = self.ids.deltaX.text
        self.y_relative_position = self.ids.deltaY.text
        move_relative(self)
        pass

    #set origin
    def set_org(self):
        self.Zaberhandler.x_relative_position = 0
        pass

    #レーザー射出

    # def emit(self):
   #      frq = self.frq.get()
   #      if not 16 <= frq <= 10000:
   #          print('Frequency must be 16~10000 Hz.')
   #      if toggle_manual_emit.state == "normal"
   #          self.laser.set_frq(frq)
   #          print('Emit')
   #  def stop_laser(self):
   #          self.laser.stop()
   #          print('Stop laser')

    def check(self,text):
        print(text)

#描画
class MainApp(App):
    def build(self):
        window = MainWindow()
        return window



class CrashHandler(ExceptionHandler):
    def handle_exception(self, inst):
        print(inst)
        return ExceptionManager.PASS
ExceptionManager.add_handler(CrashHandler())


if __name__ == '__main__':
    MainApp().run()











import serial
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window, Clock
from kivy.properties import NumericProperty
from PulseLaserController import PulseLaserController
# メモ：ZaberControllerクラスをインポート


def control_auto_emission(func):
    def wrapper(self, *args, **kwargs):
        auto_on = self.ids.toggle_auto_emit.state == 'down'
        if auto_on:
            self.emit_laser()
        ret = func(*args, **kwargs)
        return ret
    return wrapper


class MainWindow(Widget):
    pos_x = NumericProperty(0, force_dispatch=True)
    pos_y = NumericProperty(0, force_dispatch=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_request_close=self.quit)

        self.freq: int = 100
        self.speed: float = 100.0
        self.ser_laser = serial.Serial(port='COM9', baudrate=9600)
        self.laser = PulseLaserController(self.ser_laser)
        # メモ：ZaberControllerクラスのインスタンスを作成
        self.stage = None
        Clock.schedule_interval(self.update_position, 0.1)  # 0.1秒ごとに位置を更新．

    def update_position(self):
        self.pos_x, self.pos_y = self.stage.get_position()

    @control_auto_emission
    def move_top(self):
        # TODO: IMPLEMENT ME
        # メモ：ZaberControllerインスタンスのmove_top関数を呼び出す
        pass

    @control_auto_emission
    def move_bottom(self):
        # TODO: IMPLEMENT ME
        pass

    @control_auto_emission
    def move_left(self):
        # TODO: IMPLEMENT ME
        pass

    @control_auto_emission
    def move_right(self):
        # TODO: IMPLEMENT ME
        pass

    def stop_moving(self):
        auto_on = self.ids.toggle_auto_emit.state == 'down'
        if auto_on:
            self.stop_laser()
        # TODO: stop()

    def emit_laser(self):
        ok = self.laser.emit(self.freq)
        if not ok:
            # TODO: 警告を表示する
            pass

    def stop_laser(self):
        self.laser.stop()

    def set_freq(self, freq: str):
        try:
            freq_int = int(freq)
        except ValueError:
            print('invalid frequency value: ', freq)
            return

        if freq_int < 16:
            freq_int = 16
        elif freq_int > 10000:
            freq_int = 10000

        self.freq = freq_int

    def set_speed(self, speed: str):
        try:
            speed_float = int(speed)
        except ValueError:
            print('invalid speed value: ', speed)
            return

        # TODO: ステージの最低，最高速度を確認
        if speed_float < 0.05:
            speed_float = 0.05
        elif speed_float > 10000:
            speed_float = 10000

        self.speed = speed_float

    def quit(self):
        self.ser_laser.close()


class MainApp(App):
    def build(self):
        window = MainWindow()
        return window


if __name__ == '__main__':
    MainApp().run()