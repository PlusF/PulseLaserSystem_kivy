import serial
from kivy.app import App
from kivy.uix.widget import Widget

from kivy.core.window import Window, Clock
from kivy.properties import NumericProperty
from ConfigLoader import ConfigLoader
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

from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.base import ExceptionManager, ExceptionHandler
import math
# メモ：ZaberControllerクラスをインポート



class CrashHandler(ExceptionHandler):
    def handle_exception(self, inst):
        print(inst)
        return ExceptionManager.PASS

class MainWindow(BoxLayout):
    delta_x = NumericProperty(100)
    delta_y = NumericProperty(50)
    Window.size = (350, 700)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_request_close=self.quit)

        self.cl = ConfigLoader('./config.json')

        self.freq: int = 100
        self.speed: float = 100.0
        self.ser_laser = serial.Serial(port=self.cl.port_laser, baudrate=self.cl.baudrate_laser)
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
    def check(self,text):
        print(text)

    def check_freq(self,text):
        num = int(text)
        if num < 16 :
            num = 16
        elif num > 10000:
            num = 10000
        
        return str(num)
    
    def check_speed(self,text):
        num = int(text)
        if num < 1 :
            num = 1
        elif num > 1000:
            num = 1000
        
        return str(num)
    
    def set_freq_from_slider(self,value):
        freq = 0
        if value==1:
            freq = 16
        elif value==2:
            freq = 50
        elif value==3:
            freq = 100
        elif value==4:
            freq = 500
        elif value==5:
            freq = 1000
        elif value==6:
            freq = 5000
        elif value==7:
            freq = 10000
        return freq
    
    def set_speed_from_slider(self, value):
        speed = 0
        if value==1:
            speed = 1
        elif value==2:
            speed = 5
        elif value==3:
            speed = 10
        elif value==4:
            speed = 50
        elif value==5:
            speed = 100
        elif value==6:
            speed = 500
        elif value==7:
            speed = 1000
        return speed
    
    def start_program_mode(self):
        pass


    ExceptionManager.add_handler(CrashHandler())





class MainApp(App):
    def build(self):
        window = MainWindow()
        return window





if __name__ == '__main__':
    MainApp().run()
    
