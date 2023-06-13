from kivy.app import App
from kivy.uix.widget import Widget
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
        # TODO: IMPLEMENT ME
        # メモ：ZaberControllerクラスのインスタンスを作成

    def move_top(self):
        # TODO: IMPLEMENT ME
        # メモ：ZaberControllerインスタンスのmove_top関数を呼び出す
        pass

    def move_bottom(self):
        # TODO: IMPLEMENT ME
        pass

    def move_left(self):
        # TODO: IMPLEMENT ME
        pass

    def move_right(self):
        # TODO: IMPLEMENT ME
        pass

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
    
