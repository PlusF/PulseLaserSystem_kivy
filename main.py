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
