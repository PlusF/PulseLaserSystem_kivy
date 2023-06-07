from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.base import ExceptionManager, ExceptionHandler
# メモ：ZaberControllerクラスをインポート

Window.size = (350, 700)

class MainWindow(BoxLayout):
    delta_x = NumericProperty(100)
    delta_y = NumericProperty(50)
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
