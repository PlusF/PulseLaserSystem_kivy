import serial
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window, Clock
from kivy.properties import NumericProperty
from ConfigLoader import ConfigLoader
from kivy.base import ExceptionManager, ExceptionHandler
from kivy.clock import Clock
from PulseLaserController import PulseLaserController
import time
from zaber_motion import Units, Library, LogOutputMode
from zaber_motion.binary import Connection, Device
from ZaberController import ZaberController

Window.size = (350, 700)

def control_auto_emission(func):
    def wrapper(self, *args, **kwargs):
        auto_on = self.ids.toggle_auto_emit.state == 'down'
        if auto_on:
            self.emit_laser()
        ret = func(*args, **kwargs)
        return ret
    return wrapper

class MainWindow(BoxLayout):
    pos_x = NumericProperty(0, force_dispatch=True)
    pos_y = NumericProperty(0, force_dispatch=True)
    delta_x = NumericProperty(100)
    delta_y = NumericProperty(50)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_request_close=self.quit)


        self.cl = ConfigLoader('./config.json')

        self.freq: int = 100
        self.speed: float = 100.0
        #self.ser_laser = serial.Serial(port=self.cl.port_laser, baudrate=self.cl.baudrate_laser)
        #self.laser = PulseLaserController(self.ser_laser)　レーザー装置につないでないので保留
        # メモ：ZaberControllerクラスのインスタンスを作成
        self.Zaberhandler = ZaberController("COM3")
        self.stage = None
       # Clock.schedule_interval(self.update_position, 0.1)  # 0.1秒ごとに位置を更新．エラーが起きたので保留

    def update_position(self):
        self.pos_x, self.pos_y = self.stage.get_position()
        pass

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
        self.Zaberhandler.move_right(float(self.ids.speed_input.text))
        pass

    def move_rect(self):
        self.Zaberhandler.vel = float(self.ids.speed_input.text)
        self.Zaberhandler.move_right()
        time.sleep(float(self.ids.deltaX.text) / float(self.ids.speed_input.text))
        self.Zaberhandler.stop_all()
        # self.Zaberhandler.x_relative_position = 0
        # self.Zaberhandler.y_relative_position = -int(self.ids.deltaY.text)
        # self.Zaberhandler.move_relative()
        pass
        #
    def move_line(self):
        self.x_relative_position = self.ids.deltaX.text
        self.y_relative_position = self.ids.deltaY.text
        move_relative(self)
        pass
        #
    #set origin
    def set_org(self):
        self.Zaberhandler.x_relative_position = 0
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
        self.Zaberhandler.quit()


class MainApp(App):
    def build(self):
        window = MainWindow()
        return window

    #必要になるかも
    # class CrashHandler(ExceptionHandler):
    #     def handle_exception(self, inst):
    #         print(inst)
    #         return ExceptionManager.PASS
    #
    # ExceptionManager.add_handler(CrashHandler())


if __name__ == '__main__':
    MainApp().run()

