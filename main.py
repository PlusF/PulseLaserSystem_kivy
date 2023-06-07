from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
# メモ：ZaberControllerクラスをインポート

Window.size = (300, 700)

class MainWindow(BoxLayout):
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


if __name__ == '__main__':
    MainApp().run()
